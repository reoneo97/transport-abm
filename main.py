from env.env import *
from agents import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_env(path = "./cfg/locations.csv"):
    #Function to create the network 
    graph = Graph()
    df = pd.read_csv(path)
    locations = set(df["loc1"].tolist()+df["loc2"].tolist())
    locations = {i:Location(i) for i in locations}
    for i in df.values.tolist():
        graph.add_edge(locations[i[0]],locations[i[1]],i[2])
    env = Environment(graph, locations)
    return env

        


if __name__ == "__main__": 
    gp = create_env()
    # print(gp.graph.apsp())
    # print(gp.graph.nodes)
    print(gp.graph.data)
    gp.graph.shortest_path("Tampines")
    


