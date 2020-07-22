
from console_engine import ConsoleEngine


engine = ConsoleEngine()

engine.ROOMS = {
    
    'default' : {
        'objects' : [],
        'messages' : {
            "miscNoWay"          : "<genMessNoWay> You can't go that direction.",
            "miscHandEmpty"      : "<genMessHandEmpty> Your hand is empty.",
            "miscNothingToGet"   : "<genMessNothingThere> There is nothing to get.",
            "miscHandFull"       : "<genMessHandFull> You already have something in that hand.",
            "miscLeftHand"       : "<genMessLeftHand> In your left hand: ",
            "miscRightHand"      : "<genMessRightHand> In your right hand: ",
            "miscOK"             : "<genMessOK> OK.",
            "miscNothingHappens" : "<genMessNothingHappens> Nothing happens.",
            "miscDontUnderstand" : [ 
                                   "<genMessWhat1> I don't understand.",
                                   "<genMessWhat2> What?",
                                   "<genMessWhat3> Hmmmmmm."
                                   ]
        },
        'commands' : [
            'north', 'say miscNoWay',
            'south', 'say miscNoWay',
            'east',  'say miscNoWay',
            'west',  'say miscNoWay',
            
            # Look
            "look" ,      "generalDescribeRoom",     # LOOK describe the room
            
            # Gets                        
            "get * - *" , "say miscNothingToGet",    # GET left/right with nothing to get (doesn't matter what's in the hand)
            "get * * -" , "generalGet",              # GET left/right something with nothing in hand (generic GET handler)
            "get * * *" , "say miscHandFull",        # GET left/right something but something in hand        
            
            # Uses
            "use * -",    "say miscHandEmpty",       # USE left/right with nothing in hand
            "use * *",    "say miscNothingHappens",  # Use left/right with something in hand
            
            # Drops
            "drop * -",   "say miscHandEmpty",       # DROP left/right with nothing in hand
            "drop * *",   "generalDrop",             # DROP left/right with something in hand            
        ]
    },
    
    'RedRoom' : {
        'description' : '<descRed> This is the red room. You can go south.',
        'objects' : [
            {
                'id'    :  'trumpet',
                'short' : '<objTrumpetShort> trumpet',
                'long'  : '<objTrumpetLong> There is a silver trumpet here.'
            },
            {
                'id'    :  'lamp',
                'short' : '<objLampShort> lamp',
                'long'  : '<objLampLong> There is a brass lamp here.'
            }
        ],
        'commands' : [
            'south', 'goto BlueRoom'
        ]
    },
    
    'BlueRoom' : {
        'description' : '<descBlue> This is the blue room. You can go north.',
        'objects' : [],
        'commands' : [
            'north', 'goto RedRoom'
        ]
    }
    
}

engine.current_room = engine.ROOMS['RedRoom']

#import prompt_manager
#prompts = prompt_manager.find_all_prompts(engine)

engine.main_loop()