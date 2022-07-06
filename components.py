import pygame
from utilities import BuiltinLayers, GetMouse,GetMousePos, UIZINDEX, GetKey, GetKeys

class Component():
	def __init__(self,objectReference):
		self.gameObject = objectReference
		self.isActive = True

	def Setup(self):
		pass

	def Update(self,dt):
		pass

	def OnCollisionEnter(self,object):
		pass

	def OnDestroy(self):
		pass

	def OnRemove(self):
		pass

	def OnSceneChange(self,scene):
		pass

class NotStatic(Component):
	def __init__(self,objectReference):
		Component.__init__(self,objectReference)
		self.windowSizes= self.gameObject.windowSizes 

	def Update(self,dt):
		rect = self.gameObject.rect
		if rect.right < 0 or rect.left > self.windowSizes[0] or rect.bottom < 0 or rect.top > self.windowSizes[1]:
			if self.gameObject.isVisible != False:
				self.gameObject.isVisible = False
		else:
			if self.gameObject.isVisible != True:
				self.gameObject.isVisible = True

class CharacterController(Component):
	def __init__(self,objectReference):
		Component.__init__(self,objectReference)
		self.scene= self.gameObject.scene

		self.canJump = False

		self.groundLayer = BuiltinLayers["ground"]
		self.movementType = "2D"
		self.inputKeys = {"left":pygame.K_a,"right":pygame.K_d,"top":pygame.K_w,"bottom":pygame.K_s,"jump":pygame.K_SPACE,"run":pygame.K_LCTRL}
		self.hasRunning = True
		self.hasJumping = True
		self.normalSpeed = self.gameObject.speed.x
		self.runSpeed = self.normalSpeed*1.5
		self.ignoreCollisionsLayers = []
		self.mass = 1
		self.jumpHeight = 10
		self.useGravity = True

		self.onJumpFunction= None
		self.onLandFunction = None

		if not self.gameObject.GetComponent(RigidBody,False):
			self.gameObject.AddComponent(RigidBody)

		self.rigidBody = self.gameObject.components[RigidBody]
		self.rigidBody.useGravity = self.useGravity
		self.rigidBody.ignoreCollisionsLayers = self.ignoreCollisionsLayers
		self.rigidBody.mass = self.mass
		self.rigidBody.isStatic = False

	def OnSceneChange(self,scene):
		self.scene = scene

	def Setup(self,groundLayer=BuiltinLayers["ground"],hasJumping:bool=True,hasRunning:bool=True,useGravity:bool=True,mass:float=1,jumpHeight:float=10,ignoreCollisionsLayers:list=[],normalSpeed:float=None,runSpeed:float=None,onJumpFunction=None,onLandFunction=None)->None:
		self.groundLayer = groundLayer
		self.hasJumping = hasJumping
		self.hasRunning = hasRunning
		self.mass = mass
		self.jumpHeight = jumpHeight
		self.ignoreCollisionsLayers = ignoreCollisionsLayers
		self.useGravity = useGravity
		if normalSpeed:
			self.normalSpeed = normalSpeed
		if runSpeed:
			self.runSpeed = runSpeed

		self.rigidBody.useGravity = self.useGravity
		self.rigidBody.ignoreCollisionsLayers = ignoreCollisionsLayers
		self.rigidBody.mass = self.mass

		self.onJumpFunction = onJumpFunction
		self.onLandFunction = onLandFunction

	def SetupInput(self, movementType:str="2D",leftKey=pygame.K_a,rightKey=pygame.K_d,topKey=pygame.K_w,bottomKey=pygame.K_s,jumpKey=pygame.K_SPACE,runKey=pygame.K_LCTRL)->None:
		self.movementType = movementType
		self.inputKeys = {"left":leftKey,"right":rightKey,"top":topKey,"bottom":bottomKey,"jump":jumpKey,"run":runKey}

	def Input2D(self):
		left = GetKey(self.inputKeys["left"])
		right = GetKey(self.inputKeys["right"])
		if left:
			self.gameObject.direction.x = -1
		if right:
			self.gameObject.direction.x = 1
		if not left and not right:
			self.gameObject.StopMovement()

	def Input3D(self):
		top = GetKey(self.inputKeys["top"])
		bottom= GetKey(self.inputKeys["bottom"])
		if top:
			self.gameObject.direction.y = -1
		if bottom:
			self.gameObject.direction.y = 1
		if not top and not bottom:
			self.gameObject.StopMovement()

	def JumpInput(self):
		if GetKey(self.inputKeys["jump"]) and self.canJump:
			self.Jump()

	def RunInput(self):
		if GetKey(self.inputKeys["run"]):
			self.gameObject.speed.xy = (self.runSpeed,self.runSpeed)
		else:
			self.gameObject.speed.xy = (self.normalSpeed,self.normalSpeed)

	def Jump(self):
		self.rigidBody.gravity= 0
		self.rigidBody.gravity -= self.jumpHeight
		self.canJump = False
		if self.onJumpFunction:
			self.onJumpFunction()

	def Update(self,dt):
		self.Input2D()
		if self.movementType== "3D":
			self.Input3D()
		if self.hasJumping:
			self.CheckGround()
			self.JumpInput()
		if self.hasRunning:
			self.RunInput()

	def CheckGround(self):
		gameObject = self.gameObject
		if self.scene.Raycast(gameObject.rect.midbottom,(0,1),3,self.groundLayer,objectToIgnore=gameObject):
			if not self.canJump:
				self.canJump = True
				if self.onLandFunction:
					self.onLandFunction()
			self.rigidBody.gravity = 0
		else:
			self.canJump = False

class Button(Component):
	def __init__(self,objectReference):
		Component.__init__(self,objectReference)

		self.onClickFunction = None
		self.canClick = True
		self.onClickButton = 0

	def Setup(self,onClickFunction, onClickButton:int=0)->None:
		self.onClickFunction = onClickFunction
		self.onClickButton=onClickButton

	def Update(self,dt):
		mouse = GetMouse(self.onClickButton)
		if mouse and self.canClick:
			self.canClick= False
			pos = GetMousePos()
			if self.gameObject.rect.collidepoint(pos[0],pos[1]):
				if self.onClickFunction:
					self.onClickFunction()
				else:
					print("Button component in "+self.gameObject.name+" has no onClickFunction")

		if not mouse:
			self.canClick = True

class Text(Component):
	def __init__(self,objectReference):
		Component.__init__(self,objectReference)
		self._font = pygame.font.Font(None,20)
		self._text = "Text"
		self._textColor = "black"
		self._antialiasing = True
		self._bgColor = None
		self.gameObject.layer = BuiltinLayers["ui"]

	@property
	def font(self):
		return self._font

	@font.setter
	def font(self,f):
		self._font = f
		self.RefreshImage()

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self,t):
		self._text = t
		self.RefreshImage()

	@property
	def textColor(self):
		return self._textColor

	@textColor.setter
	def textColor(self,tc):
		self._textColor = tc
		self.RefreshImage()
	
	@property
	def antialiasing(self):
		return self._antialiasing

	@antialiasing.setter
	def antialiasing(self,a):
		self._antialiasing = a 
		self.RefreshImage()

	@property
	def bgColor(self):
		return self._bgColor

	@bgColor.setter
	def bgColor(self,bc):
		self._bgColor = bc
		self.RefreshImage()
	
	def Setup(self,font:pygame.font.Font=None,text:str="Text",textColor="black",antialiasing:bool=True,bgColor=None)->None:
		if font:
			self._font = font
		self._text = text
		self._textColor = textColor
		self._antialiasing= antialiasing
		self._bgColor = bgColor
		self.RefreshImage()

	def RefreshImage(self)->None:
		self.gameObject.image = self._font.render(self._text,self._antialiasing,self._textColor,self._bgColor) 

class RigidBody(pygame.sprite.Sprite):
	def __init__(self,objectReference):
		pygame.sprite.Sprite.__init__(self)

		self.gameObject = objectReference
		self.isActive = True
		self.oldRect = self.gameObject.rect.copy()
		self.scene = self.gameObject.scene
		self.rect = self.gameObject.rect

		self.useGravity = True
		self.gravityConstant = self.gameObject.scene.game.gravityConstant
		self.gravity = 0
		self.mass = 1
		self.isStatic = False
		self.ignoreCollisionsLayers = []

		self.scene.AddRigidBody(self)

	def OnSceneChange(self,scene):
		self.scene = scene
		if self not in scene.rigidBodies:
			scene.AddRigidBody(self)

	def Setup(self,useGravity:bool=True,isStatic:bool=False,mass:float=1,ignoreCollisionsLayers:float=[])->None:
		self.isStatic = isStatic
		self.mass = mass
		self.ignoreCollisionsLayers = ignoreCollisionsLayers
		self.useGravity = useGravity

	def Fall(self):
		self.gravity += self.gravityConstant*self.mass
		self.gameObject.position.y += self.gravity

	def Collisions(self):
		vertical = False
		collidingRigidBodies = pygame.sprite.spritecollide(self,self.scene.rigidBodies,False)
		myRect = self.gameObject.rect
		self.rect = myRect
		myOldRect = self.oldRect
		for body in collidingRigidBodies:
			if body != self and body.gameObject.layer not in self.ignoreCollisionsLayers:
				hisRect = body.gameObject.rect
				hisOldRect = body.oldRect
				collided = False

				if myRect.right >= hisRect.left and myOldRect.right <= hisOldRect.left:
					myRect.right = hisRect.left
					collided = True

				if myRect.left <= hisRect.right and myOldRect.left >= hisOldRect.right:
					myRect.left = hisRect.right
					collided = True

				if myRect.bottom >= hisRect.top and myOldRect.bottom <= hisOldRect.top:
					myRect.bottom = hisRect.top
					collided = True
					vertical = True

				if myRect.top <= hisRect.bottom and myOldRect.top >=  hisOldRect.bottom:
				 	myRect.top = hisRect.bottom
				 	collided = True
				 	vertical = True

				if collided:
					self.gameObject.position.xy = myRect.center
					collidedObj = body.gameObject
					collidedObj.OnCollisionEnter(self)
					self.gameObject.OnCollisionEnter(collidedObj)

		return vertical

	def setOldRect(self):
		self.oldRect = self.gameObject.rect.copy()

	def Update(self,dt):
		if not self.isStatic:
			verticalCollided= self.Collisions()
		if self.useGravity and not self.isStatic:
			if not verticalCollided:
				self.Fall()
			else:
				self.gravity = 0

	def OnCollisionEnter(self,object):
		pass

	def OnDestroy(self):
		self.scene.RemoveRigidBody(self)

	def OnRemove(self):
		self.scene.RemoveRigidBody(self)

class StaticUI(Component):
	def __init__(self,objectReference):
		Component.__init__(self,objectReference)

		self.gameObject.layer = BuiltinLayers["ui"]
		self.gameObject.zIndex = UIZINDEX

		if self.gameObject.GetComponent(RigidBody):
			self.gameObject.RemoveComponent(RigidBody)


