# import the library
import folium
import webbrowser
list = dict()

print(list["vege"])
# Make an empty map
m = folium.Map(location=[20, 0], zoom_start=3.5)
folium.Map()

# Other tiles:
# OpenStreetMap, Stamen Terrain, Stamen Toner, Mapbox Bright, and Mapbox Control Room
m = folium.Map(location=[50, 23], tiles="OpenStreetMap", zoom_start=10)
m.save('map11.html')
# MacOS
# chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# Linux
# chrome_path = '/usr/bin/google-chrome %s'
webbrowser.get(chrome_path).open("file://D://UM FSKTM//Sem4 19//WIA2005//Assignment//map2.html")

