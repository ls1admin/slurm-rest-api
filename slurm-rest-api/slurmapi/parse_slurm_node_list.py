import re

def parse_all_lists(node_str_list):
    arr = []
    for node in node_str_list:
        l = parse_list(node)
        for item in l:
            if item not in arr:
                arr.append(item)
    return arr

def parse_list(node_str):
    arr = _parse_into_array(node_str)
    arr = _parse_comma_in_brackets(arr)
    arr = _parse_into_individual_nodes(arr)
    return arr

# Splits the list of nodes into an array of nodes.
# Don't split on comma's in brackets (handle that later)
def _parse_into_array(node_str):
    arr = re.split(r',(?![^\[\]]*\])', node_str)
    return arr

# break appart nodes that have comma delimiters in the node list
def _parse_comma_in_brackets(node_arr):
    new_arr = []
    for n in node_arr:
        if ',' in n:
            current = n
            while ',' in current:
                first = current.split(',',1)[0]
                rest = current.split(',',1)[1]
                first = first + ']'
                starter = first.split('[',1)[0]
                rest = starter + '[' + rest
                new_arr.append(first)
                current = rest
            new_arr.append(current)
        else:
            new_arr.append(n)

    return new_arr

# Change range nodes (i.e. [0-2]) into individual nodes
def _parse_into_individual_nodes(node_arr):
    new_arr = []
    for n in node_arr:
        if '[' not in n:
            new_arr.append(n)
        else:
            starter = n.split('[',1)[0]
            in_brackets = n.split('[',1)[1]
            in_brackets = in_brackets.split(']',1)[0]
            if '-' not in in_brackets:
                new_arr.append(starter + in_brackets)
            else:
                value_range = in_brackets.split('-',1)
                for x in range(int(value_range[0]), int(value_range[1]) + 1):
                    new_arr.append(starter + str(x))
                
    return new_arr
