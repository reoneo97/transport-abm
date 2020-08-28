from env.env import *
from agents import *


if __name__ == "__main__":
    hi = Graph()
    #hi.add_edge("Paya Lebar","Woodlands",5)
    pl = Location("Paya Lebar")
    wl = Location("Woodlands")
    hi.add_edge(pl,wl,5)
    print(hi)