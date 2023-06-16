#run example dash
import dash
import dash_core_components as dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import xarray as xr

# Create synthetic example data
lon = np.linspace(-180, 180, 36)
lat = np.linspace(-90, 90, 18)
time = pd.date_range(start='2023-01-01', periods=10, freq='D')

observed_data = np.random.rand(len(time), len(lat), len(lon))
forecast_data = np.random.rand(len(time), len(lat), len(lon))
accuracy_data = np.random.rand(len(time), len(lat), len(lon))

# Create xarray datasets from the synthetic data
observed_dataset = xr.Dataset(
    {"rainfall": (["time", "lat", "lon"], observed_data)},
    coords={"time": time, "lat": lat, "lon": lon},
)

forecast_dataset = xr.Dataset(
    {"rainfall": (["time", "lat", "lon"], forecast_data)},
    coords={"time": time, "lat": lat, "lon": lon},
)

accuracy_dataset = xr.Dataset(
    {"accuracy": (["time", "lat", "lon"], accuracy_data)},
    coords={"time": time, "lat": lat, "lon": lon},
)

# Create the Dash application
app = dash.Dash(__name__)
sever = app.server
#app = JupyterDash(__name__)

# Define the layout of the application
app.layout = html.Div([
    html.H1("Rainfall Analysis"),
    dcc.Graph(id="rainfall-plot"),
    dcc.Slider(
        id="date-slider",
        min=0,
        max=len(observed_dataset["time"]) - 1,
        step=1,
        value=0,
        marks={str(i): str(observed_dataset["time"][i].values) for i in range(len(observed_dataset["time"]))},
    )
])

# Define the callback function to update the plot based on the selected date
@app.callback(
    Output("rainfall-plot", "figure"),
    [Input("date-slider", "value")]
)
def update_rainfall_plot(selected_date):
    # Extract the observed, forecast, and accuracy data for the selected date
    observed_data = observed_dataset["rainfall"].sel(time=observed_dataset["time"][selected_date])
    forecast_data = forecast_dataset["rainfall"].sel(time=forecast_dataset["time"][selected_date])
    accuracy_data = accuracy_dataset["accuracy"].sel(time=accuracy_dataset["time"][selected_date])

    # Create the plot using Plotly Graph Objects
    fig = go.Figure()

    # Add observed data
    fig.add_trace(go.Contour(
        x=observed_data["lon"],
        y=observed_data["lat"],
        z=observed_data,
        colorscale="Blues",
        colorbar=dict(title="Observed Rainfall")
    ))

    # Add forecast data
    fig.add_trace(go.Contour(
        x=forecast_data["lon"],
        y=forecast_data["lat"],
        z=forecast_data,
        colorscale="Reds",
        colorbar=dict(title="Forecast Rainfall")
    ))

    # Add accuracy metrics
    fig.add_trace(go.Contour(
        x=accuracy_data["lon"],
        y=accuracy_data["lat"],
        z=accuracy_data,
        colorscale="Greens",
        colorbar=dict(title="Accuracy Metrics")
    ))

    fig.update_layout(
        title="Rainfall Analysis on {}".format(observed_dataset["time"][selected_date].values),
        xaxis_title="Longitude",
        yaxis_title="Latitude")

    return fig

# Run the application


if __name__ == '__main__':
    app.run_server(debug=False)
    #app.run_server(mode="inline")
    #app.run_server(mode="inline", port=8050)
    #app.server.run(port=8000, host='127.0.0.1')
