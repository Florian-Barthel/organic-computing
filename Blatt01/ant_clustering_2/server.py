from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import AntClustering
from .agent import Ant, Particle


def agent_portrayal(agent):
    if agent is None:
        return
    portrayal = {}
    if isinstance(agent, Ant):
        portrayal = {"Shape": "rect", "w": .8, "h": .8, "Color": "Red", "Filled": "true", "Layer": 0}
    if isinstance(agent, Particle) and agent.type == 'Leaf':
        portrayal = {"Shape": "circle", "r": .4, "Color": "Green", "Filled": "true", "Layer": 1}
    if isinstance(agent, Particle) and agent.type == 'Nut':
        portrayal = {"Shape": "circle", "r": .2, "Color": "Brown", "Filled": "true", "Layer": 1}
    if isinstance(agent, Particle) and agent.type == 'Pebble':
        portrayal = {"Shape": "circle", "r": .3, "Color": "Grey", "Filled": "true", "Layer": 1}
    return portrayal


# dictionary of user settable parameters - these map to the model __init__ parameters
model_params = {
    "height": 50,
    "width": 50,
    "ants": UserSettableParameter("slider", "Number of ants", value=100, min_value=1, max_value=1000, step=1),
    "density": UserSettableParameter("slider", "Object density", value=0.22, min_value=0.01, max_value=1.0, step=.01),
    "s": UserSettableParameter("slider", "Ant step size", value=1, min_value=1, max_value=5, step=1),
    "j": UserSettableParameter("slider", "Ant jump distance", value=5, min_value=1, max_value=10, step=1),
    "distribution": UserSettableParameter("choice", "Initial distribution of ants", value="random", choices=["random",
                                                                                                             "center"])
}

# set the portrayal function and size of the canvas for visualization
canvas_element = CanvasGrid(agent_portrayal, 50, 50, 500, 500)

# create instance of Mesa ModularServer
server = ModularServer(
    AntClustering, [canvas_element], "Ant Clustering", model_params
)

