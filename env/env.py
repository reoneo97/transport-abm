import numpy as np 
from datetime import timedelta, date, time,datetime
from agents.agent import *

class Location:
    def __init__(self,name):
        self.name = name
        self.agents = []

    def describe(self):
        #Function to return all the important information about the location
        #ie. 
        print(self.name,":",len(self.agents))
    
    def add(self,agent):
        self.agents.append(agent)
    def remove(self,agent):
        self.agents.remove(agent)

class TransitLocation(Location):
    #Additional 
    def __init__(self,name,end,wait_time):
        super().__init__(name)
        self.end = end # This will be an actual location object not just the string
        assert(type(end)== Location)
        self.wait_time = wait_time
    def add(self,agent):
        agent.delay = self.wait_time
        self.agents.append(agent)
    def update(self):

        to_remove = []
        for i,a in enumerate(self.agents):
            w = a.update_delay(5)
            if w <= 0:
                to_remove.append(i)
        for idx in to_remove:
            a = self.agents.pop(idx)
            self.end.add(a)

        
    def describe(self,verbose = True):
        #Function to return all the important information about the location
        #ie. 
        
        print(self.name,":",len(self.agents))



class Graph:
    # Graph implemented using an adjacency
    def __init__(self):
        self.data = {}
        self.nodes = []
        self.distances = None
        self.V = 0
        self.loc2idx = None

    def __str__(self):
        return str(self.data)

    def add_edge(self,loc1,loc2,weight):
        if loc1.name in self.data:
            self.data[loc1.name][loc2.name] = weight
        else:
            self.nodes.append(loc1.name)
            self.V += 1
            self.data[loc1.name] = {loc2.name: weight}
        
        if loc2.name in self.data:
            self.data[loc2.name][loc1.name] = weight
        else:
            self.nodes.append(loc2.name)
            self.V += 1
            self.data[loc2.name] = {loc1.name: weight}

    def shortest_path(self,start):
        #Shortest Path Algo based on Djikstra's Algorithm but using linear search instead of Priority Queue
        if self.loc2idx == None:
            self.loc2idx = {v:i for i,v in enumerate(self.nodes)}
        def find_entry(ls, name):
            #Helper function to find items inside the queue
            for i in ls:
                if i[1] == name:
                    return i
        solved = []

        parent = [-1]*self.V
        dist = [(float("inf"),i) if i != start else (0,i) for i in self.nodes] # Queue for all the items 
        while dist:
            vertex = min(dist)
            dist.remove(min(dist))
            solved.append(vertex)
            u = vertex[0]
            for loc,weight in self.data[vertex[1]].items(): #loc,weight is all the info outgoing edges from that node
                entry = find_entry(dist,loc) #Find the item inside the queue
                if entry and entry[0] > (u + weight):
                    #Relax the edge and update with the smallest distance
                    new_entry = ((u+weight),entry[1])
                    dist.remove(entry)
                    dist.append(new_entry)
                    parent[self.loc2idx[loc]] = self.loc2idx[vertex[1]]
        paths = []
        # Return all the paths for the different locations
        for i in range(len(parent)):
            idx = parent[i]
            if self.nodes[i] == start:
                paths.append([])
                continue
            path = [self.nodes[i]]
            while idx != -1:
                path.append(self.nodes[idx])
                idx = parent[idx]
            paths.append(path[::-1]) #Invert the Paths
        return paths,solved

class Environment:
    def __init__(self,graph,private_graph,locations,transit_locations,cfg = None,log_path = "../logs/log.txt"):
        self.graph = graph
        self.locations = locations
        self.transit_locations= transit_locations
        self.paths = {}
        self.generate_paths()

        self.loc2idx = graph.loc2idx
        self.locmap = {loc.name: loc for loc in (locations + transit_locations)}
        self.log_path = log_path

        self.timestep = timedelta(minutes=5)
        self.start_time = time(hour = 7)
        self.time = datetime(2020,1,1,hour = 7)
        self.date = 0
    
    def generate_paths(self):
        for loc in self.graph.nodes:
            loc_paths,_ = self.graph.shortest_path(loc)
            self.paths[loc] = loc_paths

    def tick(self):
        #Important function which basically signifies 1 timestep in the model
        self.time = self.time + self.timestep

        #Update Transit Locations
        for loc in self.locations:
            #TODO: To add functionality such that time taken will increase if there transit location is unable to accomodate the number of people
            for agent in loc.agents:
                dest = agent.update(self.time, self.timestep) 
                if dest:
                    new_loc = self.locmap[loc.name+"->"+dest]
                    self.move_agent(agent,loc,new_loc)
        for loc in self.transit_locations:
            loc.update()

        print("(",self.time,")")
    def new_day(self):
        pass

    def check_locations(self):
        #Function to check if everyone is at home
        for location in self.locmap.values():
            if location.agents:
                print("=========",location.name,"=========")
                location.describe()


    def add_agent(self,agent_config, n=1):
        #TODO: Agent paths should come frome the config file itself 
        agent_config = {"income":0.5, "prob":0.5,"home":"Bishan","dest": "Tuas","start_work_time": time(hour = 7, minute = 30),
                        "end_work_time": time(hour = 10, minute = 30)}
        start_loc = agent_config["home"]
        a = Agent(env = self,**agent_config)
        self.locmap[start_loc].add(a)
        return a


    def move_agent(self,agent,loc,new_loc):
        loc.remove(agent)
        new_loc.add(agent)
