library(tidyverse)
library(ggrepel)
library(ggimage)
library(nflfastR)
library(hash)
library(data.table)


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


kicker_fantasy_stats <- pbp %>%
  filter(play_type == "field_goal" | play_type == "extra_point") %>%
  inner_join(id_map, by = c("kicker_player_id" = "gsis_id")) %>%
  mutate(
    kick_result = ifelse(extra_point_attempt, extra_point_result, field_goal_result),
    abbr_name = paste(substr(first_name, 1, 1) , last_name, sep = ".")
  ) %>%
  select(
    kicker_player_id,
    rotowire_id,
    yahoo_id,
    sportradar_id,
    espn_id,
    team,
    first_name,
    last_name,
    abbr_name,
    week,
    extra_point_attempt,
    kick_distance,
    kick_result
  ) 

kicker_fantasy_stats$kick_result <- replace(kicker_fantasy_stats$kick_result, kicker_fantasy_stats$kick_result == "made", "good")
kicker_fantasy_stats$kick_result <- replace(kicker_fantasy_stats$kick_result, kicker_fantasy_stats$kick_result == "failed", "missed")