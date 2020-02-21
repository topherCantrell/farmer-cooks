
from console_engine import ConsoleEngine


engine = ConsoleEngine()

engine.ROOMS = {
    
    'default' : {
        'objects' : {},
        'messages' : {
            "miscDontUnderstand" : [ 
               "<genMessWhat1> I don't understand.",
               "<genMessWhat2> What?",
               "<genMessWhat3> Hmmmmmm."
            ],
            "miscNoWay" : "<genMessNoWay> You can't go that direction.",
        },
        'commands' : [
            "north", "say miscNoWay",
            "south", "say miscNoWay",
            "east",  "say miscNoWay",
            "west",  "say miscNoWay",
        ]
    },
    
    'RedRoom' : {
        'description' : '<descRed> This is the red room. You can go south.',
        'objects' : {},
        'commands' : [
            'south', 'goto BlueRoom'
        ]
    },
    
    'BlueRoom' : {
        'description' : '<descBlue> This is the blue room. You can go north.',
        'objects' : {},
        'commands' : [
            'north', 'goto RedRoom'
        ]
    }
    
}

engine.current_room = engine.ROOMS['RedRoom']

engine.main_loop()