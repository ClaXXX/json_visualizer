# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import logging
from dash import Dash, html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State

from graph.json import JsonGraph

logging.basicConfig(level=logging.DEBUG)
app = Dash(__name__)

# Style

default_stylesheet = [
    {
        "selector": 'node',
        'style': {
            "opacity": 0.65,
            'z-index': 9999
        }
    },
    {
        "selector": 'edge',
        'style': {
            "curve-style": "bezier",
            "opacity": 0.45,
            'z-index': 5000
        }
    },
    {
        'selector': '.followerNode',
        'style': {
            'background-color': '#0074D9'
        }
    },
    {
        'selector': '.followerEdge',
        "style": {
            "mid-target-arrow-color": "blue",
            "mid-target-arrow-shape": "vee",
            "line-color": "#0074D9"
        }
    },
    {
        'selector': '.followingNode',
        'style': {
            'background-color': '#FF4136'
        }
    },
    {
        'selector': '.followingEdge',
        "style": {
            "mid-target-arrow-color": "red",
            "mid-target-arrow-shape": "vee",
            "line-color": "#FF4136",
        }
    },
    {
        "selector": '.genesis',
        "style": {
            'background-color': '#B10DC9',
            "border-width": 2,
            "border-color": "purple",
            "border-opacity": 1,
            "opacity": 1,

            "label": "data(label)",
            "color": "#B10DC9",
            "text-opacity": 1,
            "font-size": 12,
            'z-index': 9999
        }
    },
    {
        'selector': ':selected',
        "style": {
            "border-width": 2,
            "border-color": "black",
            "border-opacity": 1,
            "opacity": 1,
            "label": "data(label)",
            "color": "black",
            "font-size": 12,
            'z-index': 9999
        }
    }
]

graph = JsonGraph.from_file("rsc/sample.json")

# Layout
app.layout = html.Div(children=[
    html.H1(children='Graph Vizualizer'),

    html.Div(children='''
        Vizualise and manipulate json graph.
    '''),

    cyto.Cytoscape(
        id='cytoscape',
        elements=graph.get(),
        layout={'name': 'preset'},
        stylesheet=default_stylesheet,
        style={
            'height': '95vh',
            'width': '100%'
        }
    )
])


"""
@app.callback(Output('cytoscape', 'elements'),
              [Input('cytoscape', 'tapNodeData')],
              [State('cytoscape', 'elements'),
               State('radio-expand', 'value')])
def generate_elements(nodeData, elements, expansion_mode):
    if not nodeData:
        return graph

    # If the node has already been expanded, we don't expand it again
    if nodeData.get('expanded'):
        return elements

    # This retrieves the currently selected element, and tag it as expanded
    for element in elements:
        if nodeData['id'] == element.get('data').get('id'):
            element['data']['expanded'] = True
            break

    if expansion_mode == 'followers':

        followers_nodes = followers_node_di.get(nodeData['id'])
        followers_edges = followers_edges_di.get(nodeData['id'])

        if followers_nodes:
            for node in followers_nodes:
                node['classes'] = 'followerNode'
            elements.extend(followers_nodes)

        if followers_edges:
            for follower_edge in followers_edges:
                follower_edge['classes'] = 'followerEdge'
            elements.extend(followers_edges)

    elif expansion_mode == 'following':

        following_nodes = following_node_di.get(nodeData['id'])
        following_edges = following_edges_di.get(nodeData['id'])

        if following_nodes:
            for node in following_nodes:
                if node['data']['id'] != genesis_node['data']['id']:
                    node['classes'] = 'followingNode'
                    elements.append(node)

        if following_edges:
            for follower_edge in following_edges:
                follower_edge['classes'] = 'followingEdge'
            elements.extend(following_edges)

    return elements
"""

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
