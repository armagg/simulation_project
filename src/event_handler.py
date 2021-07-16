from queue import PriorityQueue

from dataclasses import dataclass
q = PriorityQueue()

@dataclass
class Event:
    end_time: int
    costumer_id: int

@dataclass
class CostumerServed(Event):
    store_id: int
    worker_id: int


@dataclass
class CostumerExhausted(Event):  
    store_id: int
    worker_id: int
    