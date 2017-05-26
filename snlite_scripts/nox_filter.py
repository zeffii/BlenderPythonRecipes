"""
in verts_in v
in floats_in s
in order s d=3 n=2
out verts_out v
out floats_out s
"""

def nox_filter(data, order=2):
    """
    - order >= 2
    - data has two modes, vectors and numbers
    """
    fdata = []
    add = fdata.append
    
    if not len(data) or order in {0, 1}:
        pass
    elif isinstance(data[0], (list, tuple)) and len(data[0]) == 3:
        ...
    elif isinstance(data[0], (float, int)):
        """
        currently add first n and last n are not mixed properly
        
        """
        # add first n
        for i in range(order+1):
            if i == 0:
                B = data[0]
            else:
                data_to_avg = data[0+i:i+order-1]
                num_items = len(data_to_avg)
                add(sum(data_to_avg)/num_items)

        # add middle n
        for i in range(order-1, len(data)-order):
            fk = data[i:i+order]
            add(sum(fk) / order)

        # add last n
        for i in range(-(order)+1, 0, 1):
            if i == -1:
                add(data[-1])
            else:
                a = len(data)-order
                data_to_avg = data[a-(order+i):]
                num_items = len(data_to_avg)
                add(sum(data_to_avg)/num_items)                
        
    return fdata

order = min(order, 40)

if verts_in:
    for val_list in verts_in:
        verts_out.append(nox_filter(val_list, order))
    
if floats_in:
    for val_list in floats_in:
        floats_out.append(nox_filter(val_list, order))
