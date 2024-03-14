import random

def seed_random_data(input, seeded_data=[]):
    """ Return a new object with random data, where the randomness is based on a predefined set of data (seeded_data). """
    
    if not isinstance(seeded_data, list) or len(seeded_data) == 0:
        return
    
    if isinstance(input, list):
        data = []
        for item in input:
            data_item = seed_random_data(item) if isinstance(item, dict) else random.choice(seeded_data)
            data.append(data_item)
        return data
            
    elif isinstance(input, dict):
        input:dict
        new_dict = {}
    
        for key in input.keys():
            new_dict[key] = random.choice(seeded_data)
        return new_dict

    else:
        return random.choice(seeded_data)
    
def shuffle_data(data):
    """ Return shuffled data given a list or dict object. """
    
    if isinstance(data, list):
        random.shuffle(data) 
        return data
    elif isinstance(data, dict):
        keys = list(data.keys())
        random.shuffle(keys)  
        shuffled_dict = {key: data[key] for key in keys}
        return shuffled_dict
    else:
        raise ValueError("Input data must be a list or a dictionary")
