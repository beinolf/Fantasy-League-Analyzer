library(tidyverse)
library(ggrepel)
library(ggimage)
library(nflfastR)
library(hash)
library(data.table)

def_id_map <- read.csv(file = 'data/def_pid_map.csv')