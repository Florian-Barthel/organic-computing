import pandas as pd
import plotly.graph_objects as go
import numpy as np

file_name = 'population_ws2021.csv'

df = pd.read_csv(file_name)

grouped = df.groupby('action')
actions = grouped.groups.keys()

fig = go.Figure()

for action in actions:
    this_group = grouped.get_group(action)
    this_x = this_group['center_1']
    this_y = this_group['center_2']
    if action == 'white':
        action = 'gray'

    fig.add_trace(go.Scatter(x=this_x,
                             y=this_y,
                             mode="markers",
                             marker=dict(size=((1 - this_group['spread_1']) *
                                              10),
                                         color=action),
                             line_color=action))
    # fig.add_shape(type="circle", xref="x", yref="y",
    #               x0=min(this_x), y0=min(this_y),
    #               x1=max(this_x), y1=max(this_y),
    #               opacity=0.2, fillcolor=action, line_color=action)

fig.update_layout(showlegend=False, width=1000, height=1000)
fig.show()
