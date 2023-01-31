from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
)
import plotly.express as px

from pcreations.client import AirtableClient, get_token_from_file
from pcreations.constants import base_id, table_id, orders_table_fields


DEBUG_MODE=True   # TODO: could go in constants...

# get a client object
client = AirtableClient(get_token_from_file(), base_id, table_id, fields=orders_table_fields)



# Set up the app layout
# TODO: This needs to be updates one we loads the fields from the client. The "avocado" object is a dataframe, so here we need something that can get the field names from the client
app = Dash()
#geo_dropdown = dcc.Dropdown(options=avocado['geography'].unique(),
#                            value='New York')

geo_dropdown = dcc.Dropdown(options=client.get_fields(), value="ANYTHING")
app.layout = html.Div(children=[
    html.H1(children='SOMETHING'),    # TODO: maybe I want one per soemthing?
    geo_dropdown,
    dcc.Graph(id='price_graph')
])


# Lets use the sample callback for now 
@app.callback(
    Output(component_id="price_graph", component_property="figure"),
    Input(component_id=geo_dropdown, component_property="value")
)
def update_graph(something):   # TODO: add filtering param?
    filtered_graph = client.get(max_records=8)
    line_fig = px.line(
        filtered_graph,
        title=f"ONE BILLION DOLLARS"
    )

    return line_fig


if __name__ == "__main__":
    app.run_server(debug=DEBUG_MODE)
