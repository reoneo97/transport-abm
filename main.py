from env.env import *
from agents.agent import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from easydict import EasyDict
from tqdm import tqdm
from utils import *
from data_anim import *
import sys 
import random
import os

def create_env(path = "./data/locations.csv",capacity = 300):
    '''
    Initialization function to create the transport network for the simulation
    Transport network is being represented by a weighted directed graph
    path - csv file which provides the names of the different nodes and the corresponding weights
    capacity - capacity of each station, in this model capacities of the different models are the same
    '''
    graph = Graph()
    df = pd.read_csv(path)

    locations_str = set(df["loc1"].tolist()+df["loc2"].tolist())
    loc_dict = {i:Location(i) for i in locations_str}
    locations = list(loc_dict.values())
    transit_locations = []

    for i in df.values.tolist():
        weight = i[2]
        graph.add_edge(loc_dict[i[0]],loc_dict[i[1]],weight)
        transit1 = i[0]+"->"+i[1]
        transit2 = i[1]+"->"+i[0]
        transit_locations.append(TransitLocation(transit1,loc_dict[i[1]],weight,capacity))
        transit_locations.append(TransitLocation(transit2,loc_dict[i[0]],weight,capacity))
    config = ""
    env = Environment(graph,locations,transit_locations,cfg = config)
    return env

def createAgents(cfg,loc2idx,travel_times, n_agents = 10000):
    '''
     agent_config = {"home":"Bishan","dest": "Tuas","start_work_time": time(hour = 7, minute = 30),
                    "end_work_time": time(hour = 10, minute = 30)}    
    The start_work_time here will be the time where the agent leaves the house. This already takes into
    account the travel time required to travel to the workplace. Leave time will of course be dependent only 
    on working/schooling hours
    n_agents is the number of agents to simulate 

    '''
    locations = cfg.Locations
    #Creating Students
    # 3 Paramters which we have to draw from which is the 2 locations and the start_time
    n_stud = int(cfg.prob_student*n_agents*1.1)
    stud_homes = np.random.choice(locations,size = n_stud,p = cfg.prob_student_home)
    stud_schools = np.random.choice(locations,size = n_stud,p = cfg.prob_student_home)
    school_start = np.random.choice(cfg.school_start, size = n_stud)
    school_end = np.random.choice(cfg.school_end,size = n_stud)
    agent_cfgs = []
    start_end = []
    time_diffs = []
    for (i,j,k,l) in zip(stud_homes,stud_schools,school_start,school_end):
        r,c = loc2idx[i],loc2idx[j]
        time_diff = travel_times[r,c]
        time_diffs.append(time_diff)
        mins = time_diff%60
        hrs = time_diff//60
        dt = -timedelta(minutes=mins,hours=hrs)
        k = add_time(k,dt)
        if i==j:continue
        agent_config = {"home":i,"dest":j,"start_work_time":k,"end_work_time":l}
        start_end.append((i,j))
        agent_cfgs.append(agent_config)
        

    #Creating Adults
    n_emp = int(cfg.prob_employee*n_agents*1.1)

    default_start = datetime.combine(date.today(), time(hour = 9))

    emp_homes = np.random.choice(locations,size = n_emp,p = cfg.prob_employee_home)
    emp_work = np.random.choice(locations,size = n_emp,p = cfg.prob_employee_work)
    start_delta = 60*np.random.randn(n_emp)
    start_delta = start_delta//15
    work_hours = np.random.choice(cfg.work_hours,size=n_emp,p =cfg.work_hours_prob)
    
    for (i,j,k,l) in zip(emp_homes,emp_work,start_delta,work_hours):
        r,c = loc2idx[i],loc2idx[j]
        time_diff = travel_times[r,c]
        time_diffs.append(time_diff)
        if i==j:continue
        start = default_start + timedelta(minutes = k)
        end = start + l
        start_time = start - timedelta(minutes = time_diff)
        agent_config = {"home":i,"dest":j,"start_work_time":start_time.time(),"end_work_time":end.time()}  
        agent_cfgs.append(agent_config)
        start_end.append((i,j))      
    random.shuffle(agent_cfgs)

    avg_time = np.array(time_diffs).mean()*1.1
    return agent_cfgs[:n_agents],avg_time

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
    cfg["school_end"] = [time(13,15 + (15*i)) for i in range(2)] 

    #Working Hours
    cfg["work_hours_prob"] = [0.05,0.2,0.5,0.2,0.05]
    cfg["work_hours"] = [timedelta(hours = (7+i)) for i in range(5)]
    cfg = EasyDict(cfg)
    return cfg
    
def add_time(t,t_delta):
    dt = datetime.combine(date.today(), t)
    dt = dt + t_delta
    return dt.time()
def capacity_sim(capacity):

    logs_folder = "logs/capacity/"
    if not os.path.exists(logs_folder):
         os.makedirs(logs_folder)
    log_txt = logs_folder + "capacity" + str(capacity) + ".txt"
    log_csv = logs_folder + "capacity" + str(capacity) + ".csv"
    np.random.seed(73)

    if not os.path.exists('logs'):
        os.makedirs('logs')
    stdoutOrigin=sys.stdout 
    sys.stdout = open(log_txt, "w")
    env = create_env(capacity= capacity)
    all_locs = [loc.name for loc in env.locations + env.transit_locations]

    print("Initializing Log")
    print("="*80)
    print("List of all Locations:")

    for i in all_locs:print(i)
    cfg = generateConfig()          
    loc2idx = env.loc2idx
    travel_times = env.travel_times
    agent_configs,avg_time = createAgents(cfg,loc2idx,travel_times)
    
    print("="*80)
    print("Number of Agents:",len(agent_configs))
    print("="*80)

    for i in agent_configs:
        env.add_agent(i)
    env.set_tick(5,0)
    
    for i in tqdm(range(500)):
         env.tick()
         env.check_locations() 
    sys.stdout.close()
    sys.stdout=stdoutOrigin
    print("Parsing Log")
    parse_log(log_txt,log_csv)
    avg_time2 = average_travel_time(log_csv)
    print(f"Ideal Average Time: {avg_time} minutes")
    print(f"Actual Average Time: {avg_time2} minutes")
def delay_sim(delay_loc):
    
    logs_folder = "logs/node_delay/"
    if not os.path.exists(logs_folder):
         os.makedirs(logs_folder)
    log_txt = logs_folder + "delay" + delay_loc + ".txt"
    log_csv = logs_folder + "delay" + delay_loc + ".csv"
    np.random.seed(73)
    if not os.path.exists('logs'):
        os.makedirs('logs')
    stdoutOrigin=sys.stdout 
    sys.stdout = open(log_txt, "w")
    env = create_env(capacity = 300)
    all_locs = [loc.name for loc in env.locations + env.transit_locations]

    print("Initializing Log")
    print("="*80)
    print("List of all Locations:")

    for i in all_locs:print(i)
    cfg = generateConfig()          
    loc2idx = env.loc2idx
    travel_times = env.travel_times
    agent_configs,avg_time = createAgents(cfg,loc2idx,travel_times)
    
    print("="*80)
    print("Number of Agents:",len(agent_configs))
    print("="*80)
    #Doing the delay
    affected = [loc.name for loc in env.transit_locations if delay_loc in loc.name]


    for i in agent_configs:
        env.add_agent(i)
    env.set_tick(5,0)
    
    for i in tqdm(range(24)):
         env.tick()
         env.check_locations() 
    for loc in affected:
        env.add_travel_time(loc,10)
    for i in tqdm(range(72)):
         env.tick()
         env.check_locations() 
    for loc in affected:
        env.reduce_travel_time(loc,10)
    for i in tqdm(range(404)):
         env.tick()
         env.check_locations() 

    sys.stdout.close()
    sys.stdout=stdoutOrigin
    print("Parsing Log")
    parse_log(log_txt,log_csv)
    avg_time2 = average_travel_time(log_csv)
    print(f"Delay on {delay_loc}")
    print(affected)
    print(f"Ideal Average Time: {avg_time} minutes")
    print(f"Actual Average Time: {avg_time2} minutes")



if __name__ == "__main__":
    ls = ['Paya Lebar', 'Punggol', 'Jurong', 'Tiong Bahru', 'Serangoon', 'Tampines',
        'Tuas','CCK', 'Woodlands', 'Buona', 'CBD', 'Town', 'Bishan', 'Toa Payoh']
    for l in ls:
        delay_sim(l)
    # #Parameters to set to name the files
    # logs_folder = "logs/"
    # video_folder = "logs/videos/"
    # if not os.path.exists('logs'):
    #     os.makedirs('logs')

    # sim_name = "base"
    # capacity = 300
    # log_txt = logs_folder + sim_name + ".txt"
    # log_csv = logs_folder + sim_name + ".csv"
    # log_video = video_folder + sim_name + ".html"

    # to_log = True #Almost always set this to true
    # to_video =True #Only set to true if you want to save the video of the simulation 
    
    # np.random.seed(73)
    # if to_log:    
    #     stdoutOrigin=sys.stdout 
    #     sys.stdout = open(log_txt, "w") 
    # env = create_env(capacity= capacity)
    # all_locs = [loc.name for loc in env.locations + env.transit_locations]

    # print("Initializing Log")
    # print("="*80)
    # print("List of all Locations:")

    # for i in all_locs:print(i)
    # cfg = generateConfig()          
    # loc2idx = env.loc2idx
    # travel_times = env.travel_times
    # agent_configs,avg_time = createAgents(cfg,loc2idx,travel_times)
    
    # print("="*80)
    # print("Number of Agents:",len(agent_configs))
    # print("="*80)

    # for i in agent_configs:
    #     env.add_agent(i)
    # #Parameter here is to set the timedelay which we do the simulation. 
    # env.set_tick(5,0)
    
    # for i in tqdm(range(500)):
    #      env.tick()
    #      env.check_locations()

    # if to_log:
    #     sys.stdout.close()
    #     sys.stdout=stdoutOrigin
    # print(f"Ideal Average Time: {avg_time} minutes")

    # # Parsing the .txt file and converting it to a .txt file
    # print("Parsing Log")
    # parse_log(log_txt,log_csv)
    # avg_time2 = average_travel_time(log_csv)
    # print(f"Actual Average Time: {avg_time2} minutes")

    # map_df,trans_df = load_data(log_csv)
    # if to_video:
    #     start_time = 5
    #     end_time = int(start_time + 60*17/5 + 6)

    #     map_day = map_df.iloc[:,:end_time]  
    #     trans_day = trans_df.iloc[:,:end_time]

    #     print("Creating Animation")
    #     create_animation(map_day,trans_day,log_video,"mp4")