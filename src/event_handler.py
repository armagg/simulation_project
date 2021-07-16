from queue import PriorityQueue
from enum import Enum
from dataclasses import dataclass
q = PriorityQueue()


# class EventType(Enum):
#     COSTUMER_EXHAUST = 'costomer_exhaust'
@dataclass
class CostumerServed:
    end_time: int
    costumer_id: int  
    store_id: int
    worker_id: int


@dataclass
class CostumerExhausted:
    end_time: int
    costumer_id: int  
    store_id: int
    worker_id: int
    