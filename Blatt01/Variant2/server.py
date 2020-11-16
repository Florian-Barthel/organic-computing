from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from model import AntModel
from agents import AntAgent, ParticleAgent


def agent_portrayal(agent):
    portrayal = {}

    if type(agent) is AntAgent:
        portrayal = {"Shape": "circle",
                     "Color": "red",
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.2}
    elif type(agent) is ParticleAgent:
        if agent.particle_type is 'Leaf':
            portrayal = {"Shape": "circle",
                         "Color": "darkgreen",
                         "Filled": "true",
                         "Layer": 0,
                         "r": 0.6}
        elif agent.particle_type is 'Stone':
            portrayal = {"Shape": "circle",
                         "Color": "gray",
                         "Filled": "true",
                         "Layer": 0,
                         "r": 0.6}
        elif agent.particle_type is 'Nut':
            portrayal = {"Shape": "circle",
                         "Color": "brown",
                         "Filled": "true",
                         "Layer": 0,
                         "r": 0.6}

    return portrayal


model_params = {
    "num_ants": UserSettableParameter(
        "slider",
        "Number of Ants",
        value=100,
        min_value=1,
        max_value=200,
        step=1
    ),
    "particle_density": UserSettableParameter(
        "slider",
        "Particle Density",
        value=0.15,
        min_value=0.0,
        max_value=1.0,
        step=0.01
    ),
    "step_size": UserSettableParameter(
        "slider",
        "Ant Step Size",
        value=5,
        min_value=1,
        max_value=10,
        step=1
    ),
    "all_in_center": UserSettableParameter(
        "choice",
        "All in center",
        value='No',
        choices=['Yes', 'No']
    )
}

grid = CanvasGrid(agent_portrayal, 50, 50, 800, 800)

chart1 = ChartModule([{"Label": "Particles with neighbors",
                      "Color": "Black"}],
                     data_collector_name='datacollector')

chart2 = ChartModule([{"Label": "Particles with neighbors percentage",
                      "Color": "Black"}],
                     data_collector_name='datacollector')

server = ModularServer(AntModel,
                       [grid, chart2],
                       "Ant Model", model_params=model_params)

server.port = 8521  # The default
server.launch()
