from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
)
import plotly.express as px
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from pcreations.client import (
    AirtableClient,
    get_token_from_file,
    create_date_range_formula
)

from pcreations.constants import base_id, table_id, orders_table_fields


DEBUG_MODE=True   # TODO: could go in constants...

# get a client object
client = AirtableClient(get_token_from_file(), base_id, table_id, fields=orders_table_fields)



# Set up the app layout
# TODO: This needs to be updates one we loads the fields from the client. The "avocado" object is a dataframe, so here we need something that can get the field names from the client
app = Dash()
#geo_dropdown = dcc.Dropdown(options=avocado['geography'].unique(),
#                            value='New York')

# What are the possible display options?
# They should at least include
# - total orders
# - total orders this month    (we should fetch with a filter for this option)
# - number of orders in progress
# - revenue
# - list of recent orders (default meaning of recent should be something like previous month)

dropdown_options = [
    "total orders",
    "total orders this month",
    "number of orders in progress",
    "revenue",
    "revenue by product",
    "recent orders"
]
pc_dropdown = dcc.Dropdown(options=dropdown_options, value=dropdown_options[0])

#geo_dropdown = dcc.Dropdown(options=client.get_fields(), value=client.get_fields()[0])
app.layout = html.Div(children=[
    html.H1(children='SOMETHING'),    # TODO: maybe I want one per soemthing?
    pc_dropdown,
    dcc.Graph(id="price_graph")
])


# Lets use the sample callback for now
@app.callback(
    Output(component_id="price_graph", component_property="figure"),
    Input(component_id=pc_dropdown, component_property="value")
)
def render_graph(dropdown_field):   # TODO: add filtering param?

    # TODO: as a stretch goal, how might we fetch only new data/only when new data is present?
    if dropdown_field == "total orders":
        graph_data = client.get_as_df(fields=["order_placed", "order_status", "price"])
        price_df = graph_data.groupby([graph_data["order_placed"]])["price"].sum()
        out_fig = px.bar(
            price_df,
            x="order_placed",
            y="price",
            title="Daily revenue"
        )
    elif dropdown_field == "total orders this month":
        time_now = datetime.now()
        time_then = time_now - relativedelta(months=1)
        date_range_formula = create_date_range_formula(time_then, time_now)

        graph_data = client.get_as_df(
            fields=["order_placed", "order_status", "price"],
            formula=date_range_formula
        )
        price_df = graph_data.groupby([graph_data["order_placed"]])["price"].sum()
        out_fig = px.bar(
            price_df,
            x="order_placed",
            y="price",
            title="Daily revenue"
        )

    elif dropdown_field == "revenue by product":
        graph_data = client.get_as_df(fields=["product_name", "price"])
        price_df = graph_data.groupby([graph_data["product_name"]])["price"].sum()
        out_fig = px.bar(
            price_df,
            x="product_name",
            y="price",
            title="Revenue per product"
        )

    else:
        # TODO: this needs to be error path
        graph_data = client.get_as_df(max_records=8, fields=[something, "order_placed"])
        out_fig = px.bar(
            graph_data,
            x=something,
            y="order_placed",
            title=f"ONE BILLION DOLLARS"
        )

    return out_fig





if __name__ == "__main__":
    app.run_server(debug=DEBUG_MODE)
