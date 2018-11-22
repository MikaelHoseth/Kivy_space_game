from kivy.uix.widget import Widget
from random import *
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.animation import *
from kivy.graphics import *


#This class creates all the moving widgets.
class Element(Widget):
	def __init__(self, **kwargs):
		super(Element, self).__init__(**kwargs)

		#Remove size_hint to make widget only be as big as the elements in it.
		self.size_hint = None, None
		#set size of widget, it will also be the size if element in it.
		self.size = (30,30) #(randint(10, 50), randint(10, 50))
		
		#setting random positions from the start.
		self.pos_x = randint(0, Window.width)
		self.pos_y = randint(0, Window.height)
		self.pos = (self.pos_x, self.pos_y)

		#Variables for velocities and directions
		self.velocity_x = randint(1,4)
		self.velocity_y = randint(1,4)
		self.direction_x = 0
		self.direction_y = 0

		self.spawn_time = 1

		self.images = {}
		for i in range(0, 15):
			self.images[i] = Image(source='Comet_' + str(i) + '.png', pos=self.pos, size=(0,0))

		self.img_num = randint(0, 14)
		
		#the first elements was rectangle, therefore it is named rect. (is to be renamed)

		self.rect = self.images[self.img_num] #Image(source=self.img_name, pos=self.pos, size=(0,0))
		self.add_widget(self.rect)

		self.spawn()

		
	def spawn(self):
		anim = Animation(size=self.size, duration=self.spawn_time)
		anim.start(self.rect)
		Clock.schedule_once(self.randomly_walk, self.spawn_time)
	#when this function gets called, the widget gains random directions.
	def randomly_walk(self, dt):	
		self.direction_x = randint(0, 2)
		self.direction_y = randint(0, 2)

	#Makes widget a solid, checking collision with other widgets.
	def check_object_collides(self, objects):
		#itterating through objects recieved
		for i in objects:
			#if object identity is itself, ignore it cause ofcourse it collides with itself.
			if objects[i] == self:
				pass
			#if object is of another identity than itself, we check if we collide with them.
			if objects[i] != self:

				#if we collide with the other object.
				if self.collide_widget(objects[i]) == True:

					#The object came from the right
					#and we switch both's directions vice versa.
					if self.pos_x < objects[i].pos_x and objects[i].direction_x == 2:
						self.direction_x = 2
						self.velocity_x += 1 #increase velocity
						objects[i].direction_x = 1
					#the object came from the left
					if self.pos_x > objects[i].pos_x and objects[i].direction_x == 1:
						self.direction_x = 1
						self.velocity_x += 1 #increase velocity
						objects[i].direction_x = 2
					#the object came from the bottom
					if self.pos_y > objects[i].pos_y and objects[i].direction_y == 1:
						self.direction_y = 1
						self.velocity_y += 1 #increase velocity
						objects[i].direction_y = 2
					#the object came from the top
					if self.pos_y < objects[i].pos_y and objects[i].direction_y == 2:
						self.direction_y = 2
						self.velocity_y += 1 #increase velocity
						objects[i].direction_y = 1
					#we break the for loop, we have collided
					break
				#we pass and check for the next
				else:
					pass
				
	#checking if we collide with the window's limits.
	def check_window_collides(self):
		#if we collide with the right side of the window, minus the elements own width.
		#we change direction...
		if self.pos_x >= (800.0 - self.rect.size[0]):
			self.direction_x = 2
			#decrease velocity if colliding with right
			if self.velocity_x > 1:
				self.velocity_x -= 1
			

		#colliding with left side.
		if self.pos_x <= 0.0:
			self.direction_x = 1
			#decrease velocity if colliding with left
			if self.velocity_x > 1:
				self.velocity_x -= 1

		#colliding with top, minus the elements own height.
		if self.pos_y >= (600.0 - self.rect.size[1]):
			self.direction_y = 2
			#decrease velocity if colliding with top
			if self.velocity_y > 1:
				self.velocity_y -= 1

		#colliding with bottom
		if self.pos_y  <= 0.0:
			self.direction_y = 1
			#decrease velocity if colliding with bottom
			if self.velocity_y > 1:
				self.velocity_y -= 1

	#Change position accorting to the direction it's told to move towards.
	def move(self):
		#first we check if we have collided with another object.
		self.check_window_collides()

		#If the criteria for moving up is true.
		if self.direction_x == 1:
			self.pos_x += self.velocity_x #we move at the set velocity.

		#down
		if self.direction_x == 2:
			self.pos_x -= self.velocity_x
		#left
		if self.direction_y == 2:
			self.pos_y -= self.velocity_y
		#right
		if self.direction_y == 1:
			self.pos_y += self.velocity_y

		if self.direction_x == 0:
			pass
		if self.direction_y == 0:
			pass

		#we update the element position and the widget position.
		#we use widget position for colliding, and the element position to draw it at the same position.
		self.rect.pos = (self.pos_x, self.pos_y)
		self.pos = (self.pos_x, self.pos_y)