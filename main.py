from env.env import *
from agents import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_graph(path = "./cfg/locations.csv"):
    df = pd.read_csv(path)
    
    for i in df.iterrows():
        print(i)
        print("yo")


if __name__ == "__main__":
    hi = Graph()
    create_graph()

