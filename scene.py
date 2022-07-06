import pygame
from utilities import BuiltinLayers, EmptyImage
from components import Text
from gameobject import GameObject
from game import Game

class DebugText(Text):
	def __init__(self,object):
		Text.__init__(self,object)
		self.gameObject.position = self.gameObject.localPosition

	def Update(self,dt):
		self.gameObject.isActive = False
		self.gameObject.rect.topleft = self.gameObject.position

class Scene():
	def __init__(self,game:Game=None,isActive:bool=False,updateFunction=None):
		self.index = 0
		self.screen = None
		self.game =game
		self.updateFunc = updateFunction
		if self.game:
			self.game.AddScene(self)
			if isActive:
				self.game.LoadScene(self.index)

		self.objects = []
		self.rigidBodies = pygame.sprite.Group()

		self.debugFont = pygame.font.Font(None,20)
		self.debugObject= GameObject(self,EmptyImage(),(20,20))
		self.debugObject.AddComponent(DebugText)
		self.debugObject.components[DebugText].Setup(textColor="white",bgColor="black")

	def Raycast(self,origin:tuple,direction:tuple,lenght:int,layerRequired=None,layersToIgnore:list=[],drawRay:bool=False,rayColor="red",objectToIgnore:GameObject=None,ignoreUI=True)->list:
		raycastRect = pygame.Rect(origin[0],origin[1],lenght if direction[0]!=0 else 1 if direction[1] != 0 else 0,1 if direction[0] != 0 else lenght if direction[1] != 0 else 0)
		if direction[0] == -1:
			raycastRect.topright = origin
		if direction[1] == -1:
			raycastRect.bottomleft = origin
		if direction == (0,0):
			return []

		objColliding = []
		layersToIgnore.append(BuiltinLayers["particles"])
		if ignoreUI:
			layersToIgnore.append(BuiltinLayers["ui"])

		for obj in self.objects:
			if obj.isActive and raycastRect.colliderect(obj.rect):
				layer = obj.layer
				if layerRequired == None:
					layerRequired = layer
				if layer not in layersToIgnore and layer == layerRequired and obj != objectToIgnore:
					objColliding.append(obj)

		if drawRay:
			pygame.draw.rect(self.screen,rayColor,raycastRect)

		return objColliding

	def GetObjectsByTag(self,tag:str)->list:
		objects = []
		for obj in self.objects:
			if obj.tag == tag:
				objects,append(obj)
		return objects

	def Debug(self,*thingsToDebug:any)->None:
		self.debugObject.isActive = True
		debugList = [str(thing) for thing in thingsToDebug]
		text = ", ".join(debugList)
		self.debugObject.components[DebugText].text = "[debug]: "+text


	def AddGameObject(self,gameObject:GameObject)->None:
		self.objects.append(gameObject)

	def RemoveGameObject(self,gameObject:GameObject)->None:
		self.objects.remove(gameObject)

	def SortObjectsByIndex(self)->None:
		self.objects = sorted(self.objects, key=lambda x: x.zIndex)

	def AddRigidBody(self,rigidBody)->None:
		self.rigidBodies.add(rigidBody)

	def RemoveRigidBody(self,rigidBody)->None:
		self.rigidBodies.remove(rigidBody)

	def Update(self,dt):
		for obj in self.objects:
			if obj.isActive:
				obj.Update(dt)
				if obj.isVisible:
					obj.Draw(self.screen)
		if self.updateFunc:
			self.updateFunc(dt)