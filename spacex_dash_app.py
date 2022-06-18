# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
#print(spacex_df.info)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                        options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            ],
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                        ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',min=0 , max =16000 , step = 2000, value=[0,16000])),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    print(entered_site)
    filtered_df = spacex_df
    if entered_site == 'ALL':
        df1 = filtered_df[filtered_df['class'] == 1].groupby(['Launch Site']).size().reset_index(name='counts')
        #print(df1.head())
        fig = px.pie(df1, values='counts', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        df2 = filtered_df[filtered_df['Launch Site'] == entered_site].groupby(['class']).size().reset_index(name='counts')
        #print(df2.head())
        fig = px.pie(df2, values='counts', 
        names='class', 
        title='Success and Failure Launches for site ' + entered_site )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')
              ])
  
def get_scatter_chart(entered_site, slider_val):
    filtered_df = spacex_df
    if entered_site == 'ALL':        
        df3 = filtered_df
        #print(df3)
    else:
        df3 = filtered_df[filtered_df['Launch Site'] == entered_site]
        #print(df3)
    df4 = df3[df3['Payload Mass (kg)'] >= slider_val[0]]
    df5 = df4[df4['Payload Mass (kg)'] <= slider_val[1]]
    fig = px.scatter(df5, x='Payload Mass (kg)', y='class',
        title='Success vs Payload Mass for site ' + entered_site )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
