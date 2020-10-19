import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from tqdm import tqdm 

def parse_log(path,save_file):
    '''
    This utility function converts the log that was created by the simulation and converts it
    to a time-series csv which can then be more easily analysed and graphed. 
    '''
    with open(path,"r") as f:
        lines = [line.rstrip('\n') for line in f]
    f.close()
    locations = []
    locidx = lines.index("List of all Locations:")
    locidx2 = lines.index("="*80,locidx)
    for i in range(locidx+1,locidx2):
        locations.append(lines[i])
    data = {loc:[] for loc in locations}
    time_idx = []
    start_idx = locidx2+3
    i = start_idx
    while i <len(lines):
        if lines[i][0] == "(":
            curr_time = lines[i][2:-2]
            time_idx.append(curr_time)
            loc_data = {loc:0 for loc in locations}
            i += 1
            while i < len(lines) and lines[i][0] != "(" :
                k,v = lines[i].split(":")
                loc_data[k] = v
                i += 1
            for k,v in loc_data.items():
                data[k].append(v)
    data = pd.DataFrame(data,index = time_idx)
    data.to_csv(save_file)
def average_travel_time(csv_path):
    df = pd.read_csv(csv_path,index_col=0)
    agents = df.iloc[0].sum()
    transit_locs = [loc for loc in df.columns if ">" in loc ]
    trans_df = df[transit_locs]
    sums = trans_df.sum().sum()
    return sums*5/agents/2




if __name__ == "__main__":
    parse_log("logs/cap50.txt","logs/cap50.csv")