from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from model import AntModel
from agents import AntAgent, ParticleAgent


def agent_portrayal(agent):
    portrayal = {}

    if type(agent) is AntAgent:
        portrayal = {"Shape": "circle",
                     "Color": "red",
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.5}
    elif type(agent) is ParticleAgent:
        portrayal = {"Shape": "circle",
                     "Color": "gray",
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.3}

    return portrayal


grid = CanvasGrid(agent_portrayal, 50, 50, 700, 700)

chart1 = ChartModule([{"Label": "Particles with neighbors",
                      "Color": "Black"}],
                     data_collector_name='datacollector')

chart2 = ChartModule([{"Label": "Particles with neighbors percentage",
                      "Color": "Black"}],
                     data_collector_name='datacollector')

server = ModularServer(AntModel,
                       [grid, chart1, chart2],
                       "Ant Model",
                       {"N": 100, "particle_density": 0.2,
                        "step_size": 1, "jump_size": 3,
                        "all_in_center": False})

server.port = 8521  # The default
server.launch()
