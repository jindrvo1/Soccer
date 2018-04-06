library(ggplot2)
library(ggthemes)
library(dplyr)

df <- read.csv('Ratings.csv', sep=',', header=T)

cols <- names(df)
cols <- cols[2:length(cols)]
cols <- cols[1:(length(cols)/2)]

elos <- select(filter(df), c(cols))
players <- select(filter(df), 'player')
games <- 1:(length(cols))-1

plot <- ggplot() + 
  theme_bw()
for(i in games) {
  print(i)
}
