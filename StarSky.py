from random import *
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


class StarSky(BoxLayout):
	def __init__(self, **kwargs):
		super(StarSky, self).__init__(**kwargs)

		self.stars = {}

		for i in range(0, 500):
			with self.canvas:
				Color(uniform(0.0,1.0), uniform(0.0,1.0), uniform(0.0,1.0), uniform(0.0,1.0))
				Rectangle(pos=(randint(0, Window.width - 5), randint(0, Window.height - 5)), size=(1,1))


