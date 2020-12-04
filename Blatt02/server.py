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
                     "r": 0.3}
    elif type(agent) is ParticleAgent:
        if agent.particle_type is 'Leaf':
            portrayal = {"Shape": "circle",
                         "Color": "green",
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
                         "Color": "darkorange",
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
    ),
    "grid_height": 50,
    "grid_width": 50
}

grid = CanvasGrid(agent_portrayal, 50, 50, 800, 800)

chart_neighbors = ChartModule([{"Label": "Particles with neighbors percentage",
                                "Color": "Black"}],
                              data_collector_name='datacollector')

chart_entropy_particle_type = ChartModule([{"Label": "Entropy particles type",
                                            "Color": "Black"}],
                                          data_collector_name='datacollector')

chart_entropy_ants_laden = ChartModule([{"Label": "Entropy ants laden",
                                         "Color": "Black"}],
                                       data_collector_name='datacollector')

chart_entropy_particles = ChartModule([{"Label": "Entropy particles x",
                                        "Color": "Black"},
                                       {"Label": "Entropy particles y",
                                        "Color": "Gray"}],
                                      data_collector_name='datacollector')

chart_entropy_ants = ChartModule([{"Label": "Entropy ants x",
                                   "Color": "Black"},
                                  {"Label": "Entropy ants y",
                                   "Color": "Gray"}],
                                 data_collector_name='datacollector')

chart_emergence_particles = ChartModule([{"Label": "Emergence particles x",
                                          "Color": "Black"},
                                         {"Label": "Emergence particles y",
                                          "Color": "Gray"}],
                                        data_collector_name='datacollector')

chart_emergence_ants = ChartModule([{"Label": "Emergence ants x",
                                     "Color": "Black"},
                                    {"Label": "Emergence ants y",
                                     "Color": "Gray"}],
                                   data_collector_name='datacollector')

chart_emergence_particle_type = ChartModule(
    [{"Label": "Emergence particles type",
      "Color": "Black"}],
    data_collector_name='datacollector')

chart_emergence_ants_laden = ChartModule([{"Label": "Emergence ants laden",
                                           "Color": "Black"}],
                                         data_collector_name='datacollector')

server = ModularServer(AntModel,
                       [grid, chart_neighbors, chart_entropy_particle_type,
                        chart_entropy_ants_laden,
                        chart_entropy_particles, chart_entropy_ants,
                        chart_emergence_particles,
                        chart_emergence_ants, chart_emergence_particle_type,
                        chart_emergence_ants_laden],
                       "Ant Model", model_params=model_params)

server.port = 8521  # The default
server.launch()
