library(ggplot2)
library(ggthemes)
library(reshape2)

df <- read.csv('Games.csv', sep=',', header=T)
df$goals <- NULL
df$total <- NULL
df <- melt(df)

ggplot(df, aes(x=player, y=value, fill=variable)) +
  theme_bw() +
  xlab("Players") +
  ylab("Number of games") +
  scale_fill_manual(values = c("green","red"),
                     name="Games",
                     breaks=c("won", "lost"),
                     labels=c("Won", "Lost")) +
  geom_bar(stat="identity", width=.7, position="dodge")

ggsave("Games.png",path="Graphs/")
