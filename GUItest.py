import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import *
from functools import partial
from kivy.uix.checkbox import *
from kivy.uix.dropdown import *
from kivy.uix.listview import *
import graph


# initialize the graph of cities
def create_graph():
    g = graph.Graph()
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
    g.insert_edges("China", "Korea")
    g.insert_edges("China", "Turkey")
    g.insert_edges("Korea", "Malaysia")
    g.insert_edges("Korea", "Germany")
    g.insert_edges("Malaysia", "Iran")
    return g


dis = create_graph()


class Choice(BoxLayout):
    pass

    def choose(self, *args):
        d = args[0]
        print(d)
        dis.short_path(d)
        print(dis.pathList)
        App.get_running_app().stop()
        return


class MyApp(App):
    def build(self):
        self.title = "Destination"
        return Choice()


class Result(BoxLayout):
    def __init__(self,**kwargs):
        super(Result, self).__init__(**kwargs)
        self.orientation = 'vertical'
        display = BoxLayout(orientation='vertical')
        instruction = Label(text='Choose the path you prefer')
        display.add_widget(instruction)
        c = 0
        for p in dis.pathList:
            t = "Path: "
            ps = "Political Score: "
            score = 0
            for i in range(1,len(p)):
                if(i>5):
                    break
                t += dis._get_city(p[i])+" "
                if(1<i<len(p)-1):
                    s = dis._political_score(p[i])
                    if(s>5):
                        sign = "positive"
                    elif(s<-5):
                        sign = "negative"
                    else:
                        sign = "neutral"
                    score += s
                    ps += dis._get_city(p[i])+" -> "+sign+" "
            t += "Distance: {}km".format(round(p[0], 2))
            btn = Button(text=('[b]'+t+'\n'+ps+'[/b]'),markup=True, color=(1,1,0,1))
            # btn.size()
            btn.id = str(c)
            btn.bind(on_press=self.select)
            display.add_widget(btn)
            c += 1
        self.add_widget(display)
        return

    def select(self, obj):
        selected = dis.pathList[int(obj.id)]
        dis.print_map(selected)
        return


class FlightApp(App):
    def build(self):
        self.title = "Selection"
        return Result()


if __name__ == '__main__':
    first = MyApp()
    first.run()
    FlightApp().run()