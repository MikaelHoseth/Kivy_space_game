from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics.transformation import Matrix
from kivy.graphics import PushMatrix, Rotate, PopMatrix
from kivy.clock import Clock
from LaserBullet import *
import time
import math
time_now = lambda: int(round(time.time() * 1000)) #Lambda func for calling the current time.

	


class Spaceship(Widget):
	def __init__(self, **kwargs):
		super(Spaceship, self).__init__(**kwargs)

		
		self.size = (50,50)

		self.velocity = 1
		self.floatpos_y = 50#self.pos[0]
		self.floatpos_x = 50#self.pos[1]
		self.change_x = 0
		self.change_y = 0
		self.angle = 0

		#Creating spaceship, of widget type 'Scatter' which alowes for rotation
		#self.ship = Scatter(do_scale = False, size=self.size, pos=self.pos)
		
		
		#body of ship is an image
		self.ship = Image(source='redfighter00050.png', size=self.size, pos=self.pos, color=(1,1,1,1))
		self.anim_count = 0
		#adding body to scatter widget
		#self.ship.add_widget(self.body)
		with self.ship.canvas.before:
			PushMatrix()
			self.rot = Rotate()
			self.rot.axis = (0,0,1)
			self.rot.origin=self.ship.center
			self.rot.angle = 0
		with self.ship.canvas.after:
			PopMatrix()

		#adding scatter widget to Spaceship widget.
		self.add_widget(self.ship)
		self.bind(pos = self.binding)


		#The reason for storing the time variables as properties is to use em everywhere in this class.
		self.time_now = 0.0 #variable to store time now.
		self.time_between = 0.0 #Variable to store Time between making a bullet and making a new one.
		self.time_previous = 0.0 #variable to store previous time of making a bullet.
		self.shoot_speed = 30   #Increase to reduce shooting speed.
		self.bullets = {}	#Bullets are stored here for their amount of time.
		self.shooting = False	#Bool, are we shooting or not?.
		self.burst_time = 1000 #Time the spaceship keeps shooting after button pressed.

	def rocket_trace(self):
		with self.canvas:

			self.trace = Rectangle(size=(1,1), pos=(self.ship.center))


	def binding(self, * args):
		self.ship.center = self.ship.center
		self.ship.size = (self.ship.size)

	def stop_shoot(self):
		self.shooting = False
	def shoot(self):
		self.shooting = True


	def reduce_speed(self):
		pass
		 
	#captures a moment from input, for later use.
	def capture_input(self, time):
		self.input_time = time

	def mouse_drive(self, mouse_y, mouse_x):
		self.mouse_y = mouse_y
		self.mouse_x = mouse_x
		#capture ship positions
		ship_x, ship_y = self.ship.pos[0], self.ship.pos[1]
		#float positions of x and y.
		self.floatpos_y = ship_y
		self.floatpos_x = ship_x
		#difference between coordinates.
		x_diff, y_diff = mouse_x - ship_x, mouse_y - ship_y
		#calculating angle between mouse position and ship positions.
		direct_angle = math.sqrt(((mouse_y - ship_y)**2) + ((mouse_x - ship_x)**2))
		#adding the numbers to the changes going to be made.
		self.change_x = ((mouse_x - ship_x) / direct_angle ) * self.velocity
		self.change_y = ((mouse_y - ship_y) / direct_angle ) * self.velocity
		

	#Feed this with mouse positions to angle ship towards it.
	def angle_ship(self, mouse_y, mouse_x):
		#print("Pos", touch.pos)
		#store ship positions
		ship_x, ship_y = self.pos
		#calculating vector from ship to mouse position
		rel_x, rel_y = mouse_x - ship_x, mouse_y - ship_y
		#calculating angle
		self.angle = (180 / math.pi) * - math.atan2(rel_y, rel_x)
		
		self.rot.angle = self.angle
		#print("ShipAngle:", angle)
		#Making sure the center anchor of ship gets updated when moving mouse.
		self.rot.origin = self.ship.center

	def move(self):
		#self.rocket_trace()
		#self.check_window_collides()

		#making sure for every frame that the rotation anchor stays in center of ship.
		self.rot.origin = self.ship.center
		#updating angle despite that the mouse is not being hold down.
		self.rot.angle = self.angle
		#adding change of velocity towards y and x to floatpos.
		self.floatpos_y += self.change_y 
		self.floatpos_x += self.change_x 
		#Updating position, of both widget and ship.
		self.pos = (self.floatpos_x , self.floatpos_y)
		self.ship.pos = (self.floatpos_x , self.floatpos_y)

		if self.shooting:
			self.time_now = time_now()

			time_between  = (self.time_now - self.time_previous)
			

			if time_between >= self.shoot_speed:
				self.bullets[self.time_now] = LazerBullet()
				self.bullets[self.time_now].bullet.pos = (self.ship.center)
				self.add_widget(self.bullets[self.time_now])

			self.time_previous = time_now()

			if self.time_previous > self.burst_time:
				self.stop_shoot()

		for i in self.bullets:
			if (self.time_now - int(i)) >= self.bullets[i].last_time:
						self.remove_widget(self.bullets[i])
						self.bullets.pop(i)
						break

		if len(self.bullets) > 0:
			for i in self.bullets:
				self.bullets[i].shoot(self.mouse_y, self.mouse_x)
				self.bullets[i].move()



		print(len(self.bullets))



		

		
