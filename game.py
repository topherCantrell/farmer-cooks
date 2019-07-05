ROOMS = {

    # The "default" room is for objects that are out of play, general messages, and the
    # general command handlers (that specific rooms can override).
    
    # Audio/Text messages are defined as
    # name:this is the text
    # where the name can be referenced in other places and is the name of the audio file (no file extension needed)
    
    "default" : {
        # List of objects in the room
        "objects" : {
            # The butter appears when you churn the milk
            "butter" : {
                "short" : "objButterShort:butter", # The short description is what appears in the inventory
                "long" : "objButterLong:There is butter here.", # The long description appears with the room
                "moveable" : True # True (the default) if you can move the object
            }
        },   
    
        # Search order for message refs:
        # 1. Defined (as in "say miscNo:No!!!!!")
        # 2. In the current room's "messages"
        # 3. In the "default" room's "messages"
    
        # General purpose messages
        "messages" : {
            "miscNoWay" : "You can't go that direction.",
            "miscHandEmpty" : "Your hand is empty",
            "miscLeftHand" : "In your left hand: ",
            "miscRightHand" : "In your right hand: "
        },
                
        # General command handlers
        "commands" : {
            # Default directions
            "north" : "miscNoWay", # No ":" in this ... this must be a message reference
            "south" : "miscNoWay",
            "east" : "miscNoWay",
            "west" : "miscNoWay",
            # Gets
            "getLeft *" : "",
            "getLeft_handFull" : "",
            "getRight *" : "",
            "getRight_handFull" : "",
            # Drops
            "dropLeft_handEmpty" : "",
            "dropLeft" : "",
            "dropRight_handEmpty" : "",
            "dropRight" : "",
            # Use
            "useLeft_handEmpty" : "",
            "useLeft" : "",
            "useRight_handEmpty" : "",
            "useRight" : "",
            # Look
            "look" : "",
        }
    },
    
    "Parlor" : {
        "description": "descParlor:This is the parlor. Churn is here. You can go south.",
          "commands" : {
              "south": "goto Porch",            
               "use pail_with_milk": [  
                   "move butter to _here",
                   "move pail_with_milk default",
                   "move pail to _here",
                   "say 'madeButter:You made butter! The cat drank some milk.'"
               ],
               "get _handEmpty" : "say 'The churn won\'t budge.'"
        },
          
        "messages" : {
            "wow" : "Big wow here!"
        }
    },
    
    

}

GAME = {
    'current_room' : ROOMS['Parlor'],
    'last_room' : None,
    'left_hand' : None,
    'right_hand' : None
}

ROOMS['Parlor']['objects'] = [ROOMS['default']['objects']['butter']]

def find_message(s):
    # TODO check if it is callable
    
    # This might be defined in-place
    i = s.find(':')
    if i>=0:        
        return (s[0:i],s[i+1:])
    # Next, check the messages for the room
    if 'messages' in GAME['current_room'] and s in GAME['current_room']['messages']:
        return (s,GAME['current_room']['messages'][s])
    # Next, check the default messages
    if 'messages' in ROOMS['default'] and s in ROOMS['default']['messages']:
        return (s,ROOMS['default']['messages'][s])     
    # Nowhere to be found
    raise Exception('I could not find a message with id: '+s)                
    
# Room description
room = GAME['current_room']
GAME['right_hand'] = ROOMS['default']['objects']['butter']
a,t = find_message(room['description'])
print(t)
# Objects in room
for obj in room['objects']:
    a,t = find_message(obj['long'])
    print(t)
# Objects in hand
if GAME['left_hand']:
    a,t = find_message('miscLeftHand')
    print(t,end='')
    a,t = find_message(GAME['left_hand']['short'])
    print(t)
if GAME['right_hand']:
    a,t = find_message('miscRightHand')
    print(t,end='')
    a,t = find_message(GAME['right_hand']['short'])
    print(t)

