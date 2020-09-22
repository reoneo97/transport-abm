from env.env import *
from agents.agent import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from easydict import EasyDict
from tqdm import tqdm
import sys 

def create_env(path = "./data/locations.csv"):
    #Function to read the csv file of locations and the connectivity and return a graph
    graph = Graph()
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
    env = Environment(graph, locations,transit_locations,config)
    return env

def createAgents():
    '''
     agent_config = {"home":"Bishan","dest": "Tuas","start_work_time": time(hour = 7, minute = 30),
                    "end_work_time": time(hour = 10, minute = 30)}    


    '''
    pass

def generateConfig():
    #Function to generate the configuration file such as probability etc. from data that we have obtained
    Cfg = EasyDict()
    #For each probability distribution save it as a dictionary ie. {"Student": 0.3, "Employee": 0.7}

    #Probability distribution for Student vs Employee

    #Probability distribution for home locations


    #Probability distribution for work locations


    #Probability distribution for work timings



    pass
    





if __name__ == "__main__":
    stdoutOrigin=sys.stdout 
    sys.stdout = open("logs/log.txt", "w") 
    env = create_env()
    print({loc.name:loc for loc in env.locations})
    env.locations
    a = env.add_agent(agent_config=0)
    
    for i in tqdm(range(500)):
        env.tick()
        env.check_locations()
    sys.stdout.close()
    sys.stdout=stdoutOrigin