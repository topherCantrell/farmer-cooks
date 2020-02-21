
# Commands:
#   - north, east, south, west
#   - action, look
#   - use left/right objInHand ("-" for nothing)
#   - get left/right objToGet objInHand ("-" for nothing)
#   - drop left/right objInHand ("-" for nothing)
    
# These can all be built as one big literal. I find it easier to follow broken out.

ROOMS = {}
GAME = {}

ROOMS['default'] = {

    # The "default" room is for objects that are out of play, general messages, and the
    # general command handlers (that specific rooms can override).
    
    # Audio/Text messages are defined as
    # name:this is the text
    # where the name can be referenced in other places and is the name of the audio file (no file extension needed)    
    
    # List of objects in the room
    "objects" : [
        # The butter appears when you churn the milk
        {
            "id"     : "butter", # Referenced by the app_console
            "short"  : "<objButterShort> butter", # The short description is what appears in the inventory
            "long"   : "<objButterLong> There is butter here.", # The long description appears with the room
            "stuck"  : False, # [False] False if you can move the object
            "hidden" : False # [False] True if the object is hidden (can't be seen or targeted)
        },
        # The empty pail
        {
            "id" : "pail",
            "short" : "<objPailShort> empty pail",
            "long"  : "<objPailLong> There is an empty pail here.",
        },
        # The pail with milk
        {
            "id" : "pail_with_milk",
            "short" : "<objPailMilkShort> pail filled with milk",
            "long"  : "<objPailMilkLong> There is a pail here full of milk.",
        }
    ],   

    # Search order for message refs:
    # 1. Defined (as in "say miscNo:No!!!!!")
    # 2. In the current room's "messages"
    # 3. In the "default" room's "messages"

    # General purpose messages
    "messages" : {
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
            
    # General command handlers
    "commands" : [
        # Default directions
        "north" ,    "say miscNoWay",            # N,E,S,W say "can't go that way"
        "south" ,    "say miscNoWay",
        "east" ,     "say miscNoWay",
        "west" ,     "say miscNoWay",
        
        # Look
        "look" ,      "generalDescribeRoom",     # LOOK describe the room
        
        # Action
        "action" ,    "say miscNothingHappens",  # ACTION nothing happens
        
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
}
  
ROOMS['Parlor'] =  {
    "description": "<descParlor> TODO This is the parlor. Churn is here. You can go south.",
    "commands" : [
       "south", "goto Porch",            
       "use * pail_with_milk", [  
           "move butter to _here",
           "move pail_with_milk default",
           "move pail to _here",
           # Single use prompts ... can define inline
           "say '<madeButter> You made butter! The cat drank some milk.'"
       ],
       # These are processed before the "moveable" check.
       "get * churn *" , "say getChurn",
    ],
      
    "messages" : {
        "getChurn" : "<objChurnWontBudge> The churn won't budge."
    },
    
    "objects" : [
        {
            "id" : "churn",
            "long" : "<objChurnLong> There is a churn here.",
            "stuck" : True
        }
    ]
}    

ROOMS['Porch'] =  {
    "description"  : "<descPorch> TODO The porch!",
    "commands"     : [],
    "objects"      : [],
}
