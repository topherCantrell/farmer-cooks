import FARM
from console_engine import ConsoleEngine


engine = ConsoleEngine()

engine.ROOMS = FARM.ROOMS

engine.current_room = engine.ROOMS['Porch']

# FOR TESTING
# Put the pail with milk in the room with us
engine.ROOMS['Porch']['objects'].append(engine.ROOMS['default']['objects'][2])
del engine.ROOMS['default']['objects'][2]

engine.main_loop()