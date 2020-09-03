class Agent:
    def __init__(self,env,income,prob,home,dest,work_time):
        self.income = income
        self.prob = prob
        self.home = home
        loc2idx = env.loc2idx
        self.dest = dest
        self.work_time = work_time

        self.path_to_dest = env.paths[home][loc2idx[dest]]
        self.path_to_home = env.paths[dest][loc2idx[home]]
        self.env = env
        self.current_location = home
        self.delay = 0
    def move(self, loc1, loc2):

        
        pass
    def update(self):
        if self.env.time > self.work_time:
            self.move(self.home,self.dest)
        elif self.current_location.transit == True:
            pass

