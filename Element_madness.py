
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint
from Spaceship import *
from Collide_element import *
from LaserBullet import *
from StarSky import *
import math

import time
time_now = lambda: int(round(time.time() * 1000)) #Lambda func for calling the current time.



#Floatlayout, as MyScreen
class MyScreen(FloatLayout):
	#Initialize
	def __init__(self, **kwargs):
		super(MyScreen, self).__init__(**kwargs)
		#adding starry sky
		self.add_widget(StarSky())
		#Here we store all the moving elements
		self.element = {}
		self.element_del_que = []
		#We chose the number of elements
		self.num_of_starting_element = 5
		#enable or disable colliding with other elements
		self.collide_enabled = True
		#enable ir disable if we want them to randomly change directions at given time.
		self.randomly_walk_enabled = True
		#random movement time settings.
		self.delay = 10000 # our delay between random changing directions in milliseconds
		#variables to store timing.
		self.time_now = 0
		self.time_previous = 5
		#add player
		self.ship = Spaceship() #This is our spaceship.
		self.add_widget(self.ship)
		#class property mouse_x and mouse_y.
		self.mouse_x = 0.0
		self.mouse_y = 0.0

		#Here we add a given number of elements.
		for i in range(0, self.num_of_starting_element):
			#add element as a object in element dictionary.
			self.element[i] = Element()
			#we add element to our screen, MyScreen.
			self.add_widget(self.element[i])
			#We start off with giving them random directions.
			

		#Bings key_downs from keyboard to the window
		Window.bind(on_key_down=self._on_keyboard_down)

	#Keyboard input to change directions, it currently changes directions to all elements.
	def _on_keyboard_down(self, keyboard, keycode, text, modifiers,*args):
		print(keycode)

		#if keycode is space
		if keycode == 32: 
			self.ship.shoot()

	def on_touch_down(self, touch):
		mouse_x, mouse_y = touch.pos	
		#tell ship to angle towards mouse position          
		self.ship.angle_ship(mouse_x, mouse_y)


	def on_touch_move(self, touch):
		
		#store mouse positions
		self.mouse_x, self.mouse_y = touch.pos	
		#tell ship to angle towards mouse position
		self.ship.angle_ship(self.mouse_x, self.mouse_y)
		#tell ship to drive towards mouse position
		self.ship.mouse_drive(self.mouse_y, self.mouse_x)


	#Functions runs in a clock interval, to update everything that happens.
	def update(self, dt):
		#we itterate through our elements,
		#and checks if colliding is enabled, and if it is we call their function for checking collisions.
		for i in self.element:

			if self.collide_enabled:
				self.element[i].check_object_collides(self.element)

			#we update element positions
			self.element[i].move()

			for d in self.ship.bullets:
				if self.ship.bullets[d].hit(self.element[i]):
					self.remove_widget(self.element[i])
					self.element_del_que.append(i)

		for i in self.element:
			if i in self.element_del_que:
				self.element.pop(i)
				break

		#print(self.element)



		#This is to make them occasionally randomly change direction
		if self.randomly_walk_enabled:
			#we store the time right here.
			self.time_now = time_now()
			#we checks how long time has gone since the last time we changed directions.
			self.time_between = (self.time_now - self.time_previous)

			#if we have passed our chosen delay time or hit jackpot on the timing,
			#we itterate through our elements and calls their function for randomly changing directions.
			if self.time_between >= self.delay:

				for i in self.element:
					self.element[i].randomly_walk(0)
				#we store the time after this random change, to compare to the next time.
				self.time_previous = time_now()

				if len(self.element) == 0:
					self.element_del_que = []
					for i in range(1, randint(2, 20)):
						#add element as a object in element dictionary.
						self.element[i] = Element()
						#we add element to our screen, MyScreen.
						self.add_widget(self.element[i])
						#make em randomly walk
						#self.element[i].randomly_walk()
			#print(len(self.ship.bullets))



		self.ship.move()






#Main App
class ElementMadness(App):
	def build(self):
		#Build screen
		self.screen = MyScreen()
		#Window.clearcolor = (1, 1, 1, 1)
		#Store screen size
		self.screen.size = Window.size
		Clock.schedule_interval(self.screen.update, 1 / 60)
		return self.screen

#Main loop
if __name__ == '__main__':
	ElementMadness().run()
