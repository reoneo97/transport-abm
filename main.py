from env.env import *
from agents.agent import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from easydict import EasyDict
from tqdm import tqdm
import sys 

def create_env(path = "./data/locations.csv",private_path = "./data/locations_private.csv"):
    #Function to read the csv file of locations and the connectivity and return a graph
    graph = Graph()
    graph2 = Graph()
    df = pd.read_csv(path)

    locations_str = set(df["loc1"].tolist()+df["loc2"].tolist())
    loc_dict = {i:Location(i) for i in locations_str}
    locations = list(loc_dict.values())
    transit_locations = []

    for i in df.values.tolist():
        graph.add_edge(loc_dict[i[0]],loc_dict[i[1]],i[2])
        transit1 = i[0]+"->"+i[1]
        transit2 = i[1]+"->"+i[0]
        transit_locations.append(TransitLocation(transit1,loc_dict[i[1]],i[2]))
        transit_locations.append(TransitLocation(transit2,loc_dict[i[0]],i[2]))
    config = ""
    env = Environment(graph, graph2, locations,transit_locations,config)
    return env

def createAgents(cfg,loc2idx,travel_times, n_agents = 11000):
    '''
     agent_config = {"home":"Bishan","dest": "Tuas","start_work_time": time(hour = 7, minute = 30),
                    "end_work_time": time(hour = 10, minute = 30)}    
    The start_work_time here will be the time where the agent leaves the house. This already takes into
    account the travel time required to travel to the workplace. Leave time will of course be dependent only 
    on working/schooling hours

    '''
    locations = cfg.Locations
    #Creating Students
    # 3 Paramters which we have to draw from which is the 2 locations and the start_time
    n_stud = int(cfg.prob_student*n_agents)
    stud_homes = np.random.choice(locations,size = n_stud,p = cfg.prob_student_home)
    stud_schools = np.random.choice(locations,size = n_stud,p = cfg.prob_student_home)
    school_start = np.random.choice(cfg.school_start, size = n_stud)
    school_end = np.random.choice(cfg.school_end,size = n_stud)
    agent_cfgs = []
    dupes = 0
    for (i,j,k,l) in zip(stud_homes,stud_schools,school_start,school_end):
        r,c = loc2idx[i],loc2idx[j]
        time_diff = travel_times[r,c]
        mins = time_diff%60
        hrs = time_diff//60
        dt = -timedelta(minutes=mins,hours=hrs)
        k = add_time(k,dt)
        if i==j:continue
        agent_config = {"home":i,"dest":j,"start_work_time":k,"end_work_time":l}
        agent_cfgs.append(agent_config)

    #Creating Adults
    n_emp = int(cfg.prob_employee*n_agents+1)

    default_start = datetime.combine(date.today(), time(hour = 9))

    emp_homes = np.random.choice(locations,size = n_emp,p = cfg.prob_employee_home)
    emp_work = np.random.choice(locations,size = n_emp,p = cfg.prob_employee_work)
    start_delta = 60*np.random.randn(n_emp)
    start_delta = start_delta//15
    work_hours = np.random.choice(cfg.work_hours,size=n_emp,p =cfg.work_hours_prob)

    for (i,j,k,l) in zip(emp_homes,emp_work,start_delta,work_hours):
        r,c = loc2idx[i],loc2idx[j]
        time_diff = travel_times[r,c]
        if i==j:continue
        start = default_start + timedelta(minutes = k)
        end = start + l
        start_time = start - timedelta(minutes = time_diff)
        agent_config = {"home":i,"dest":j,"start_work_time":start_time.time(),"end_work_time":end.time()}  
        agent_cfgs.append(agent_config)      
    print(dupes)
    return agent_cfgs

def generateConfig(path = "data/locations_data.csv"):
    #Function to generate the configuration file such as probability etc. from data that we have obtained
    cfg = {}
    #For each probability distribution save it as a dictionary ie. {"Student": 0.3, "Employee": 0.7}
    df = pd.read_csv(path)
    student_total = df["student_home"].sum()
    employee_total = df["people_home"].sum()
    popn_total = student_total + employee_total

    #Probability distribution for Student vs Employee
    cfg["Locations"] = df["location"].values
    cfg["prob_student"] = student_total/popn_total
    cfg["prob_employee"] = employee_total/popn_total 

    #Probability distribution for home locations
    cfg["prob_student_home"] = [i/student_total for i in df["student_home"]]
    cfg["prob_employee_home"] = [i/employee_total for i in df["people_home"]]

    #Probability distribution for work/school locations
    student_total = df["student_school"].sum()
    work_total = df["people_work"].sum()

    cfg["prob_student_school"] = [i/student_total for i in df["student_school"]]
    cfg["prob_employee_work"] = [i/work_total for i in df["people_work"]]

    #Timing Probability Distributions
    cfg["school_start"] = [time(7,15*i) for i in range(4)]
    cfg["school_end"] = [time(13,15 + (15*i)) for i in range(3)] 

    #Working Hours
    cfg["work_hours_prob"] = [0.05,0.2,0.5,0.2,0.05]
    cfg["work_hours"] = [timedelta(7+i) for i in range(5)]
    cfg = EasyDict(cfg)
    return cfg
    
def add_time(t,t_delta):
    dt = datetime.combine(date.today(), t)
    dt = dt + t_delta
    return dt.time()





if __name__ == "__main__":

    env = create_env()
    # print({loc.name:loc for loc in env.locations})
    cfg = generateConfig()          
    loc2idx = env.loc2idx
    travel_times = env.travel_times

    agent_configs = createAgents(cfg,loc2idx,travel_times) 
    for i in agent_configs:
        env.add_agent(i)