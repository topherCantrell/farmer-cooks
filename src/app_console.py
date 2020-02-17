
# Commands:
#   - north, east, south, west
#   - action, look
#   - use left/right objInHand ("-" for nothing)
#   - get left/right objToGet objInHand ("-" for nothing)
#   - drop left/right objInHand ("-" for nothing)

import random

from FARM import ROOMS, GAME

def get_input():
    # Get target objects and hands here. This is very game-specific
    return input('Command: ')

def find_command(inp_words,commands):
    #print('##',inp_words,'##',commands)
    matches = []    
    fewest_wilds = len(inp_words)
    for p in range(0,len(commands),2):
        target = commands[p]
        act = commands[p+1]
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
            matches.append((act,num_wilds))
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
        
    msg = None
    
    # This might be defined in-place
    
    
    if s.startswith('<'):
        msg = s    
    elif 'messages' in GAME['current_room'] and s in GAME['current_room']['messages']:
        msg = GAME['current_room']['messages'][s]
    # Next, check the default messages
    elif 'messages' in ROOMS['default'] and s in ROOMS['default']['messages']:
        msg = ROOMS['default']['messages'][s]
    if msg:
        # TODO: check if it is callable
        if isinstance(msg,list):
            msg=random.choice(msg)        
        i = msg.index('>')
        return (msg[1:i].strip(),msg[i+1:].strip())
        
    # Nowhere to be found
    raise Exception('I could not find a message with id: '+s)       

def execute_script(cmd_script,inp_words):
    #print('##',cmd_script,'##',inp_words)
    if isinstance(cmd_script,list):
        for cmd in cmd_script:
            execute_script(cmd,inp_words)
        return True
    else:
        cmd_words = cmd_script.split(' ')
        cmd = COMMANDS[cmd_words[0]]
        cmd(cmd_words,inp_words)
        return True    

def general_describe_current_room(_cmd_words=None,_inp_words=None):
    # Room description
    room = GAME['current_room']    
    _,t = find_message(room['description'])
    print(t)
    # Objects in room
    for obj in room['objects']:
        _,t = find_message(obj['long'])
        print(t)
    # Objects in hand
    if GAME['left_hand']:
        _,t = find_message('miscLeftHand')
        print(t,end='')
        _,t = find_message(GAME['left_hand']['short'])
        print(t)
    if GAME['right_hand']:
        _,t = find_message('miscRightHand')
        print(t,end='')
        _,t = find_message(GAME['right_hand']['short'])
        print(t)
        
def general_get(_cmd_words=None,_inp_words=None):
    print('TODO here')

def general_say(cmd_words,_inp_words=None):
    _,t = find_message(cmd_words[1])
    print(t)
    
def general_goto(cmd_words,_inp_words=None):
    GAME['current_room'] = ROOMS[cmd_words[1]]
    general_describe_current_room()
    
COMMANDS = {
    'generalDescribeRoom' : general_describe_current_room,
    'generalGet' : general_get,
    'say' : general_say,
    'goto' : general_goto,
}

if __name__ == '__main__':

    general_describe_current_room()
    
    while True:    
        
        room = GAME['current_room']
        
        inp = get_input()
        inp_words = inp.split(' ')
        
        # The get/drop/use handlers need the object in the target hand (or '-')
        if inp_words:
            if inp_words[0]=='get':
                if len(inp_words)!=3:
                    inp_words=inp_words[0:1] # This will be an error
                    # TODO: append object in hand
            elif inp_words[0]=='drop' or inp_words[0]=='use':
                if len(inp_words)!=2:
                    inp_words=inp_words[0:1] # This will be an error
                    # TODO: append object in hand
                
        #print('*',inp_words,'*')
        
        handled = False
        cmd_script = find_command(inp_words,room['commands'])
        if cmd_script:
            handled = execute_script(cmd_script,inp_words)
            
        if not handled:
            cmd_script = find_command(inp_words,ROOMS['default']['commands'])
            if not cmd_script:
                cmd_script = 'say miscDontUnderstand'  
            handled = execute_script(cmd_script,inp_words)

