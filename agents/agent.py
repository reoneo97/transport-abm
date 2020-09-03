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


class Student(Agent):
    def home(self):
        pass

    def destination(self):
        path = os.path.join(input_dir, 'cn4238r_schools.csv')
        data = pd.read_csv(path)

        # find total no. of schools
        total = data.sum(axis=0)
        probs = []
        schs_column = data.iloc[:, 1]
        schs = list(schs_column)

        # find probability for each region
        for number in schs:
            probability = number / total[1]
            probs.append(probability)

        # get destination for student
        dest_no = np.random.choice(len(probs), p=probs)
        dest = school_locations.locations[dest_no]
        print(dest)

    def transport_mode(self):
        pass


class Employee(Agent):
    def home(self):
        pass

    def destination(self):
        pass

    def transport_mode(self):
        pass