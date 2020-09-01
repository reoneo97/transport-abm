class Agent:
    def __init__(self,env,income,prob,home,dest):
        self.income = income
        self.prob = prob
        self.home = home
        loc2idx = env.loc2idx
        self.dest = dest
        self.path_to_dest = env.paths[home][loc2idx[dest]]
        self.path_to_home = env.paths[dest][loc2idx[home]]
    def move(self):
        pass