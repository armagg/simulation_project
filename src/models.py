import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collections import deque
from src.variables import *
class Costumer:
    def __init__(self, id, exhusting_rate, arrival_time, priority = None) -> None:
        self.id = id
        self.arrival_time = arrival_time
        self.exhust_time = get_exponential_variable(exhusting_rate)

        if priority:
            self.priority = priority
        else:
            self.priority = generate_costumer_priority()
    
    def __repr__(self) -> str:
        return f'costomer_id: {self.id}'
    
    def __eq__(self, o: object) -> bool:
        if self.id == o.id:
            return True
        else:
            return False
    

class CostomerGenerator():
    def __init__(self, landa, exhausting_rate):
        self.landa = landa
        self.id = 0
        self.exhausting_rate = exhausting_rate
    
    def get_costomer(self, time): 
        costumers = []
        for _ in range(get_poisson_variable(self.landa)):
            costumers.append(Costumer(self.id, self.exhausting_rate, time))
            self.id += 1
        return costumers
    
    
class PriorityQueue:
    def __init__(self, number_of_priorities = 5) -> None:
        self.queues = [deque() for _ in range(number_of_priorities)]

    def add_to_queue(self, person: Costumer):
        self.queues[person.priority].append(person)
    
    def get_all_objects():
        pass

    def remove(self, id: int= None, person: Costumer= None):
        if not id and not person:
            raise TypeError('you should provide at least one the id or\
                 person')
        if person:
            self.queues[person.priority].remove(person)
        else:
            for queue in self.queues:
                for element in list(queue):
                    if element.id == id:
                        queue.remove(element)
    
    def pop(self):
        for i in range(len(self.queues) - 1, -1, -1):
            if len(self.queues[i]) > 0 :
                return self.queues[i].popleft()
        raise ValueError
        
    
    
    def get_number_in_queue(self, priority):
        return len(self.queues[priority])

class Server:
    '''
    An abstract class for serving costumers with priority queues 
    
    '''

    def __init__(self) -> None:
        pass


class Reception():
    def __init__(self) -> None:
        pass

    def serve():
        pass

    def add_to_queue():
        pass


class Store:
    def __init__(self) -> None:
        pass
    
    def serve():
        pass



class Chef:
    def __init__(self) -> None:
        pass


if __name__ == '__main__':
 