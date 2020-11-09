from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import (
    CanvasGrid
)
from mesa.visualization.UserParam import UserSettableParameter
from blatt1.ants.agents import AntAgent, ParticleAgent
from blatt1.ants.model import AntModel


def agent_portrayal(agent):
    if agent is None:
        return
    portrayal = {}
    if isinstance(agent, AntAgent):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1.0
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"
        portrayal["Color"] = "#FF3333"

    if isinstance(agent, ParticleAgent):
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.3
        portrayal["h"] = 0.3
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        portrayal["Color"] = "#333333"
    return portrayal


# dictionary of user settable parameters - these map to the model __init__ parameters
model_params = {
    "num_ants": UserSettableParameter(
        "slider",
        "Number of Ants",
        value=10,
        min_value=1,
        max_value=100,
        step=1
    ),
    "density": UserSettableParameter(
        "slider",
        "Particle Density",
        value=0.1,
        min_value=0.0,
        max_value=1.0,
        step=0.01
    ),
    "step_size": UserSettableParameter(
        "slider",
        "Ant Step Size",
        value=1,
        min_value=1,
        max_value=10,
        step=1
    ),
    "jump_size": UserSettableParameter(
        "slider",
        "Ant Jump Size",
        value=2,
        min_value=1,
        max_value=10,
        step=1
    ),
    "width": 50,
    "height": 50,
    "init_dist": UserSettableParameter(
        "choice",
        "Initial Distribution",
        value='random',
        choices=['random', 'center']
    )
}

# set the portrayal function and size of the canvas for visualization
canvas_element = CanvasGrid(agent_portrayal, 50, 50, 700, 700)

# create instance of Mesa ModularServer
server = ModularServer(
    AntModel,
    [canvas_element],
    "Ant Simulation",
    model_params=model_params,
)
