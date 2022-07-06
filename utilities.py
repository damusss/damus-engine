import pygame,sys

BuiltinLayers = {
	"default":"Default",
	"ui":"UI",
	"ignoreRaycast":"Ignore Raycast",
	"ground":"Ground",
	"particles":"Particle System"
}

LEFT = -1
RIGHT = 1
UP = -1
DOWN = 1

RIGHTCLICK = 2
MIDDLECLICK = 1
LEFTCLICK = 0

UIZINDEX = 999999

def GetKey(key)->bool:
	keys = pygame.key.get_pressed()
	if keys[key]:
		return True
	return False

def GetKeys()->list:
	return pygame.key.get_pressed()

def GetMouse(button:int)->bool:
	mouse = pygame.mouse.get_pressed()
	if mouse[button]:
		return True
	return False

def GetMousePos()->tuple:
	return pygame.mouse.get_pos()

def SetMouseVisible(visible:bool)->None:
	pygame.mouse.set_visible(visible)

def LoadImage(path:str,convertAlpha:bool=False)->pygame.Surface:
	if convertAlpha:
		image = pygame.image.load(path).convert_alpha()
	else:
		image = pygame.image.load(path).convert()

	return image

def RotateImage(image:pygame.Surface,angle:int)->pygame.Surface:
	return pygame.transform.rotate(image,angle)

def FlipImage(image:pygame.Surface,flipX:bool=False,flipY:bool=False)->pygame.Surface:
	return pygame.transform.flip(image,flipX,flipY)

def ScaleImage(image:pygame.Surface,scale:float=None,sizes:tuple=None,smooth:bool=False)->pygame.Surface:
	if scale:
		if not smooth:
			return pygame.transform.scale(image,(image.get_width()*scale,image.get_height()*scale))
		else:
			return pygame.transform.smoothscale(image,(image.get_width()*scale,image.get_height()*scale))
	elif sizes:
		if not smooth:
			return pygame.transform.scale(image,(sizes[0],sizes[1]))
		else:
			return pygame.transform.smoothscale(image,(sizes[0],sizes[1]))

def EmptyImage(sizes:tuple=(1,1),color=None)->pygame.Surface:
	image = pygame.Surface(sizes)
	if color:
		image.fill(color)

	return image

def GetTicks()->float:
	return pygame.time.get_ticks()

def GetEvents()->list:
	return pygame.event.get()

def Quit()->None:
	pygame.quit()
	sys.exit()

def DrawOnImage(imageToDraw:pygame.Surface,posOrRect,surfaceToDrawOn:pygame.Surface)->None:
	surfaceToDrawOn.blit(imageToDraw,posOrRect)

def DrawOnWindow(imageToDraw:pygame.Surface,posOrRect)->None:
	pygame.display.get_surface().blit(imageToDraw,posOrRect)

def GetWindowSurface() ->pygame.Surface:
	return pygame.display.get_surface()