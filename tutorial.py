# import like that
from damusengine import *

# game instance
game = Game()

# if you wanna do something cool on quit, define this function, otherwise it will do it automatically
def onQuit():
	game.Quit() # if you forget this line you will need to close the process via task manager lol
	# other fancy stuff

# setup the game. the parameters are NOT required
game.Setup((500,500),60,"Tutorial game","green")

# define you scene update function, if you wanna do something in it, else don't
def update(dt): # dt is required in EVERY update function
	# do something fancy
	scene.Debug(round(game.GetFPS()))

# make a scene
scene = Scene(game,True,update)
# if you DON'T pass game and isActive parameter, you'll have to add the scene like that:
horribleScene = Scene()
game.AddScene(horribleScene)
game.LoadScene(horribleScene.index)

# you can also remove them
game.RemoveScene(horribleScene.index)
game.LoadScene(scene.index)

# create a game object
obj1 = GameObject(scene,EmptyImage((100,100),"red"),(300,200)) # those are the only required parameters
# to change the other ones quickly, use the Setup function, otherwise, you can change the attributes manually
# some attributes cannot be set, you will be notified if you try to

# some useful things you may want to know:
#1 every frame the center of the rect of an object get set to it's position attribute. if you want to
# specifically change one rect value, remember to add a obj.position.xy = obj.rect.center
#2 speed, direction, forwardDirection and localPosition are all VECTORS. you can access their coordinates like
# vector.x, vector.y, vector[0], vector[1] but if you wanna change both don't do vector = (0,0) but vector.xy = (0,0)
# + never do vector = pygame.math.Vector2((0,0)) every frame (if you can avoid it),  it's performance consuming 
#3 there are 2 methods to instantly moving the object (moveHorizontal and vertical) but to achieve a fluid movement
# you should change the direction attribute leaving the speed the same. there is a StopMovement fun that set direction to (0,0)
#4 if you make an object a child, changing it's position attribute will be absolutely useless.change instead the localPosition, that offset from parent center

# and now the COMPONENTSSSSS

# when you add, remove or get a component, you have to pass in the function it's TYPE, not the object. here is an example
obj1.AddComponent(RigidBody)
objRigidBody = obj1.GetCompoenent(RigidBody)
# to make the get faster do it like that:
anotherRigidBodyInstance = obj1.components[RigidBody]
# if a component does not have an update, use the AddStaticCompoent instead. remove and get will be the same
# defualt static components are Text and StaticUI
# you can make a custom component like that:
class CustomComponent(Component):
	def __init__(self,objectReference):
		Component.__init__(self.objectReference)

		# by default, a component always have a gameObject attribute, referencing the object attached to
		# a component have the following overridable functions: Update (parameter: dt), OnCollisionEnter (parameter: object), OnSceneChange(parameter: scene), OnDestroy and OnRemove. a Setup is also present, but shouldn't be needed for custom ones

# built in components have their attributes by default,but to quickly change them they also have a Setup function.otherwise change the attributes like always
# here are the built in components

# RigidBody. needed for collisions and gravity. a static rigidbody won't be moved
# Text. change object image to a text. everything is customizable. when you change an attribute, the image is refreshed!
# button. when you click the obect it will fire a function you have to pass into the setup, or set manually.
# StaticUI. set the object layer to ui(raycast by default don't see them) and change it's zIndex to a high value, to make it always on top
# CharacterController. has input and jumping (customizable, even the keys). movementType 3d means you can move left, right,top, bottom, while 2D only left right
# character controller automatically add a rigid body

# new one is NotStatic. in object constructor, you can pass a isStatic argument, false by default.if you leave it false,
# the object will add a NotStatic components, that checks if the game is outside the window to make isVisible false.
# if you know an object will ALWAYS stay inside the window, pass isStatic as false to avoid this checks. StaticUI remove
# it automatically. changing isStatic will automatically add or remove the component.

# you can set an object to stay on load but i haven't tested much so it may break something

# you can call StartCoroutime to create a coroutime. exactly like unity

# DAMUS PARTICLES SYSTEM, A GREAT WAY TO MAKE PARTICLES IN THE DAMUS ENGINE
# you instantiate similar to objects
particles = ParticleSystem(scene,obj1.rect.center,obj1) #2 parameter is the origin from where particles spawn, 3 parameter is the parent. you can avoid passing this
# setup the  normal attributes with SetupAttributes, the particles related with SetupParticles or change stuff manually
# you can choose between having a circle particle or one with custom images. 

# start the game (you can call that whenever you want, but you have to create at least one scene)
# its is good practice to put it when all pre-init objects are created. but you can instanciate them during runtime
game.Start()

#it's all i think
# ask everything on discord
# check the files in case something is not clear or ask me.i worked hard on it and on the tutorial especially. bye