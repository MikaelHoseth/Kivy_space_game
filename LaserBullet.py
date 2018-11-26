from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.image import Image
#from kivy.core.audio import SoundLoader


import math

#sound_1 = SoundLoader.load('LaserBlast.wav')
"""
	def animate_position(self, mouse_y, mouse_x):

		ship_x, ship_y = self.bullet.pos[0], self.bullet.pos[1]
		anim = Animation(pos=(mouse_y,mouse_x))
		anim.start(self.bullet)
	"""

class LazerBullet(Widget):
	def __init__(self, **kwargs):
		super(LazerBullet, self).__init__(**kwargs)

		self.size = (5,5)
		self.pos = (Window.width / 2, Window.height / 2)

		self.velocity = 5
		self.floatpos_y = self.pos[0]
		self.floatpos_x = self.pos[1]
		self.change_x = 0
		self.change_y = 0
		self.last_time = 1500
		self.traveling = False
		self.bullet = Image(source='shot.png', size=self.size, pos=self.pos)
		self.add_widget(self.bullet)
		#sound_1.play()
		#with self.canvas:

			#Color(1,1,1)
			#self.bullet = Rectangle(size=self.size, pos=self.pos)


	def shoot(self, mouse_y, mouse_x):
		#capture ship positions
		ship_x, ship_y = self.bullet.pos[0], self.bullet.pos[1]
		self.floatpos_y = ship_y
		self.floatpos_x = ship_x
		
		x_diff, y_diff = mouse_x - ship_x, mouse_y - ship_y	

		direct_distance = math.sqrt(((y_diff)**2) + ((x_diff)**2))

		if self.traveling:
			pass
		else:
			self.change_x = ((mouse_x - ship_x) / direct_distance ) * self.velocity
			self.change_y = ((mouse_y - ship_y) / direct_distance ) * self.velocity
			self.traveling = True

	def hit(self, element):
		if self.collide_widget(element) == True:
			return True

	def move(self):
		
		self.floatpos_y += self.change_y
		self.floatpos_x += self.change_x
		
		self.pos = (self.floatpos_x , self.floatpos_y)
		self.bullet.pos = (self.floatpos_x , self.floatpos_y)

		#print(self.pos)
		#print(self.bullet.pos)
