
def find_all_prompts(engine):
    
    ret = []
    
    for room in engine.ROOMS:
        data = engine.ROOMS[room]
        
        # Description
        if 'description' in data:
            pr = data['description']
            if pr.startswith('<'):
                ret.append(pr)
        
        # Objects
        for obj in data['objects']:            
            if 'long' in obj:
                pr = obj['long']
                if pr.startswith('<'):
                    ret.append(pr)
            if 'short' in obj:
                pr = obj['short']
                if pr.startswith('<'):
                    ret.append(pr)
            
        # Messages        
        if 'messages' in data:
            for mes in data['messages']:
                pr = data['messages'][mes]
                if isinstance(pr,list):
                    for p in pr:
                        if p.startswith('<'):
                            ret.append(p)
                else:
                    if pr.startswith('<'):
                        ret.append(pr)

    ret2 = []
    for r in ret:
        i = r.index('>')
        ret2.append( (r[1:i],r[i+1:].strip()) )        
        
    return ret2