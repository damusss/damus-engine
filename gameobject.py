import pygame
from utilities import GetMousePos, RotateImage, ScaleImage, BuiltinLayers,FlipImage
from components import RigidBody, NotStatic

class GameObject(object):
	def __init__(self,scene,image:pygame.Surface,startCenterPosition:tuple,isStatic=False):
		self._scene= scene
		self._parent = None
		self._isVisible = True
		self._isActive = True
		self._image = image
		self.rect = self._image.get_rect(center=startCenterPosition)
		self.layer = None
		self.tag = ""
		self.name = "<Game Object>"
		self._zIndex = 0
		self.direction = pygame.math.Vector2((0,0))
		self.speed = pygame.math.Vector2((5,5))
		self.position = pygame.math.Vector2(self.rect.center)
		self.localPosition =pygame.math.Vector2(self.position.xy)
		self.forwardDirection = pygame.math.Vector2(self.direction.xy)
		self._windowSizes = self._scene.game.sizes
		self.hasRigidBody = False
		self._isStatic = isStatic

		self.children = []
		self.components = {}
		self.staticComponents = {}

		self._scene.AddGameObject(self)
		self._scene.SortObjectsByIndex()

		self.coroutimes = []

		if not self._isStatic:
			self.AddComponent(NotStatic)

	def SetupAttributes(self,parent=None,isVisible:bool=True,isActive:bool=True,layer=BuiltinLayers["default"],tag:str="gameobject",zIndex:int=0,speed:tuple=(5,5),direction:tuple=(0,0),name:str="<Game Object>")->None:
		if parent:
			self.SetParent(parent)
		self._isVisible = isVisible
		self._isActive = isActive
		self._zIndex = zIndex
		self._scene.SortObjectsByIndex()
		self.tag = tag
		self.layer = layer
		self.speed.xy = speed
		self.direction.xy = direction
		self.name = name

	def StartCoroutime(self,function,cooldown):
		self.coroutimes.append([function,cooldown,pygame.time.get_ticks()])

	def InstantiateCopy(self,scene=None):
		objScene = scene if scene != None else self._scene
		obj = GameObject(objScene,self.image,self.rect.center,self._isStatic)
		obj.SetupAttributes(self._parent,self.isVisible,self.isActive,self.layer,self.tag,self._zIndex,self.speed.xy,self.direction.xy,self.name)
		obj.localPosition.xy = self.localPosition.xy
		obj.forwardDirection.xy = self.forwardDirection.xy
		obj.position.xy = self.position.xy
		obj.hasRigidBody = self.hasRigidBody
		obj.children = self.children
		obj.components = self.components
		obj.staticComponents = self.staticComponents
		return obj

	def Draw(self,screen):
		screen.blit(self.image,self.rect)

	def OnSceneChange(self,scene):
		self._scene= scene
		for component in self.components.values():
			component.OnSceneChange(scene)
		for staticCompoenent in self.staticComponents.values():
			staticCompoenent.OnSceneChange(scene)

	def OnCollisionEnter(self,gameObject)->None:
		for component in self.components.values():
			component.OnCollisionEnter(gameObject)
		for staticComponent in self.staticComponents.values():
			staticComponent.OnCollisionEnter(gameObject)

	def BlitImageOn(self,image:pygame.Surface,posOrRect)->None:
		self._image.blit(image,posOrRect)

	def StopMovement(self)->None:
		self.direction.xy = (0,0)

	def CheckSingleCollision(self,gameObject)->bool:
		return self.rect.colliderect(gameObject.rect)

	def CheckMouseCollision(self)->bool:
		pos = GetMousePos()
		return self.rect.collidepoint(pos[0],pos[1])

	def Destroy(self)->None:
		for component in self.components.values():
			component.Destroy()
			component.OnDestroy()
		for staticComponent in self.staticComponents.values():
			staticComponent.Destroy()
			staticComponent.OnDestroy()
		self.scene.RemoveGameObject(self)
		del self

	def SetParent(self,parentObject)->None:
		if self._parent != None:
			self._parent.RemoveChild(self)
		self._parent = parentObject
		if self._parent != None:
			self._parent.AddChild(self)

	def AddChild(self,childObject)->None:
		self.children.append(childObject)

	def RemoveChild(self,childObject)->None:
		self.children.remove(childObject)

	def MoveHorizontal(self,amount:int)->None:
		self.position.x += amount

	def MoveVertical(self,amount:int)->None:
		self.position.y += amount

	def Rotate(self,angle:int)->pygame.Surface:
		self.image = RotateImage(self._image,angle)
		return self._image

	def Scale(self,scale:float=None,sizes:tuple=None,smooth:bool=False)->pygame.Surface:
		self.image = ScaleImage(self._image,scale,sizes,smooth)
		return self._image

	def Flip(self,horizontal:bool,vertical:bool)->pygame.Surface:
		self.image = FlipImage(self._image,horizontal,vertical)
		return self._image

	def AddComponent(self,componentType):
		self.components[componentType] = componentType(self)
		if componentType == RigidBody:
			self.hasRigidBody= True
		return self.components[componentType]

	def AddStaticComponent(self,componentType):
		self.staticComponents[componentType] = componentType(self)
		return self.staticComponents[componentType]

	def RemoveComponent(self,componentType)->None:
		if componentType in self.components.keys():
			if componentType== RigidBody:
				self.hasRigidBody= False
			component = self.components[componentType]
			component.OnRemove()
			self.components.remove(component)
		elif componentType in self.staticComponents.keys():
			component = self.staticComponents[componentType]
			component.OnRemove()
			self.staticComponents.remove(component)
		else:
			print("Couldn't find component")
			return False

	def GetComponent(self,componentType,returnIfNotFound=False):
		if self.components.get(componentType):
			return self.components[componentType]
		elif self.staticComponents.get(componentType):
			return self.staticComponents[componentType]
		else:
			return returnIfNotFound


	def Update(self,dt):
		if self.direction.length() != 0:
			self.direction = self.direction.normalize()
			self.forwardDirection.xy = self.direction.xy

		if self.hasRigidBody:
			self.components[RigidBody].setOldRect()

		self.position.x += self.speed.x*self.direction.x*dt
		self.position.y += self.speed.y*self.direction.y*dt
		self.rect.center = (round(self.position.x),round(self.position.y))

		for component in self.components.values():
			if component.isActive:
				component.Update(dt)

		for child in self.children:
			child.rect.center = (self.rect.centerx+child.localPosition.x,self.rect.centery+child.localPosition.y)
			child.position.xy = child.rect.center

		for c in self.coroutimes:
			if pygame.time.get_ticks()-c[2] >= c[1]:
				c[0]()
				self.coroutimes.remove(c)

	@property
	def isStatic(self):
		return self._isStatic

	@isStatic.setter
	def isStatic(self,value):
		self._isStatic =value
		if value== True:
			if self.components.get(NotStatic):
				self.RemoveComponent(NotStatic)
		elif value==False:
			if not self.components.get(NotStatic):
				self.AddComponent(NotStatic)

	@property
	def isActive(self):
		return self._isActive

	@property
	def isVisible(self):
		return self._isVisible

	@property
	def zIndex(self):
		return self._zIndex

	@property
	def image(self):
		return self._image

	@property
	def scene(self):
		return self._scene

	@property
	def windowSizes(self):
		return self._windowSizes

	@property
	def parent(self):
		return self._parent
	

	@isActive.setter
	def isActive(self,value):
		self._isActive = value
		for child in self.children:
			child.isActive = value

	@isVisible.setter
	def isVisible(self,value):
		self._isVisible = value
		for child in self.children:
			child.isVisible = value

	@zIndex.setter
	def zIndex(self,value):
		self._zIndex = value
		self._scene.SortObjectsByIndex()

	@image.setter
	def image(self,value):
		self._image = value
		self.rect = self._image.get_rect(center=self.rect.center)

	@scene.setter
	def scene(self,value):
		print("You cannot change the scene attribute")

	@windowSizes.setter
	def windowSizes(self,value):
		print("You cannot change window sizes attribute")

	@parent.setter
	def parent(self,value):
		print("You cannot change the parent attribute. To set the parent use the SetParent function instead")

	
	
	
	
	


