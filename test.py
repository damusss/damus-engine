from damusengine import *

game= Game()
game.Setup((500,500),60)

def update(dt):
	scene.Raycast(obj1.rect.center,obj1.forwardDirection,200,drawRay=True,rayColor="orange")

scene = Scene(game,True)

obj1 = GameObject(scene,EmptyImage((50,50),"green"),(150,150))
obj1.AddComponent(CharacterController)

obj4 = GameObject(scene,EmptyImage(),(0,0))
obj4.AddStaticComponent(Text)
obj4.GetComponent(Text).Setup(text="player",textColor="white")
obj4.SetParent(obj1)

obj2 = GameObject(scene,EmptyImage((300,50),"red"),(150,300),True)
obj2.AddComponent(RigidBody)
obj2.components[RigidBody].isStatic = True
obj2.layer = "Ground"

obj3 = GameObject(scene,EmptyImage((50,300),"blue"),(50,225),True)
obj3.AddComponent(RigidBody)
obj3.components[RigidBody].isStatic = True

particles = ParticleSystem(scene,obj1.rect.center)
particles.startScaleorRadius = 3
particles.circleParticles = True
particles.speedRandomRange= ((-3,3),(-0.3,0.3))
particles.hideAfterTime = True
particles.destroyOrHideCooldown = 300
particles.isVisible = False
particles.gravitySpeed = 0.05

def onJump():
	particles.originPoint = obj1.rect.midbottom
	particles.isVisible=True

obj1.components[CharacterController].onJumpFunction = onJump

game.Start()