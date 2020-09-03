from env.env import *
from agents.agent import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *

def create_env(path = "./cfg/locations.csv"):
    #Function to create the network 
    graph = Graph()
    df = pd.read_csv(path)
    locations = set(df["loc1"].tolist()+df["loc2"].tolist())
    loc_dict = {i:Location(i) for i in locations}
    locations = list(locations)
    for i in df.values.tolist():
        graph.add_edge(loc_dict[i[0]],loc_dict[i[1]],i[2])
        transit1 = i[0]+"->"+i[1]
        transit2 = i[1]+"->"+i[0]
        locations.append(Location(transit1,True))
        locations.append(Location(transit2,True))
    config = ""
    env = Environment(graph, locations,config)
    return env
        


if __name__ == "__main__": 
    env = create_env()
    print(env.locations)
    a = Agent(env,2000,0.5,"Bishan","Tiong Bahru",time(hour = 7, minute = 30))
    print(a.path_to_dest)
    print(a.path_to_home)
    print([str(i) for i in env.locations])


