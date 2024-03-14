def get_nested_value(dictionary, keys):
    for key in keys:
        if isinstance(dictionary, dict) and key in dictionary:
            dictionary = dictionary[key]
        else:
            return None
    return dictionary

def invert_dict(dictionary:dict) -> dict:
    temp_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, dict) or isinstance(value, list):
            pass
        else: 
            temp_dict.update({value: key})
    return  temp_dict


def find_dict_list_duplicates(list_of_dicts:list, key_to_check:str):
    """
    Given a list of dictionaries, return duplicate items with the associated key.
    """
    
    from collections import defaultdict

    value_occurrences = defaultdict(list)

 
    for index, item in enumerate(list_of_dicts):
        value = item.get(key_to_check)
        if value:
            value_occurrences[value].append(index)
 
    duplicate_items = [item for indices in value_occurrences.values() if len(indices) > 1 for item in (list_of_dicts[i] for i in indices)]

    return duplicate_items


def safe_pop(dictionary:dict, keys:list):
    """ 
    Safely remove the specified keys in a dictionary.
    """
    if not isinstance(keys, list):
        keys = [keys]

    for key in keys:
        if key in dictionary:
            dictionary.pop(key)
    

