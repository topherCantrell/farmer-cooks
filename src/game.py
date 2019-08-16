
ROOMS = {

    # The "default" room is for objects that are out of play, general messages, and the
    # general command handlers (that specific rooms can override).
    
    # Audio/Text messages are defined as
    # name:this is the text
    # where the name can be referenced in other places and is the name of the audio file (no file extension needed)
    
    "default" : {
        # List of objects in the room
        "objects" : [
            # The butter appears when you churn the milk
            {
                "id" : "butter", # Referenced by the game
                "short" : "objButterShort:butter", # The short description is what appears in the inventory
                "long" : "objButterLong:There is butter here.", # The long description appears with the room
                "stuck" : False, # False (the default) if you can move the object
                "hidden" : False # True if the object is hidden (can't be seen or targeted)
            }
        ],   
    
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
            "north" : "say miscNoWay", # No ":" in this ... this must be a message reference
            "south" : "say miscNoWay",
            "east" : "say miscNoWay",
            "west" : "say miscNoWay",
            # Gets
            # The wildcard will be the target object or "" if there is no object.
            "getLeft *" : "",            
            "getRight *" : "",
            # Drops
            "dropLeft *" : "",
            "dropRight *" : "",
            # Use
            "useLeft *" : "",
            "useRight *" : "",
            # Look
            "look" : "describeRoom",
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
               # These are processed before the "moveable" and "is empty" check.
               "getLeft churn" : "say getChurn",
               "getRight churn" : "say getChurn",
        },
          
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
    },
    
    

}

GAME = {
    'current_room' : ROOMS['Parlor'],
    'last_room' : None,
    'left_hand' : None,
    'right_hand' : None
}

def get_input():
    # Get target objects and hands here. This is very game-specific
    return input('Command: ')

def find_command(inp,commands):
    matches = []
    inp_words = inp.split(' ')
    fewest_wilds = len(inp_words)
    for target in commands:
        target_words = target.split(' ')
        if len(inp_words)!=len(target_words):
            # Must be same the length
            continue
        match = True
        num_wilds = 0        
        for i in range(len(inp_words)):
            if target_words[i]=='*':
                # Matches everything
                num_wilds += 1
                continue
            if inp_words[i] != target_words[i]:
                match = False
                break
        if match:
            matches.append((commands[target],num_wilds))
            if num_wilds<fewest_wilds:
                fewest_wilds = num_wilds
                
    for i in range(len(matches)-1,-1,-1):
        if matches[i][1]>fewest_wilds:
            del matches[i]
            
    if matches:
        return matches[0][0]
    else:
        return None    

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

# Processing here for objects, hands and empty/full

# Factory methods here to override

inp = get_input()
print('*',inp,'*')

# TODO wildcard search

def execute_script(cmd_script):
    print(':',cmd_script,':')
    return True

handled = False
cmd_script = find_command(inp,room['commands'])
if cmd_script:
    handled = execute_script(cmd_script)
    
if not handled:
    cmd_script = find_command(inp,ROOMS['default']['commands'])
    handled = execute_script(cmd_script)

