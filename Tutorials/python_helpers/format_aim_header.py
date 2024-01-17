def logtodict(log):
    """
    Converts a formatted AIM file log string into a dictionary.

    The function processes a multi-line string, where each line represents a key-value pair.
    Non-numeric values are stored as strings, and numeric values are converted to int or float.
    Lines starting with '!' are ignored.
    
    Parameters:
    log (str): A multi-line string representing the log.

    Returns:
    dict: A dictionary with keys and values extracted from the log.
    """
    lines = log.split('\n')
    log_dict = {}

    for line in lines:
        if line.strip() and not line.startswith('!'):
            parts = line.split('  ') # Two spaces to avoid issues with dates
            parts = [p.strip() for p in parts if p.strip()]
            if len(parts) == 2: # two parts is a normal key value pair
                key, value = parts[0], parts[1]
                # Convert numeric values to int or float
                if value.replace('.', '', 1).replace('-','',1).replace('e+','',1).isdigit():
                    value = float(value) if '.' in value else int(value)
                
            elif len(parts) > 2: # More parts is a 
                key, value = parts[0], [int(p) for p in parts[1:]]
            else:
                print(f'Warning: Unknown line type: {parts}')
            log_dict[key] = value

    return log_dict


def dicttolog(log_dict):
    """
    Converts a dictionary into a formatted AIM file log string.

    The function creates a string representation of the dictionary where each key-value pair
    is formatted and arranged on separate lines. Numeric values are right-justified and
    strings are left-justified.

    Parameters:
    log_dict (dict): A dictionary with keys and values to be logged.

    Returns:
    str: A formatted multi-line string representing the log.
    """
    log = '! Processing Log\n!\n!-------------------------------------------------------------------------------\n'
    split_line = '!-------------------------------------------------------------------------------\n'
    for key, value in log_dict.items():
        if isinstance(value, (int, float)):
            # Numeric values: key left-justified at 30, value right-justified at 50
            formatted_line = f'{key.ljust(30)}{value:>23}'
        elif isinstance(value, list):
            # List values: each element formatted individually
            formatted_line = f'{key.ljust(30)}{" ".join([f"{v:>10}" for v in value])}'
        else:
            # String values: key left-justified at 30
            formatted_line = f'{key.ljust(30)}{value}'.ljust(80)
        log += formatted_line + '\n'
        
        # Add a split line after certain keys for better readability
        if key in ['Orig-ISQ-Dim-um','Index Measurement','Default-Eval','HU: mu water','Standard data deviation']:
            log += split_line
    
    return log