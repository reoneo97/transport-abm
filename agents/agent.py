class Agent:
    def __init__(self,env,income,prob,home,dest,start_work_time,end_work_time):
        self.income = income
        self.prob = prob
        self.home = env.locmap[home]
        self.dest = env.locmap[dest]
        self.start_work_time = start_work_time
        self.end_work_time = end_work_time


        self.path_to_dest = env.paths[home][env.loc2idx[dest]]
        self.path_to_home = self.path_to_dest[::-1]
        self.env = env
        self.current_location = self.home
        self.delay = 0

        self.queue = None #This is a queue which will indicate if the person is travelling 
        self.status = 0 #  0 for at home and 1 for at work 

    def move_work(self):
        self.queue = self.path_to_dest[1:]
        self.status = 1
        print("Agent going to work")
    def move_home(self):
        self.queue = self.path_to_dest[1:]
        self.status =0 
        print("Agent going home")

    def update(self,current_time,timestep):
        #Check if the agent should go work/go home
        if current_time.time() > self.start_work_time and not self.status:
            self.move_work()
        elif current_time.time() > self.end_work_time and self.status:
            self.move_home()
        elif self.queue:
            return self.queue.pop(0)

    def update_delay(self,timestep):
        self.delay -= timestep
        print(self.delay)
        return self.delay 
