class EloForTeams(object):
    def __init__(self, K_FACTOR = 32):
        self.K_FACTOR = K_FACTOR

    # t1: list of first team's players' ratings
    # t2: list of seconds team's players' ratings
    #
    # returns a tuple of two numbers representing each team's expectancy to win
    def predict_winner(self, t1, t2):
        r_t1, r_t2 = self.teams_ratings(t1, t2)

        e_t1 = 1.0/(1+10**((r_t2-r_t1)/400))
        e_t2 = 1-e_t1

        return (e_t1, e_t2)

    # t1: list of first team's players' ratings
    # t2: list of seconds team's players' ratings
    # s_t1: 0/0.5/1 number representing first team's score
    # s_t2: 0/0.5/1 number representing seconds team's score
    # scores have to add up to 1, leaving us with only three possible scenarios ([0,1],[1,0],[0.5,0.5])
    # score of 0 means the team lost, score of 1 means it won and score of 0.5 means the match was a draw
    #
    # returns a tuple of two lists of numbers, each list representing of two teams, each number representing each player's new rating
    def rate_match(self, t1, t2, s_t1, s_t2):
        r_t1, r_t2 = self.teams_ratings(t1, t2)
        e_t1, e_t2 = self.predict_winner(t1, t2)

        r_t1_new = r_t1 + self.K_FACTOR*(s_t1-e_t1)
        r_t2_new = r_t2 + self.K_FACTOR*(s_t2-e_t2)

        t1_new = [r + (r_t1_new-r_t1)*((r_t1_new - (2*s_t1-1)*(r - r_t1))/r_t1_new) for r in t1]
        t2_new = [r + (r_t1_new-r_t1)*((r_t2_new - (2*s_t2-1)*(r - r_t2))/r_t2_new) for r in t1]

        return (t1_new, t2_new)

    # t1: list of first team's players' ratings
    # t2: list of seconds team's players' ratings
    #
    # returns a tuple of two numbers, each number representing team's elo rating
    # team's elo rating is calculated as average rating of all players in given team
    def teams_ratings(self, t1, t2):
        return (sum(t1)/len(t1), sum(t2)/len(t2))

    # K_FACTOR: value the K_FACTOR should be set to
    # default value of K_FACTOR is 32
    def set_k_factor(self, K_FACTOR):
        self.K_FACTOR = K_FACTOR

    # returns the K_FACTOR's current value
    def get_k_factor(self):
        return self.K_FACTOR