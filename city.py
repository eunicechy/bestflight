from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from collections import defaultdict
import folium
import webbrowser
import politicalSentiment as posen


class Graph:
    def __init__(self):
        self.edges = []
        self.vertex = []
        self.adjList = defaultdict(list)
        self.pathList = []
        self.airport = dict()
        self.city = dict()
        self.apgeo = defaultdict()
        self.cityps = defaultdict()
        self._init_airport()
        self._init_city()

    # initialize the country and its international airport
    def _init_airport(self):
        self.airport["Malaysia"] = "Kuala Lumpur International Airport"
        self.airport["UK"] = "London City Airport"
        self.airport["Iran"] = "Mehrabad International Airport"
        self.airport["China"] = "Beijing Capital International Airport"
        self.airport["Germany"] = "Berlin Tegel Airport"
        self.airport["Turkey"] = "Ankara Esenboga Airport"
        self.airport["Korea"] = "Incheon International Airport"
        self.airport["Libya"] = "Tripoli International Airport"
        self.airport["Argentina"] = "Ministro Pistarini International Airport"
        self.airport["US"] = "Washington Dulles International Airport"

    # initialize the airport and its capital city
    def _init_city(self):
        self.city["Kuala Lumpur International Airport"] = "KUALALUMPUR"
        self.city["London City Airport"] = "LONDON"
        self.city["Mehrabad International Airport"] = "TEHRAN"
        self.city["Beijing Capital International Airport"] = "BEIJING"
        self.city["Berlin Tegel Airport"] = "BERLIN"
        self.city["Ankara Esenboga Airport"] = "ANKARA"
        self.city["Incheon International Airport"] = "SEOUL"
        self.city["Tripoli International Airport"] = "TRIPOLI"
        self.city["Ministro Pistarini International Airport"] = "BUENOSAIRES"
        self.city["Washington Dulles International Airport"] = "WASHINGTON"

    # find the airport when user select the location
    def _get_city(self, country):
        return self.city[country]

    # find the airport when user select the location
    def _get_airport(self, country):
        return self.airport[country]

    # get geolocation of the airport
    def geolocation(self, city):
        if (city[-7:] != "Airport"):
            city = self._get_airport(city)
        if(city not in self.apgeo):
            geolocator = Nominatim()
            loca = geolocator.geocode(city)
            self.apgeo[city] = loca
        else:
            loca = self.apgeo[city]
        return loca

    # Calculate the distance between 2 city
    def _cal_distance(self, city1, city2):
        city1_lo = (city1.latitude, city1.longitude)
        city2_lo = (city2.latitude, city2.longitude)
        dist = round(great_circle(city1_lo, city2_lo).kilometers, 2)
        return dist

    # add airport to vertex
    def _add_city_(self, city1, city2):
        if(city1 not in self.vertex):
            self.vertex.append(city1)
        if(city2 not in self.vertex):
            self.vertex.append(city2)

    # insert airport to edges, adjList, vertex
    def insert_edges(self, sour, dest):
        sour = self._get_airport(sour)
        dest = self._get_airport(dest)
        sourlo = self.geolocation(sour)
        destlo = self.geolocation(dest)
        weight = self._cal_distance(sourlo, destlo)
        self._add_city_(sour, dest)
        self.edges.append((sour, dest, weight))
        self.adjList[sour].append((dest, weight))
        self.edges.append((dest, sour, weight))
        self.adjList[dest].append((sour, weight))

    # get distance in in edges between 2 airport
    def get_distance(self, sour, dest):
        distance = 0
        for i in range(len(self.edges)):
            if(self.edges[0]==sour and self.edges[1]==dest):
                distance = self.edges[2]
                break
        return distance

    # Sort the path based on the distance store in 1st element of each list
    def sort_path(self, routes):
        routes.sort()
        return routes

    # Initial call to cal path
    def short_path(self, dest, sour, routes=None):
        if (routes==None):
            sour = self._get_airport(sour)
            dest = self._get_airport(dest)
            routes = [[]]
            routes[0].append(0)
            routes[0].append(sour)
        if(len(routes)>0):
            self.sort_path(routes)
            temp = self.compute_path(dest, routes)
            self.short_path(dest, None, temp)

    # Calculate all possible path
    def compute_path(self, dest, routes):
        path = routes[0].copy()
        n = path[(len(path) - 1)]
        if(True):
            next = ""
            for j in range(len(self.adjList[n])):
                path = routes[0].copy()
                distance = self.adjList[n][j][1]
                next = self.adjList[n][j][0]
                if(next not in path):
                    routes.insert(1, path)
                    routes[1][0] += distance
                    routes[1].append(next)
                    self._possible_path(routes, dest)
            routes.remove(routes[0])
        return routes

    # Add path to pathList when reached destination or more than 4 transit
    def _possible_path(self, routes, dest):
        if (routes[1][len(routes[1])-1] == dest):
            if (3 < len(routes[1]) < 6):
                self.pathList.append(routes[1])
                routes.remove(routes[1])
            else:
                routes.remove(routes[1])
        elif(len(routes[1])>6):
            routes.remove(routes[1])
        self.sort_path(self.pathList)

    # Return the shortest path
    def get_shortest_path(self):
        return self.pathList[0]

    # Return all possible paths in ascending order
    def get_paths(self):
        return self.pathList

    # Calculate political score for each city
    def _political_score(self, airport):
        city = self._get_city(airport)
        if(city not in self.cityps):
            ps = posen.Ps(city)
            score = ps.calculate_political_score()
            self.cityps[city] = score
            ps.print_graph1()
        return self.cityps[city]

    def selection(self):
        self.short_path()


    # Draw the map
    def _map(self):
        # Map titles: OpenStreetMap, Stamen Terrain, Stamen Toner, Mapbox Bright, and Mapbox Control Room
        m = folium.Map(location=[0, 0], tiles="Mapbox Bright", zoom_start=2.3)
        points = []
        sp = self.pathList[0]
        text = "Shortest Path: "
        e = len(sp)
        while (e > 1):
            text += sp[e - 1]
            if (e > 2):
                text += ", "
            e -= 1
        text += "\nTotal distacne: " + str(sp[0]) +"km"
        print(text)
        # folium.Popup(folium.IFrame(("<div>"+text+"</div>"), width=500, height=500)).add_to(m)
        for i in range(1, len(self.pathList[0])):
            points.append((self.geolocation(self.pathList[0][i]).latitude, self.geolocation(self.pathList[0][i]).longitude))
            folium.Marker(points[i-1], popup=self.pathList[0][i]).add_to(m)
        folium.PolyLine(points, color="blue", weight=5, popup="").add_to(m)

        m.save('map2.html')
        # Open the map in Chrome browser in Windows
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open("file://D://UM FSKTM//Sem4 19//WIA2005//Assignment//map2.html", 2, True)


# initialize the graph of cities
def create_graph():
    g = Graph()
    g.insert_edges("US", "Korea")
    g.insert_edges("US", "Germany")
    g.insert_edges("US", "UK")
    g.insert_edges("UK", "Argentina")
    g.insert_edges("UK", "Turkey")
    g.insert_edges("Argentina", "Turkey")
    g.insert_edges("Argentina", "Libya")
    g.insert_edges("Libya", "Malaysia")
    g.insert_edges("Libya", "Turkey")
    g.insert_edges("Turkey", "Germany")
    g.insert_edges("Turkey", "Iran")
    g.insert_edges("Germany", "China")
    g.insert_edges("Iran", "China")
    g.insert_edges("China", "Malaysia")
    g.insert_edges("Korea", "Malaysia")
    g.short_path("Turkey", "Malaysia")
    for p in g.pathList:
        print(p)


create_graph()