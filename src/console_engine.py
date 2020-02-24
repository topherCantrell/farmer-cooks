
from game_engine import GameEngine

class ConsoleEngine(GameEngine):    
    
    def __init__(self):
        super().__init__()

    def get_input(self):
        '''Get the next command from the user
        
        Returns:
            the user's input
        '''
        # Get target objects and hands here. This is very game/hardware-specific
        return input('Command: ')
    
    def play_show_prompt(self,pr, eol=True):
        '''Output the prompt (audio or text)
        
        Args:
            pr: the prompt (audio,text)
            eol: True to print an eol
        '''
        if not eol:
            print(pr[1],end='')
            if pr[1].endswith(':'):
                print(' ',end='')
        else:
            print(pr[1])       
