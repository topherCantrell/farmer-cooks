
# Commands:
#   - north, east, south, west
#   - action, look
#   - use left/right objInHand ("-" for nothing)
#   - get left/right objToGet objInHand ("-" for nothing)
#   - drop left/right objInHand ("-" for nothing)
    
ROOMS = {}

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
            "id" : "butter", # Referenced by the app_console
            "short" : "objButterShort:butter", # The short description is what appears in the inventory
            "long" : "objButterLong:There is butter here.", # The long description appears with the room
            "stuck" : False, # [False] False if you can move the object
            "hidden" : False # [False] True if the object is hidden (can't be seen or targeted)
        }
    ],   

    # Search order for message refs:
    # 1. Defined (as in "say miscNo:No!!!!!")
    # 2. In the current room's "messages"
    # 3. In the "default" room's "messages"

    # General purpose messages
    "messages" : {
        "miscNoWay" : "You can't go that direction.",
        "miscHandEmpty" : "Your hand is empty.",
        "miscNothingToGet" : "There is nothing to get.",
        "miscHandFull" : "You already have something in that hand.",
        "miscLeftHand" : "In your left hand: ",
        "miscRightHand" : "In your right hand: ",
        "miscOK" : "OK.",
        "miscNothingHappens" : "Nothing happens.",
    },
            
    # General command handlers
    "commands" : [
        # Default directions
        "north" , "say miscNoWay", # No ":" in this ... this must be a message reference
        "south" , "say miscNoWay",
        "east" , "say miscNoWay",
        "west" , "say miscNoWay",
        
        # Look
        "look" , "generalDescribeRoom",
        
        # Action
        "action" , "say miscNothingHappens", # ACTION nothing happens
        
        # Gets                        
        "get * - *" , "say miscNothingToGet", # GET left/right nothing to get (doesn't matter what's in the hand)
        "get * * -" , "generalGet", # GET left/right something and nothing in hand (generic GET handler)
        "get * * *" , "say miscHandFull", # GET left/right something but something in hand        
        
        # Uses
        "use * -","say miscHandEmpty", # USE left/right nothing in hand
        "use * *","say miscNothingHappens", # Use left/right something in hand
        
        # Drops
        "drop * -","say miscHandEmpty", # DROP left/right nothing in hand
        "drop * *","generalDrop", # DROP left/right something in hand        
    ]
}
  
ROOMS['Parlor'] =  {
    "description": "descParlor:TODO This is the parlor. Churn is here. You can go south.",
    "commands" : [
       "south", "goto Porch",            
       "use * pail_with_milk", [  
           "move butter to _here",
           "move pail_with_milk default",
           "move pail to _here",
           # Single use prompts ... can define inline
           "say 'madeButter:You made butter! The cat drank some milk.'"
       ],
       # These are processed before the "moveable" check.
       "get * churn" , "say getChurn",
    ],
      
    "messages" : {
        "getChurn" : "The churn won't budge."
    },
    
    "objects" : [
        {
            "id" : "churn",
            "long" : "objChurnLong:There is a churn here.",
            "stuck" : True
        }
    ]
}    

GAME = {
    'current_room' : ROOMS['Parlor'],
    'last_room' : None,
    'left_hand' : None,
    'right_hand' : None
}
