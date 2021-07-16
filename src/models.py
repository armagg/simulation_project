from typing import List
from collections import deque
from src.event_handler import CostumerServed, CostumerExhausted
from src.variables import *

class Costumer:
    def __init__(self, id, exhusting_rate, arrival_time, priority=None):
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


class CostumerGenerator():
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
    def __init__(self, number_of_priorities=5) -> None:
        self.number_of_priorities = number_of_priorities
        self.queues = [deque() for _ in range(number_of_priorities)]

    def add_to_queue(self, person: Costumer):
        self.queues[person.priority].append(person)

    def get_all_objects():
        pass

    def remove(self, id: int = None, person: Costumer = None):
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

    def pop(self, n=1):
        persons = []
        for i in range(len(self.queues) - 1, -1, -1):
            if len(self.queues[i]) > 0:
                persons.append(self.queues[i].popleft())
            if len(persons) == n:
                break
        return persons

    def get_number_in_queue(self, priority):
        return len(self.queues[priority])

    def get_total_numer(self):
        total = 0
        for i in range(self.number_of_priorities):
            total += self.get_number_in_queue(i)
        return total


class Reception():
    def __init__(self, miu: float) -> None:
        self.pq = PriorityQueue()
        self.miu = miu

    def serve(self):
        this_time_serve = get_poisson_variable(self.miu)
        number_in_queue = self.pq.get_total_numer()
        if this_time_serve > number_in_queue:
            this_time_serve = number_in_queue
        costomers = []
        for _ in range(this_time_serve):
            costomers.append(self.pq.pop()[0])
        return costomers

    def add_to_queue(self, costomers: list):
        for costumer in costomers:
            self.pq.add_to_queue(costumer)


class Worker:
    def __init__(self, id, miu) -> None:
        self.busy = False
        self.miu = miu
        self.costumer_id = None
        self.id = id

    def cook(self, costumer_id):
        self.busy = True
        self.costumer_id = costumer_id
        return get_poisson_variable(self.miu)

    def free(self):
        self.busy = False
        self.costumer_id = None


class Shop:
    def __init__(self, id, mius) -> None:
        self.pq = PriorityQueue()
        self.workers: list[Worker] = []
        for miu in mius:
            self.workers.append(Worker(miu))
        self.total_workers = len(mius)
        self.free_workers = self.total_workers
        self.id = id

    # todo: lower the bar with one time sort
    def get_sorted_worker(self):
        sorted_workers = sorted(
            self.workers, key=lambda x: x.miu, reverse=True)
        return sorted_workers

    def serve(self, time):
        events = []
        if self.free_workers > 0 and self.pq.get_total_numer() > 0:
            costumers = self.pq.pop(n=self.free_workers)
            workers: list[Worker] = [
                w for w in self.get_sorted_worker() if w.busy == False]
            for i, costumer in enumerate(costumers):
                events.append(CostumerServed(
                    time + workers[i].cook(costumer_id=costumer.id),
                    costumer.id,
                    self.id,
                    workers[i].id))
                self.free_workers -= 1
        return events

    def free_worker(self, worker_id):
        self.free_worker +=1
        for worker in self.workers:
            if worker.id == worker_id:
                worker.free()
                break

    def add_to_queue(self, costumer: Costumer):
        self.pq.add_to_queue(costumer)

class SharifPlus:
    def __init__(self, workers_parameters) -> None:
        self.shops: List[Shop] = []
        for i, workers in enumerate(workers_parameters):
                self.shops.append(Shop(i, workers))
        self.number_of_shops = len(workers_parameters)
    
    def add_to_queue(self, costumers):
        for costumer in costumers:
            tmp = random.randint(0, self.number_of_shops - 1)
            self.shops[tmp].add_to_queue(costumer)
    
    def serve(self, time):
        for shop in self.shops:
            shop.serve(time)


if __name__ == '__main__':
    # g = CostomerGenerator(10, 100)
    # r = Reception(10)
    # l = g.get_costomer(1)
    # r.add_to_queue(l)
    # print(r.pq.queues)
    # e()
    # print(r.pq.queues)
    pass
