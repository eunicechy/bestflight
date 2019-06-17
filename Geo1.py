from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from gmplot import gmplot

def cal_distance(city1, city2):
    city1_lo = (city1.latitude, city1.longitude)
    city2_lo = (city2.latitude, city2.longitude)

    return geodesic((city1_lo,city2_lo).kilometers)

geolocator = Nominatim(user_agent="XXX")

kl = geolocator.geocode("KLIA")
London = geolocator.geocode("London City Airport")
Tehran = geolocator.geocode("Mehrabad International Airport")
bj = geolocator.geocode("Beijing Capital International Airport")
berlin = geolocator.geocode("Berlin Tegel Airport")
ankara = geolocator.geocode("Ankara Esenboga Airport")
seoul = geolocator.geocode("Incheon International Airport")
tripoli = geolocator.geocode("Tripoli International Airport")
ba = geolocator.geocode("Ministro Pistarini International Airport")
washing = geolocator.geocode("Washington Dulles International Airport")

latitude_list = [kl.latitude, London.latitude]
longitude_list = [kl.longitude, London.longitude]
gmap = gmplot.GoogleMapPlotter((kl.latitude + London.latitude) /2, (London.longitude + kl.longitude) /2, 5)
gmap.scatter(latitude_list, longitude_list, '# FF0000', size = 40, marker = False)
gmap.plot(latitude_list, longitude_list, color = 'cornflowerblue', edge_width = 5.0)
gmap.apikey = "AIzaSyA0JWAH65qm3USeOo9E1vFH1WUC_4SLiYQ"
gmap.draw("map.html")