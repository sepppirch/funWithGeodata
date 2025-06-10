import plotly.express as px
import plotly.io as pio
import plotly.offline as pyo
# Set notebook mode to work in offline
#pyo.init_notebook_mode()

import pandas as pd

'''
gps_data = "gps.csv"
gps_df = pd.read_csv(gps_data)
gps_df

api_token = 'pk.eyJ1Ijoic2ViYXN0aWFuMTMzNyIsImEiOiJjbG02OW9ycTQwOXlyM2Vtdnc3c3AzdGgxIn0.3FWF229mk_k4gj7PMjm78g'

fig = px.scatter_mapbox(gps_df, lat="Lat", lon="Long", 
                  #color_continuous_scale=["black", "purple", "red" ], size_max=30, zoom=12.5,
                  height = 512, width = 512, #center = dict(lat = g.center)
                        #title='Drive Route with Mapbox',
                       #mapbox_style="open-street-map"
                       )
fig.update_layout(font_size=16,  title={'xanchor': 'center','yanchor': 'top', 'y':0, 'x':0,}, 
        title_font_size = 24, mapbox_accesstoken=api_token, mapbox_style = "mapbox://styles/strym/ckhd00st61aum19noz9h8y8kw")
fig.update_traces(marker=dict(size=6))
fig.show()
#fig.write_image('gps.png')

fig=px.choropleth(gps_df,
             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
             featureidkey='properties.ST_NM',   
             #locations='Area_Name',        #column in dataframe
              #animation_frame='Year',       #dataframe
              #color='Rape_Cases_Reported',  #dataframe
              color_continuous_scale='Inferno',
               title='Rape cases across the states' ,  
               height=700
              )
fig.update_geos(fitbounds="locations", visible=False)
fig.show()'''

import geopandas as gpd
import plotly.express as px
import json
geojson = {
"type": "FeatureCollection",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::4283" } },
"features": [
{ "type": "Feature", "properties": { "OBJECTID": 2282, "SORT_GBR_I": "20039", "LABEL_ID": "20-039", "SUB_NO": 100, "CODE": "20-039-100-106", "UNIQUE_ID": "20039100106", "FEATURE_C": 106, "GBR_NAME": "Hill Rock", "FEAT_NAME": "Rock", "QLD_NAME": "Hill Rock", "X_LABEL": "20-039S", "GBR_ID": "20039", "LOC_NAME_S": "Hill Rock (20-039)", "LOC_NAME_L": "Hill Rock (20-039)", "X_COORD": 148.90635681000001, "Y_COORD": -20.25865936, "Area_HA": 0.0, "GlobalID": "{6CFEA6F6-33A2-444A-835B-0003206EBA49}", "Shape_STAr": 14139.6796875, "Shape_STLe": 471.01884611600002 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 148.90694393116658, -20.259096202918855 ], [ 148.906921432860258, -20.259141198606248 ], [ 148.906754946292011, -20.259253691138628 ], [ 148.906687452271484, -20.259253691138628 ], [ 148.906655954642673, -20.259244690660317 ], [ 148.906619957352575, -20.259235691867001 ], [ 148.906570461078786, -20.259231191627361 ], [ 148.90651646604195, -20.259222192833235 ], [ 148.906302341814211, -20.259159602404967 ], [ 148.906223988958516, -20.259136699206643 ], [ 148.906196990990964, -20.259132199806906 ], [ 148.906156494039664, -20.259123201007046 ], [ 148.906124997309178, -20.259118700764201 ], [ 148.905985260773463, -20.259177555334624 ], [ 148.905936012434609, -20.259145698848446 ], [ 148.905900015144567, -20.259114202206661 ], [ 148.905882015601208, -20.259078205314452 ], [ 148.905873017177015, -20.259037707325927 ], [ 148.905864017854498, -20.258997211012321 ], [ 148.905859518193239, -20.258961213250245 ], [ 148.905850518870693, -20.258925217165245 ], [ 148.905850517972397, -20.258884719979569 ], [ 148.905850518870693, -20.258844222783306 ], [ 148.905854417559027, -20.25880628498949 ], [ 148.905859518193239, -20.25878122768551 ], [ 148.905859518193239, -20.258736231893799 ], [ 148.905850517972397, -20.258682236420832 ], [ 148.905859518193239, -20.258655238255969 ], [ 148.905850518870693, -20.258619241257328 ], [ 148.905850517972397, -20.258592243081473 ], [ 148.905850518870693, -20.258551745808919 ], [ 148.905864016956144, -20.258506749950669 ], [ 148.905868516617403, -20.258470752917578 ], [ 148.90586851841411, -20.258434755876166 ], [ 148.905873017177015, -20.258380760298351 ], [ 148.90588651616082, -20.258326764701771 ], [ 148.905891014923725, -20.25828626820272 ], [ 148.905900014246271, -20.25825476970104 ], [ 148.905904514805826, -20.258218772609524 ], [ 148.905922512552536, -20.25818277635242 ], [ 148.905922512552536, -20.258146779244225 ], [ 148.905998580094177, -20.258045355404413 ], [ 148.906057503288594, -20.257966792735232 ], [ 148.906106997765789, -20.257926296984994 ], [ 148.906165494260449, -20.257912796994663 ], [ 148.906205990313481, -20.257921796707411 ], [ 148.906232988281033, -20.257935295854242 ], [ 148.906273485232333, -20.257948794999852 ], [ 148.906295982640302, -20.257966792735221 ], [ 148.906462470106902, -20.258097282996108 ], [ 148.906493967735656, -20.258119780986227 ], [ 148.906516465143653, -20.258151278672489 ], [ 148.906547962772464, -20.258191775206793 ], [ 148.906570461977083, -20.258218772609524 ], [ 148.90659295938508, -20.258259269968963 ], [ 148.906624457013834, -20.258304265898925 ], [ 148.906646955320156, -20.258349262658626 ], [ 148.906750446630753, -20.258515749629034 ], [ 148.906790942683756, -20.258542746975422 ], [ 148.906831439635141, -20.258556246068217 ], [ 148.906871936586413, -20.258560746327401 ], [ 148.906898934553993, -20.258574243733147 ], [ 148.906943932064848, -20.258601242754846 ], [ 148.9069546902887, -20.258654134260489 ], [ 148.906948430827839, -20.258713733993034 ], [ 148.906934931844063, -20.258740732147746 ], [ 148.90692593341987, -20.258961214092974 ], [ 148.90694393116658, -20.259010710065613 ], [ 148.906948430827839, -20.259064706267022 ], [ 148.90694393116658, -20.259096202918855 ] ] ] } }] 
}
geojson = gpd.read_file('power1.geojson')
gdf = gpd.GeoDataFrame.from_features(geojson)
point = (148.90635, -20.25866)

LeftTop = [47.48802456352513, 13.233287974359211]
width = 0.1096
height =0.16

fig = px.scatter_mapbox(lat=[LeftTop[1]], lon=[LeftTop[0]]).update_layout(
        mapbox={
            "style": "open-street-map",
            #"zoom": 16,
            "layers": [
                {
                    "source": json.loads(gdf.geometry.to_json()),
                    "below": "traces",
                    "type": "line",
                    "color": "purple",
                    "line": {"width": 1.5},
                }
            ],
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

fig.update_mapboxes(bounds_west=LeftTop[1], bounds_east=LeftTop[1] - width, bounds_north=LeftTop[0],bounds_south=LeftTop[0]+height)
#fig.update_mapboxes(style='white-bg',
#                    center={'lat':47.422505931257994, 'lon':   13.388575949584213},
#                    zoom=16)
fig.show()