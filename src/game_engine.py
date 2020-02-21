
import random

class GameEngine:
    
    def __init__(self):        
        self.ROOMS = {}
        self.COMMANDS = {
            'generalDescribeRoom' : self.general_describe_current_room,
            'generalGet'          : self.general_get,
            'say'                 : self.general_say,
            'goto'                : self.general_goto,
        }
        
        self.current_room = None
        self.left_hand = None
        self.right_hand = None
    
    def find_command(self,inp_words:list ,commands:list):
        '''Find the command that matches the given input words
        
        The command list is of the form: [
          "north", "script",
          "south", "script"
        ]
        
        Technically, the entries should be grouped (tuple or list), but this makes
        the syntax easier for humans.
        
        Args:
            inp_words: the list of input words
            commands: list of commands and scripts
        Returns:
            a command handler from the commands or None if not found
        '''
            
        # Debugging
        #print('##',inp_words,'##',commands)
        
        # Build a list of pairs: (command, number_of_wilds)
        matches = [] # List of (command,num_wilds)
        fewest_wilds = len(inp_words) # Highest possible value to start with
        for p in range(0,len(commands),2):
            target = commands[p] # This is the command string
            act = commands[p+1] # This is the script
            target_words = target.split(' ')
            if len(inp_words)!=len(target_words):
                # Must be same the length to match
                continue
            match = True # The initial value ... we check next
            num_wilds = 0        
            for i in range(len(inp_words)):
                if target_words[i]=='*':
                    # Matches everything
                    num_wilds += 1
                    continue
                if inp_words[i] != target_words[i]:
                    match = False
                    break
            # Add this to our list and maintain the fewest wilds (most specific command)
            if match:
                matches.append((act,num_wilds))
                if num_wilds<fewest_wilds:
                    fewest_wilds = num_wilds
        
        # Keep only the most specific matches
        for i in range(len(matches)-1,-1,-1):
            if matches[i][1]>fewest_wilds:
                del matches[i]
                
        if matches:        
            if len(matches)>1:
                raise Exception('Multiple command matches.')
            # Just one match ... return its script
            return matches[0][0]
        else:
            return None  
    
    def find_message(self,s: str):
        '''Find the requested message
        
        Messages can be defined inline (s would be the actual message here). Or they
        can be defined in the current room. If neither of those, then we look in the
        "default" room for global messages.
        
        Args:
            s: the message or message-reference
            
        Returns:
            the name of the audio file and the text (file,text)
        '''
            
        msg = None
        
        if s.startswith('<'):
            # This might be defined in-place
            msg = s    
            
        elif 'messages' in self.current_room and s in self.current_room['messages']:
            # No ... check a reference to the current room
            msg = self.current_room['messages'][s]
        
        elif 'messages' in self.ROOMS['default'] and s in self.ROOMS['default']['messages']:
            # No ... check the default (globals)
            msg = self.ROOMS['default']['messages'][s]
            
        if not msg:
            # Nowhere to be found
            raise Exception('I could not find a message with id: '+s)  
        
        # Allow for functions that generate messages
        if callable(msg):
            msg = msg()
        
        # Allow a list of messages -- pick one at random
        if isinstance(msg,list):
            msg=random.choice(msg)
            
        # Audio and text        
        i = msg.index('>')
        return (msg[1:i].strip(),msg[i+1:].strip())                 
    
    def execute_script(self,cmd_script,inp_words: list):
        '''Execute the target command script
        
        Args:
            cmd_script: the command script or list of command scripts
            
        Returns:
            true if the command was handled or false if the handler says it didn't work
        '''
        
        # For debugging
        #print('##',cmd_script,'##',inp_words)
        
        if isinstance(cmd_script,list):
            for cmd in cmd_script:
                res = self.execute_script(cmd,inp_words)
                if not res:
                    return False
            return True
        else:
            cmd_words = cmd_script.split(' ')
            cmd = self.COMMANDS[cmd_words[0]]
            return cmd(cmd_words,inp_words)    
    
    def general_describe_current_room(self,_cmd_words=None,_inp_words=None):
        '''Describe the current room (LOOK)
        '''
            
        # Room description
        room = self.current_room
        pr = self.find_message(room['description'])
        self.play_show_prompt(pr)
        
        # Objects in room
        for obj in room['objects']:
            pr = self.find_message(obj['long'])
            self.play_show_prompt(pr)
            
        # Objects in hands
        if self.left_hand:
            pr = self.find_message('miscLeftHand')
            self.play_show_prompt(pr, False)
            pr = self.find_message(self.left_hand['short'])
            self.play_show_prompt(pr)
            
        if self.right_hand:
            pr = self.find_message('miscRightHand')
            self.play_show_prompt(pr, False)
            pr = self.find_message(self.right_hand['short'])
            self.play_show_prompt(pr)
    
    #
    # General command handlers (common things)
    #
            
    def general_get(self,_cmd_words=None,_inp_words=None):
        print('TODO here')
    
    def general_say(self,cmd_words,_inp_words=None):
        pr = self.find_message(cmd_words[1])
        self.play_show_prompt(pr)
        
    def general_goto(self,cmd_words,_inp_words=None):
        self.current_room = self.ROOMS[cmd_words[1]]
        self.general_describe_current_room()
            
    def main_loop(self):
    
        # Print the current room
        self.general_describe_current_room()
        
        while True:    
            
            room = self.current_room
            
            # Get the input words
            inp = self.get_input()
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
            
            # Debugging        
            #print('*',inp_words,'*')
            
            handled = False
            
            # First try the room's commands
            cmd_script = self.find_command(inp_words,room['commands'])
            if cmd_script:
                handled = self.execute_script(cmd_script,inp_words)
                
            # If not, fall back on the default commands 
            if not handled:
                cmd_script = self.find_command(inp_words,self.ROOMS['default']['commands'])
                if not cmd_script:
                    cmd_script = 'say miscDontUnderstand'  
                handled = self.execute_script(cmd_script,inp_words)