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

def createAgents(cfg,loc2idx, n_agents = 10000):
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
    print(np.random.choice(locations,size = n_stud,p = cfg.prob_student_home))


    
    #Creating Adults
    n_emp = int(cfg.prob_employee*n_agents)

    return 0 

def generateConfig(path = "data/locations_data.csv"):
    #Function to generate the configuration file such as probability etc. from data that we have obtained
    Cfg = {}
    #For each probability distribution save it as a dictionary ie. {"Student": 0.3, "Employee": 0.7}
    df = pd.read_csv(path)
    student_total = df["student_home"].sum()
    employee_total = df["people_home"].sum()
    popn_total = student_total + employee_total
    #Probability distribution for Student vs Employee
    Cfg["Locations"] = df["location"].values
    Cfg["prob_student"] = student_total/popn_total
    Cfg["prob_employee"] = employee_total/popn_total 

    #Probability distribution for home locations

    #Student Homes
    Cfg["prob_student_home"] = [i/student_total for i in df["student_home"]]
    Cfg["prob_employee_home"] = [i/employee_total for i in df["people_home"]]
    #Probability distribution for work/school locations

    student_total = df["student_school"].sum()
    work_total = df["people_work"].sum()

    Cfg["prob_student_school"] = [i/student_total for i in df["student_school"]]
    Cfg["prob_employee_work"] = [i/work_total for i in df["people_work"]]

    Cfg = EasyDict(Cfg)
    return Cfg
    





if __name__ == "__main__":
    # stdoutOrigin=sys.stdout 
    # sys.stdout = open("logs/log.txt", "w") 
    env = create_env()
    # print({loc.name:loc for loc in env.locations})
    a = env.add_agent(agent_config=0)
    cfg = generateConfig()          
    loc2idx = env.loc2idx

    agent_configs = createAgents(cfg,loc2idx)   
    # for i in tqdm(range(500)):
    #     env.tick()
    #     env.check_locations()
    # sys.stdout.close()
    # sys.stdout=stdoutOrigin