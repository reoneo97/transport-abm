from env.env import *
from agents.agent import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *

def create_env(path = "./data/locations.csv"):
    #Function to create the network 
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
        
import sys 



if __name__ == "__main__":
    stdoutOrigin=sys.stdout 
    sys.stdout = open("log.txt", "w") 
    env = create_env()
    print({loc.name:loc for loc in env.locations})
    env.locations
    a = env.add_agent(agent_config=0)
    
    for i in range(500):
        env.tick()
        env.check_locations()
    sys.stdout.close()
    sys.stdout=stdoutOrigin
    