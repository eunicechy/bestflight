# Import gmplot library.
from gmplot import *
# Place map
# First two arugments are the geogrphical coordinates .i.e. Latitude and Longitude
#and the zoom resolution.
gmap = gmplot.GoogleMapPlotter("2.74552395", "101.701506799265", 18)
# Location where you want to save your file.
gmap.draw("map11.html")

# Malysia
kl = geolocator.geocode("KLIA")
# United Kingdom
london = geolocator.geocode("London City Airport")
# Iran
tehran = geolocator.geocode("Mehrabad International Airport")
# China
bj = geolocator.geocode("Beijing Capital International Airport")
# Germany
berlin = geolocator.geocode("Berlin Tegel Airport")
# Turkey
ankara = geolocator.geocode("Ankara Esenboga Airport")
# Korea
seoul = geolocator.geocode("Incheon International Airport")
# Libya
tripoli = geolocator.geocode("Tripoli International Airport")
# Argentina
ba = geolocator.geocode("Ministro Pistarini International Airport")
# United State of America
washing = geolocator.geocode("Washington Dulles International Airport")