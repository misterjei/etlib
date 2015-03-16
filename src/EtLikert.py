import exceptions

'''
@summary: Helper function to convert a numeric string to a Likert string
'''
def toLikert(value, scale):
    # convert the string to a float
    try:
        value = float(value)
    except exceptions.ValueError:
        return "-1"

    for limit in sorted(scale.keys(), reverse=True):
        if (value >= limit):
            return scale[limit]
    
    return "-1"

'''
@summary: Helper function to convert a Likert string to a number value
'''
def getLikertKey(value, scale):
    # convert the string to a float
    try:
        value = str(value).lower()
    except exceptions.ValueError:
        return "-1"

    for limit, likertString in scale.items():
        if (value == likertString.lower()):
            return limit
    
    return "-1"

'''
@summary: Helper function to convert a numeric string to a Likert index
'''
def getLikertIndex(value, scale):
    # convert the string to a float
    if isinstance(value, basestring):
        return sorted(scale.values()).index(value)
    elif isinstance(value, (int, long, float)):
        try:
            return sorted(scale.keys()).index(value)
        except:
            return -1
    else:
        return -1
