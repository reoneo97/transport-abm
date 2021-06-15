# transport-abm
Project using an Agent-based Modelling approach to analyse traffic congestion in Singapore. Agent-based modelling is a modelling approach where different agents interact with each other in a simulated environment in an attempt to model real-world behaviour.

In this model, there are two types of agents:
1. Working Adults
2. Students

The environment is modelled as a weighted undirected graph where the nodes are planning areas around Singapore and the edges are the travel time between the different nodes.

Each agent has a `home_location` and a `work_location` and they travel to and from work/school everyday. By using census data about where citizens live and work, we construct a simulated environment in which we can study how minor traffic disruptions can snowball and affect lots of people. This project also allows us to propose possible solutions and study their effectiveness when used in this simulated model

## Demo

<figure class="video_container">
  <video controls="true" allowfullscreen="true" poster="assets/poster.png">
    <source src="./assets/base.mp4" type="video/mp4">
  </video>
</figure>

<figure class="video_container">
  <video controls="true" allowfullscreen="true" poster="assets/poster.png">
    <source src="[assets/base.mp4](https://user-images.githubusercontent.com/52419450/122032160-f5428a80-ce01-11eb-832c-1a5f2d7a89ca.mp4)" type="video/mp4">
  </video>
</figure>


## Data
The `./data` folder contains many `.csv` files which controls the set up of the environment. 
- `locations.csv` - `.csv` file which shows the different nodes and distances between them 
  
## Simulation

Using `main.py` there are several simulations that can be used

Each simulation will create an entry in the `logs/` directory which is `stdout` from all the print statements when performing the simulation. `utils.parse_log` is then used to read the log files and create a .csv file to display the number of people at each location at every timestep

## Visualisation

Visualisations were obtained using Geopandas and [publicly available shapefiles](https://storage.data.gov.sg/master-plan-2019-planning-area-boundary-no-sea/master-plan-2019-planning-area-boundary-no-sea.zip) to create the heatmap animations

### File Structure

```bash
├───agents
├───assets
│   └───plan-shp
├───data
├───env
├───logs
```