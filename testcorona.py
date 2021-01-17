import numpy as np
import pandas as pd
import plotly.express as px
import folium
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def main():
    data = pd.read_csv('test.csv',skiprows = 7,sep=';')
    datamap = data.dropna(axis = 0)

    def createhisto() :
        datainf = data.drop({'Infections','Guerisons','TauxDeces','TauxGuerison', 'TauxInfection','Latitude','Longitude'},axis = 1)
        datainf['Date'] = pd.to_datetime(datainf['Date'], format='%d/%m/%Y')
        evolvinf = datainf.groupby(['Date']).mean()
        fig2 = px.histogram(evolvinf,x= evolvinf.index, y="Deces", log_y=True, labels=dict(couv= "Couverture de fibre"), nbins=evolvinf.index.size)
        return fig2

    def createmap() : 
        m = folium.Map(location=[31.7917,-7.0926],zoom_start=6, max_zoom=12,min_zoom=2)
        for i in range(0,len(datamap)):
            folium.CircleMarker(
                location = [datamap.iloc[i]['Latitude'],datamap.iloc[i]['Longitude']],
                radius = int(datamap.iloc[i]['Deces'])/5000,
                popup = datamap.iloc[i]['Pays'],
                color = 'red',
                fill_color ='indigo',
                tooltip = "<div style='margin: 0; background-color: black; color: white;'>"+
                        "<h4 style='text-align:center;font-weight: bold'>"+datamap.iloc[i]['Pays'] + "</h4>"
                        "<hr style='margin:10px;color: white;'>"+
                        "<ul style='color: white;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
                            "<li>Infecté: "+str(datamap.iloc[i]['Infections'])+"</li>"+
                            "<li>Deces:   "+str(datamap.iloc[i]['Deces'])+"</li>"+
                            "<li>Taux de mortalite: "+ str(datamap.iloc[i]['TauxDeces'])+ "</li>"+
                        "</ul></div>",
            ).add_to(m)
        return m
    
    
    #Using dash to create an html template

    histogramme = createhisto()
    location_map = createmap()
    location_map.save('Coronavirus_locations.html')

    app = dash.Dash(__name__)
    app.layout = html.Div(
                        children=[
                            html.H1(children=f'Somme du nombre de décés du corona par jours dans le monde',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)
                            html.Div(
				                children=[
					                dcc.Graph(id="example-graph-1", figure=histogramme, style = {"width": "100%"}),
					                html.Iframe(id = 'map', srcDoc= open('Coronavirus_locations.html').read(),width = '100%',height = '300')
				                ],
				            style =	{"display": "flex", "flex-direction": "row", "width": "95%"}
                            ),

                html.Div(
				    children=["Source DataGouv ",
					html.A("Lien de la database", href="https://www.data.gouv.fr/fr/datasets/coronavirus-covid19-evolution-par-pays-et-dans-le-monde-maj-quotidienne/")
				]
			),
    ]
    )
    #
    # RUN APP
    #
    app.run_server(debug=True)

if __name__ == "__main__":
    main()
