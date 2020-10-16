import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from datetime import timedelta, date, time,datetime
from shapely.geometry import Polygon,LineString
from math import sqrt
from IPython.display import HTML
from numpy.linalg import norm 
from matplotlib import animation
from matplotlib.widgets import Slider, Button, RadioButtons
from utils import parse_log

def load_data():
    df = pd.read_csv("logs/data.csv",index_col = 0)
    df.index = pd.to_datetime(df.index)
    locations = [loc for loc in df.columns if ">" not in loc]
    transit_locs = [loc for loc in df.columns if ">" in loc ]
    region_shp = "assets/plan-shp/MP14_PLNG_AREA_NO_SEA_PL.shp"
    region_map = gpd.read_file(region_shp)
    region_map["coords"] = region_map["geometry"].apply(lambda x:x.representative_point().coords[0])
    to_remove = [17,40,44,46,48]
    # region_map.drop(to_remove,inplace = True)
    my_map = region_map.copy()
    #Insert all change to my_map here
    df = pd.read_csv("data/locations_data.csv")
    my_map = region_map.copy()
    to_remove = [17,40,44,46,48]
    water_regions = [27,49]
    water_regions = my_map.iloc[water_regions]
    my_map.drop(to_remove,inplace = True)
    loc_map = ["Bishan","Paya Lebar","Bishan","Jurong","CCK","CBD","CCK","Buona","Paya Lebar","Town","Toa Payoh","Tampines","Serangoon","Jurong","CCK","Woodlands",
    "Paya Lebar","Tuas","Jurong","Paya Lebar","Punggol","Tiong Bahru","Punggol","Woodlands","Punggol","Serangoon","Bishan","Tampines","Woodlands","Tampines","CBD",
    "Town","CCK","Toa Payoh","Paya Lebar","Woodlands","CBD","CBD","Town","CCK","Buona","CBD","Woodlands","Tuas","CCK","Woodlands","Town","CBD","Town","Town"]
    my_map["location"] = loc_map
    my_map2 = my_map.dissolve(by="location").reset_index()
    # my_map2 = my_map2.merge(df,on = "location")
    my_map2["coords"] = my_map2["geometry"].apply(lambda x:(x.representative_point().x,x.representative_point().y))
    pd.set_option('mode.chained_assignment', None)
    map_df = my_map2.merge(df,on = "location")
    map_df["total_home"] = map_df["people_home"] + map_df["student_home"]
    map_df = map_df[["location","geometry","total_home","coords"]]

    map_df["text_coords"] = map_df["coords"]
    map_df["text_coords"] = map_df["text_coords"].apply(lambda x: np.array(x))
    #map_df["coords"] = map_df["coords"].apply(lambda x: np.array(x))
    # Adjusting Coordinates of the Text for Visualisation
    map_df["text_coords"][0] = map_df["text_coords"][0] + np.array([-2000,0])
    map_df["text_coords"][1] = map_df["text_coords"][1] + np.array([0,1500])
    map_df["text_coords"][2] = map_df["text_coords"][2] + np.array([-500,0])
    map_df["text_coords"][3] = map_df["text_coords"][3] + np.array([0,1000])
    map_df["text_coords"][4] = map_df["text_coords"][4] + np.array([500,-1000])
    map_df["text_coords"][5] = map_df["text_coords"][5] + np.array([0,-2000]) #Paya Lebar
    map_df["text_coords"][6] = map_df["text_coords"][6] + np.array([0,100])
    #map_df["text_coords"][7] = map_df["text_coords"][7] + np.array([0,-1000]) #Serangoon
    map_df["text_coords"][8] = map_df["text_coords"][8] + np.array([0,-1000])
    map_df["text_coords"][9] = map_df["text_coords"][9] + np.array([0,-100]) #Tiong Bahru
    map_df["text_coords"][10] = map_df["text_coords"][10] + np.array([3500,750]) #Toa Payoh
    map_df["text_coords"][11] = map_df["text_coords"][11] + np.array([3750,0]) #Town
    map_df["text_coords"][12] = map_df["text_coords"][12] + np.array([1000,4300]) #Tuas
    map_df["text_coords"][13] = map_df["text_coords"][13] + np.array([0,400]) #Woodlands

    # Adjusting Coordinates of the Transport Center 
    #map_df["coords"][9] = map_df["coords"][9] + np.array([0,1000])
    map_df["coords"][11] = map_df["coords"][11] + np.array([750,0])
    map_df["coords"][12] = np.array([9000,34000])

    map_df["coords"] = map_df["coords"].apply(lambda x: tuple(x))
    pd.set_option('mode.chained_assignment', 'raise')
    data_df = pd.read_csv("logs/data.csv",index_col = 0)
    data_df.index = pd.to_datetime(data_df.index)
    locations = [loc for loc in data_df.columns if ">" not in loc]
    transit_locs = [loc for loc in data_df.columns if ">" in loc ]
    loc_data = data_df[locations].T
    loc_data.reset_index(inplace = True)
    loc_data.columns = ["location"] + list(loc_data.columns[1:])
    trans_data = data_df[transit_locs].T
    trans_data.reset_index(inplace = True)
    trans_data.columns = ["location"] + list(trans_data.columns[1:])
    width = 300
    geoms = []
    for i,v in enumerate(transit_locs):
        loc1,loc2 = v.split("->")
        c1 = np.array(map_df[map_df["location"] == loc1]["coords"].iloc[0])
        c2 = np.array(map_df[map_df["location"] == loc2]["coords"].iloc[0])
        #Vector from 1 to 2 
        v = c2 - c1
        n1 = np.array((-v[1],v[0]))
        n1 = n1/norm(n1)*width
        if i%2:
            coords = [c1+n1,c1,c2,c2+n1]
            poly = Polygon(coords)
        else:
            coords = [c1+(1.5*n1),c1+(2.5*n1),c2+(2.5*n1),c2+(1.5*n1)]
            poly = Polygon(coords)
        geoms.append(poly)
    trans_df = pd.DataFrame({"location":transit_locs,"geometry":geoms})
    trans_df = gpd.GeoDataFrame(trans_df)
    trans_df = trans_df.merge(trans_data,on = "location")
    trans_df.columns = [str(i) for i in trans_df.columns]
    map_df = map_df.merge(loc_data,on = "location")
    map_df.columns = [str(i) for i in map_df.columns]
    return map_df,trans_df
def create_slider_plot1(map_df,trans_df):
    fig,ax = plt.subplots(figsize=(15,15))
    plt.subplots_adjust(left=0.25, bottom=0.25)
    timings = map_df.columns[5:]

    map_df.plot(ax = ax, edgecolor = 'black',legend = True,column = timings[0],cmap = "PuBu")
    trans_df.plot(ax = ax, legend = True,column = timings[0],cmap = "Reds",vmin = 0,vmax = 1000)

    axcolor = 'lightgoldenrodyellow'
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)    
    stime = Slider(axfreq, 'Time', 0, len(timings)-1, valinit=0, valstep=1)

    def update(val):
        time_index = stime.val
        time = timings[time_index]
        map_df.plot(ax = ax, edgecolor = 'black',column = time,cmap = "PuBu")
        trans_df.plot(ax = ax,column = time,cmap = "Reds")
        fig.canvas.draw_idle()

    stime.on_changed(update)
    plt.show()
def create_animation(map_df,trans_df):
    fig,ax = plt.subplots(figsize=(15,15))
    #plt.subplots_adjust(left=0.25, bottom=0.25)
    timings = map_df.columns[5:]
    ims = []
    im = map_df.plot(ax = ax, edgecolor = 'black',legend = True,column = timings[0],cmap = "PuBu",vmin = -200,vmax = 2000)
    im = trans_df.plot(ax = ax, legend = True,column = timings[0],cmap = "Reds",vmin = -100,vmax = 700)
    for i,time in enumerate(timings):
        im = map_df.plot(ax = ax, edgecolor = 'black',legend = True,column = time,cmap = "PuBu",vmin = -200,vmax = 2000,animated = True)
        im = trans_df.plot(ax = ax, legend = True,column = time,cmap = "Reds",vmin = -100,vmax = 700,animated = True)
        fig.canvas.draw_idle()
        ims.append([fig])
        plt.clf()



    ani = ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=1000)
    plt.show()
def create_animation2(map_df,trans_df):
    fig,ax = plt.subplots(figsize=(15,15))
    #plt.subplots_adjust(left=0.25, bottom=0.25)
    timings = map_df.columns[5:]
    #print(timings)

    def init():
        map_df.plot(ax = ax, edgecolor = 'black',legend = True,column = timings[0],cmap = "PuBu",vmin = -200,vmax = 2000,
                    legend_kwds={'shrink': 0.7})
        trans_df.plot(ax = ax, legend = True,column = timings[0],cmap = "Reds",vmin = -100,vmax = 700,legend_kwds={'shrink': 0.7})

    def animate(i):
        time = timings[i]
        map_df.plot(ax= ax,edgecolor = 'black',column = time,cmap = "PuBu",vmin = -200,vmax = 2000,legend_kwds={'shrink': 0.7})
        trans_df.plot(ax= ax,column = time,cmap = "Reds",vmin = -100,vmax = 700,legend_kwds={'shrink': 0.7})
        plt.title(time[11:])
        print(time)
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(timings), repeat = False,interval = 200)
    with open("assets/videos/baseline.html", "w") as f:
        print(ani.to_html5_video(), file=f)





if __name__ == "__main__":
    map_df,trans_df = load_data()
    #print(map_df.columns)
    start_time = 5
    end_time = int(start_time + 60*17/5)
    map_day = map_df.iloc[:,:end_time]
    trans_day = trans_df.iloc[:,:end_time]
    create_animation2(map_day,trans_day)
    #create_slider_plot1(map_day,trans_day) 