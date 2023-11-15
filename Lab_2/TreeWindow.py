# importing pyglet module 
import pyglet 
import pyglet.window.key as key
import pyglet.window.mouse as mouse
from pyglet import shapes

def createWindow():
    
	width = 500
	height = 500
	title = "Connect 4"
	window = pyglet.window.Window(width, height, title) 
	batch = pyglet.graphics.Batch()
	image = pyglet.image.load('board_image.png')
	board_image_rect = [230,400]
	sprite = pyglet.sprite.Sprite(image, x = 230, y = 400)
	sprite.scale = 0.125
 
	offset = [0,0]  
	speed = [0,0]
	pos = [width/2,height/2]  

	# on draw event 
	@window.event 
	def on_draw(): 
		# clear the window 
		window.clear() 
  
		pos[0]+=speed[0]
		pos[1]+=speed[1]
		offset[0] += (pos[0] - width/2 - offset[0])/10
		offset[1] += (pos[1]- height/2 - offset[1])/10
    
		renderOffset = (int(offset[0]),int(offset[1])) 
  
		x = board_image_rect[0] - renderOffset[0]
		y = board_image_rect[1] - renderOffset[1]
  
		sprite.x,sprite.y = x,y
		sprite.draw()

	@window.event 
	def on_key_press(symbol, modifier): 
    
		if symbol == key.RIGHT:
			speed[0] = 10
		if symbol == key.LEFT:
			speed[0] = -10
		if symbol == key.UP:
			speed[1] = 10
		if symbol == key.DOWN:
			speed[1] = -10
                                
		if symbol == key.C: 
			print("Key : C is pressed")
   
	@window.event 
	def on_key_release(symbol, modifier): 
		if symbol == key.RIGHT or symbol == key.LEFT:
			speed[0] = 0
		if symbol == key.UP or symbol == key.DOWN:
			speed[1] = 0
 	
  
	window.set_location(1000, 100)
	pyglet.clock.schedule_interval(lambda y:y, 1/60)
	pyglet.app.run()


createWindow()


