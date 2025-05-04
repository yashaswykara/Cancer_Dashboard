import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from dash.dependencies import State

# Load the detailed data
df = pd.read_csv('data/cancer_detailed_data.csv')

# Create app
app = Dash(__name__, suppress_callback_exceptions=True)

app.title = "Cancer Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Cancer Dashboard (2013 - 2023)", className='header'),

    html.Div([
        html.Label("Select Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
            value='USA',
            className='dropdown'
        ),
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
            value=2023,
            className='dropdown'
        )
    ], className='selectors'),

    html.Div([
        dcc.Graph(id='cancer-type-graph'),
        dcc.Graph(id='cancer-pie-chart')
    ])
])

# Callback to update both bar chart and pie chart
@app.callback(
    [Output('cancer-type-graph', 'figure'),
     Output('cancer-pie-chart', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_graph(selected_country, selected_year):
    # Filter data based on selection
    filtered_df = df[(df['Country'] == selected_country) & (df['Year'] == selected_year)]
    
    # Create Bar chart
    bar_fig = px.bar(
        filtered_df,
        x='CancerType',
        y='Cases',
        title=f"Cancer Types in {selected_country} ({selected_year})",
        labels={'CancerType': 'Cancer Type', 'Cases': 'Number of Cases'},
        color='CancerType',
        text='Cases'
    )
    bar_fig.update_layout(xaxis_title='', yaxis_title='Cases', title_x=0.5)

    # Create Pie chart
    pie_fig = px.pie(
        filtered_df,
        names='CancerType',
        values='Cases',
        title=f"Cancer Distribution in {selected_country} ({selected_year})",
        color='CancerType'
    )
    
    return bar_fig, pie_fig

if __name__ == '__main__':
    app.run(debug=True)
