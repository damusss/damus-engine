# classic imports
import pygame, sys, time

# main game class
class Game(object):
	def __init__(self):
		# init pygame
		pygame.init()

		# generic attributes
		self.clock= pygame.time.Clock()
		self.desiredFPS = 60
		self._sizes = (500,500)
		self.title = "Game using Damus Engine"
		self.onQuitFunction = None
		self.screen = None
		self.bgColor = "black"
		self.gravityConstant = 0.5

		# scenes
		self.scenes = {}
		self.activeScene = None

		self.stayOnLoadObjects = []

		# delta time
		self.lastTime = time.time()
		self.dt = 1

		# utility
		self._hasSetup = False

	def AddStayOnLoadObject(self,object):
		self.stayOnLoadObjects.append(object)

	def RemoveStayOnLoadObject(self,object):
		self.stayOnLoadObjects.remove(object)

	def Setup(self,sizes:tuple=(500,500),desiredFPS:int=60,title:str="Game using Damus Engine",onQuitFunction=None,bgColor="black")->None:
		self._sizes = sizes
		self._title= title
		self.desiredFPS = desiredFPS
		self.onQuitFunction = onQuitFunction
		self.bgColor = bgColor
		self.screen = pygame.display.set_mode(self.sizes)
		pygame.display.set_caption(self.title)
		self._hasSetup = True

	def AddScene(self,scene,isActive:bool=False)->None:
		scene.index = len(self.scenes.keys())
		scene.screen = self.screen
		scene.game = self
		self.scenes[0] = scene
		if isActive:
			self.LoadScene(scene.index)

	def GetFPS(self)->float:
		return self.clock.get_fps()

	def LoadScene(self,sceneIndex:int):
		if sceneIndex in self.scenes.keys():
			self.activeScene = self.scenes[sceneIndex]
			for obj in self.stayOnLoadObjects:
				if obj not in self.activeScene.objects:
					self.activeScene.AddGameObject(obj)
					obj.OnSceneChange(self.activeScene)
			return self.activeScene
		else:
			raise Exception(sceneIndex+" index has no associated scene. Make sure to add it")

	def RemoveScene(self,sceneIndex:int):
		if sceneIndex in self.scenes.keys():
			del self.scenes[sceneIndex]
		else:
			raise Exception(sceneIndex+" index has no associated scene. Make sure to have it")

	@property
	def sizes(self):
		return self._sizes

	@property
	def title(self):
		return self._title
	
	@property
	def hasSetup(self):
		return self._hasSetup

	@sizes.setter
	def sizes(self,value):
		print("Changing the sizes attribute will not affect the actual window sizes")
	
	@title.setter
	def title(self,value):
		self._title = value
		pygame.display.set_caption(self.title)

	@hasSetup.setter
	def hasSetup(self,value):
		print("You cannot change the has setup attribute")
	
	def Update(self):
		while True:
			current = time.time()
			self.dt = (current-self.lastTime)*60
			self.lastTime = current

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					if self.onQuitFunction:
						self.onQuitFunction()
					else:
						self.Quit()

			self.screen.fill(self.bgColor)

			self.activeScene.Update(self.dt)

			self.clock.tick(self.desiredFPS)
			pygame.display.update()


	def Quit(self):
		print("Application quitted")
		pygame.quit()
		sys.exit()

	def Start(self):
		if self.hasSetup:
			if self.activeScene:
				self.Update()
			else:
				raise Exception("No scene is set to active")
		else:
			raise Exception("Game object hasn't been setup.")