import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import requests
import certifi
from geopy.geocoders import Nominatim
from folium import plugins
import folium
from flask import Flask, render_template, request
from fastapi.templating import Jinja2Templates



# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py
def search(user):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': user, 'count': '200'})
    print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    with open("oleg.json", 'w') as file:
        json.dump(js, file, indent=4)

    data = js['users']
    result_info = []
    for element in data:
        result = (element["screen_name"], element['location'])
        result_info.append(result)
    lst = []
    for elements in result_info:
        lst.append(list(elements))
    for element in lst:
        geo_location = element[-1]
        if len(geo_location) == 0:
            lst.remove(element)
        else:
            try:
                geolocator = Nominatim(user_agent='My map')
                geo_loc = geo_location
                location = geolocator.geocode(geo_loc)
                coordinates = (location.latitude, location.longitude)
                element.append(coordinates)
            except:
                geolocator = Nominatim(user_agent='My map')
                geo_loc = geo_location.split(',')[0]
                try:
                    location = geolocator.geocode(geo_loc)
                    coordinates = (location.latitude, location.longitude)
                    element.append(coordinates)
                except AttributeError:
                    lst.remove(element)
    final_lst = []
    for item in lst:
        if len(item) == 3:
            final_lst.append(item)
    map = folium.Map(tiles="Stamen Terrain", location=[48.8566, 2.3522], control_scale=True)
    fg = folium.FeatureGroup(name="user's friends locations")
    for pair in final_lst:
        latitude = pair[-1][0]
        longitude = pair[-1][1]
        nickname = pair[0]
        fg.add_child(
            folium.Marker(location=[latitude, longitude], popup=nickname, icon=folium.Icon(icon='nickname', color="pink")))
    map.add_child(fg)
    plugins.ScrollZoomToggler().add_to(map)
    plugins.Fullscreen(position="topright").add_to(map)
    map.add_child(folium.LayerControl())
    map.save('templates/my_map3.html')
    return True
