import random, math
import numpy as np

#TODO: get variable and distributions with a function call 

def get_poisson_variable(miu):
    value = np.random.poisson(miu)
    return math.floor(value)

def get_exponential_variable(alpha):
    value =  np.random.exponential(alpha)
    return math.floor(value)


def generate_costumer_priority():
        rand = random.randint(0, 99)
        if rand < 50 : 
            return 0
        elif rand < 70:
            return 1
        elif rand < 85:
            return 2
        elif rand < 95:
             return 3
        else:
            return 4

def init_data():
    pass

2, 10, 10, 100                               
1, 1, 3, 15, 12, 4, 2, 5, 4, 1
1, 1, 3, 15, 12, 4, 2, 5, 4, 1
