library(tidyverse)
library(ggrepel)
library(ggimage)
library(nflfastR)
library(hash)
library(data.table)

#' Increments the provided hash at the provided key and value location 
#'
#' @param i_hash - Hash to increment, format expected is a csv string set of values
#' @param key - key to locate value
#' @param inc_V_loc - increment value location, location in the string to increment ex. 2 would increment "1,1" to "1,2"
increment_hash <- function(i_hash, key, inc_V_loc) {
  inc_V_loc <- inc_V_loc * 2 - 1
  curr_value <- values(i_hash, keys = key)
  del(key, i_hash)
  substring(curr_value, inc_V_loc, inc_V_loc) <-
    as.character(as.numeric(substring(curr_value, inc_V_loc, inc_V_loc)) + 1)
  .set(i_hash, keys = key, values = curr_value)
}

#' Builds a row(s) of 40 yard weekly player data based on provided play-by-play row
#'
#' @param pbp_df - row of play-by-play data containing a 40+ yard play in dataframe format
#' @param fys_hash - forty yard stat hash to add data to 
build_fys <- function(pbp_df, fys_hash) {
  td_id <- pbp_df[["td_player_id"]]
  week <- as.numeric(pbp_df[["week"]])
  empty_value <- paste(0, 0, 0, 0, 0, 0, sep = ",")
  
  if (pbp_df[["play_type"]] == "pass") {
    pass_value_loc <- 1
    catch_value_loc <- 2
    pass_td_value_loc <- 4
    catch_td_value_loc <- 5
    pass_id <- pbp_df[["passer_player_id"]]
    catch_id <- pbp_df[["receiver_player_id"]]
    pass_key <- paste(pass_id, week, sep = ",")
    catch_key <- paste(catch_id, week, sep = ",")
    
    if (!has.key(pass_key, fys_hash)) {
      .set(fys_hash, keys = pass_key, values = empty_value)
    }
    
    if (!has.key(catch_key, fys_hash)) {
      .set(fys_hash, keys = catch_key, values = empty_value)
    }
    
    increment_hash(fys_hash, pass_key, pass_value_loc)
    increment_hash(fys_hash, catch_key, catch_value_loc)
    
    if (!is.na(td_id)) {
      increment_hash(fys_hash, pass_key, pass_td_value_loc)
    }
    
    if (!is.na(td_id) & td_id == catch_id) {
      increment_hash(fys_hash, catch_key, catch_td_value_loc)
    }
    
  } else {
    rush_value_loc <- 2
    rush_td_value_loc <- 6
    rush_id <- pbp_df[["rusher_player_id"]]
    rush_key <- paste(rush_id, week, sep = ",")
    
    if (!has.key(rush_key, fys_hash)) {
      .set(fys_hash, keys = rush_key, values = empty_value)
    }
    
    increment_hash(fys_hash, rush_key, rush_value_loc)
    
    if (!is.na(td_id) & td_id == rush_id) {
      increment_hash(fys_hash, rush_key, rush_td_value_loc)
    }
  }
}

#' Builds a row of offensive fumble return touchdown data based on provided play-by-play row
#'
#' @param pbp_ofr - row of play-by-play data containing an offensive fumble return touchdown in dataframe format
#' @param ofr_hash - offensive fumble return touchdown hash to add data to
build_ofr_td <- function(pbp_ofr, ofr_hash) {
  off_key <-
    paste(pbp_ofr[["td_player_id"]], pbp_ofr[["week"]], sep = ",")
  
  if (!has.key(off_key, ofr_hash)) {
    .set(ofr_hash, keys = off_key, values = "1")
  } else {
    increment_hash(ofr_hash, off_key, 1)
  }
}

#' Builds a row of offensive fumble return touchdown data based on provided play-by-play row
#'
#' @param pbp_ps - row of play-by-play data containing a pick six in dataframe format
#' @param ofr_hash - offensive fumble return touchdown hash to add data to
build_pick_six <- function(pbp_ps, ps_hash) {
  pass_key <-
    paste(pbp_ps[["passer_player_id"]], pbp_ps[["week"]], sep = ",")
  
  if (!has.key(pass_key, ps_hash)) {
    .set(ps_hash, keys = pass_key, values = "1")
  } else {
    increment_hash(ps_hash, pass_key, 1)
  }
}

# Get neccesary nflfastR data
players <- load_player_stats(2021)

pbp <- load_pbp(2021)

id_map <- fast_scraper_roster(2021) %>%
  select(
    gsis_id,
    rotowire_id,
    yahoo_id,
    sportradar_id,
    espn_id,
    team,
    jersey_number,
    first_name,
    last_name,
    position
  )

# Build forty yard stats dataframe
forty_yard_pbp <- pbp %>%
  filter(yards_gained >= 40 &
           week <= 18 &
           (play_type == "run" | play_type == "pass")) %>%
  select(
    week,
    passer_player_id,
    receiver_player_id,
    rusher_player_id,
    td_player_id,
    play_type
  )

fourty_yard_stats_hash <- hash()

apply(forty_yard_pbp, 1, build_fys, fourty_yard_stats_hash)

fourty_yard_stats_df <- as.list(fourty_yard_stats_hash) %>%
  as.data.frame(check.names = FALSE) %>%
  gather(key = "c_key", value = "c_values") %>%
  separate(
    col = "c_key",
    into = c("player_id", "week"),
    sep = ",",
    remove = TRUE
  ) %>%
  separate(
    col = "c_values",
    into = c(
      "fourty_yard_passes",
      "fourty_yard_receptions",
      "fourty_yard_rushes",
      "fourty_yard_passing_tds",
      "fourty_yard_receiving_tds",
      "fourty_yard_rushing_tds"
    ),
    sep = ",",
    remove = TRUE
  ) %>%
  mutate("week" = as.numeric(week))

# Build pick six dataframe
pick_six_pbp <- load_pbp(2021) %>%
  filter(interception == 1 & td_team == defteam)

pick_six_hash <- hash()

apply(pick_six_pbp, 1, build_pick_six, pick_six_hash)

pick_six_df <- as.list(pick_six_hash) %>%
  as.data.frame(check.names = FALSE) %>%
  gather(key = "c_key", value = "pick_sixes") %>%
  separate(
    col = "c_key",
    into = c("player_id", "week"),
    sep = ",",
    remove = TRUE
  )  %>%
  mutate("week" = as.numeric(week))


# Build offensive fumble return touchdown dataframe
offensive_fumble_rec_td_pbp <- load_pbp(2021) %>%
  filter(
    fumble == 1 &
      td_team == posteam &
      (
        td_player_id == fumble_recovery_1_player_id |
          td_player_id == fumble_recovery_2_player_id
      )
  )

offensive_fumble_rec_td_hash <- hash()

apply(offensive_fumble_rec_td_pbp,
      1,
      build_ofr_td,
      offensive_fumble_rec_td_hash)

ofr_df <- as.list(offensive_fumble_rec_td_hash) %>%
  as.data.frame(check.names = FALSE) %>%
  gather(key = "c_key", value = "ofr_tds") %>%
  separate(
    col = "c_key",
    into = c("player_id", "week"),
    sep = ",",
    remove = TRUE
  )  %>%
  mutate("week" = as.numeric(week))

# Join gathered and built data
fantasy_stats <- players %>%
  full_join(ofr_df,
            by = c("player_id" = "player_id", "week" = "week")) %>%
  left_join(fourty_yard_stats_df,
            by = c("player_id" = "player_id", "week" = "week")) %>%
  left_join(pick_six_df,
            by = c("player_id" = "player_id", "week" = "week")) %>%
  inner_join(id_map, by = c("player_id" = "gsis_id")) %>%
  mutate(
    incomplete_passes = attempts - completions,
    two_point_conversions = rushing_2pt_conversions + passing_2pt_conversions + receiving_2pt_conversions,
    fumbles_lost = sack_fumbles_lost + rushing_fumbles_lost + receiving_fumbles_lost,
    fumbles = sack_fumbles + rushing_fumbles + receiving_fumbles_lost,
    abbr_name = paste(substr(first_name, 1, 1) , last_name, sep = ".")
  ) %>%
  select(
    player_id,
    rotowire_id,
    yahoo_id,
    sportradar_id,
    espn_id,
    team,
    position,
    abbr_name,
    first_name,
    last_name,
    week,
    completions,
    passing_yards,
    passing_tds,
    interceptions,
    sacks,
    passing_first_downs,
    carries,
    rushing_yards,
    rushing_tds,
    rushing_first_downs,
    receptions,
    receiving_yards,
    receiving_tds,
    receiving_first_downs,
    incomplete_passes,
    two_point_conversions,
    fumbles,
    fumbles_lost,
    fourty_yard_passes,
    fourty_yard_rushes,
    fourty_yard_receptions,
    fourty_yard_passing_tds,
    fourty_yard_receiving_tds,
    fourty_yard_rushing_tds,
    pick_sixes,
    ofr_tds
  ) %>%
  filter(week <= 18) %>%
  mutate_all( ~ replace(., is.na(.), 0))

View(fantasy_stats)
