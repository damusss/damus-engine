import pygame
from random import uniform, choice
from utilities import ScaleImage, EmptyImage, BuiltinLayers

class ParticleSystem():
	def __init__(self, scene,origin:tuple,parent=None):

		self.originPoint = origin
		self.originOffset = (0,0)
		self.parent= parent

		self.isActive = True
		self.isVisible = True
		self.scene = scene

		self.particles = []

		self.useGravity = True
		self.gravitySpeed = 0.1
		self._cooldown = 1000
		self.speedRandomRange = ((-1.0,1.0),(-1.0,1.0))
		self.changeOverTime = True
		self.changeMultiplier = -1
		self._startScaleOrRadius = 1
		self.destroyOrHideCooldown = 9999
		self.destroyAfterTime = False
		self.hideAfterTime = False

		self.circleParticles = False
		self.circleColor = "white"
		self.originalImages = [EmptyImage((5,5),"white")]

		self.scaleMinuser = self._startScaleOrRadius/self._cooldown

		self.lastTime = pygame.time.get_ticks()
		self.lastHide = pygame.time.get_ticks()

		self._zIndex = 0
		self.tag = "particles"
		self.layer = BuiltinLayers["particles"]

		self.rect = pygame.Rect(-1000,-1000,1,1)

		self.scene.AddGameObject(self)
		self.scene.SortObjectsByIndex()

	@property
	def cooldown(self):
		return self._cooldown
	
	@cooldown.setter
	def cooldown(self,value):
		self._cooldown = value
		self.scaleMinuser = self._startScaleOrRadius/self._cooldown

	@property
	def startScaleorRadius(self):
		return self._startScaleOrRadius
	
	@startScaleorRadius.setter
	def startScaleorRadius(self,value):
		self._startScaleOrRadius= value
		self.scaleMinuser = self._startScaleOrRadius/self._cooldown
		for image in self.originalImages:
			image = ScaleImage(image,self._startScaleOrRadius)

	@property
	def zIndex(self):
		return self._zIndex

	@zIndex.setter
	def zIndex(self,value):
		self._zIndex = value
		self.scene.SortObjectsByIndex()

	def EmptyParticles(self):
		self.particles.clear()

	def SetupAttributes(self,zIndex=0,tag="particles",layer=BuiltinLayers["particles"],isActive=True,isVisible=True):
		self._zIndex = zIndex
		self.tag = tag
		self.layer = layer
		self.scene.SortObjectsByIndex()
		self.isActive = isActive
		self.isVisible = isVisible

	def InstantiateCopy(self,scene=None):
		particleScene = scene if scene else self.scene
		particle = ParticleSystem(particleScene,self.originPoint,self.parent)
		particle.SetupAttributes(self._zIndex,self.tag,self.layer,self.isActive,self.isVisible)
		particle.SetupParticles(self.useGravity,self.gravitySpeed,self.cooldown,self.speedRandomRange[0],self.speedRandomRange[1],self.changeOverTime,self.changeMultiplier,self.startScaleOrRadius,self.circleParticles,self.originalImages,self.circleColor,self.destroyOrHideCooldown,self.hideAfterTime,self.destroyAfterTime,self.originOffset)
		return particle

	def SetupParticles(self,useGravity=True,gravitySpeed=0.1,cooldown=1000,speedRandomRangeX=(-1.0,1.0),speedRandomRangeY=(-1.0,1.0),changeOverTime=True,changeMultiplier=-1,startScaleOrRadius=1,circleParticles=False,originalImages=[],circleColor="white",destroyOrHideCooldown=9999,hideAfterTime=False,destroyAfterTime=False,originOffset=(0,0)):
		self.useGravity = useGravity
		self.gravitySpeed= gravitySpeed
		self._cooldown= cooldown
		self.speedRandomRange[0]= speedRandomRangeX
		self.speedRandomRange[1]= speedRandomRangeY
		self.cahangeOverTime = changeOverTime
		self.changeMultiplier = changeMultiplier
		self._startScaleOrRadius= startScaleOrRadius
		self.circleParticles= circleParticles
		if len(originalImages) > 0:
			self.originalImages = originalImages
		self.circleColor= circleColor
		self.destroyOrHideCooldown = destroyOrHideCooldown
		self.destroyAfterTime = destroyAfterTime
		self.hideAfterTime =hideAfterTime
		self.originOffset = originOffset

		self.scaleMinuser = self.startScaleOrRadius / self.cooldown

		for image in self.originalImages:
			image = ScaleImage(image,self._startScaleOrRadius)

	def Update(self,dt):
		if self.parent:
			self.originPoint = (self.parent.rect.centerx+self.originOffset[0],self.parent.rect.centery+self.originOffset[1])

	def DrawCircle(self,particle,screen):
		pygame.draw.circle(screen,self.circleColor,(int(particle["pos"][0]),int(particle["pos"][1])),int(particle["scale"]))

	def DrawParticle(self,particle,screen):
		if self.changeOverTime:
			particle["image"] = ScaleImage(particle["original"],particle["scale"])
		screen.blit(particle["image"],particle["pos"])

	def Draw(self,screen):

		image = choice(self.originalImages)
		self.particles.append({"pos":list(self.originPoint),"speed":[uniform(self.speedRandomRange[0][0],self.speedRandomRange[0][1]),uniform(self.speedRandomRange[1][0],self.speedRandomRange[1][1])],"time":self._cooldown,"scale":self._startScaleOrRadius,"image":image,"original":image})

		current = pygame.time.get_ticks()

		toRemove = []

		for particle in self.particles:
			particle["pos"][0] += particle["speed"][0]
			particle["pos"][1] += particle["speed"][1]

			dt = current-self.lastTime

			particle["time"] -= dt

			if self.useGravity:
				particle["speed"][1] += self.gravitySpeed

			if particle["time"] <= 0:
				toRemove.append(particle)

			if self.changeOverTime:
				preview = particle["scale"]+((dt*self.scaleMinuser) * self.changeMultiplier)
				if preview > 0:
					particle["scale"] = preview

			if self.circleParticles:
				self.DrawCircle(particle,screen)
			else:
				self.DrawParticle(particle,screen)

		for particle in toRemove:
			self.particles.remove(particle)

		if self.destroyAfterTime or self.hideAfterTime:
			if current-self.lastHide >= self.destroyOrHideCooldown:
				if self.destroyAfterTime:
					self.Destroy()
				elif self.hideAfterTime:
					self.isVisible = False
					self.EmptyParticles()
				self.lastHide = current

		self.lastTime = current

	def Destroy(self):
		self.scene.RemoveGameObject(self)
		del self

	def OnSceneChange(self,scene):
		self.scene= scene