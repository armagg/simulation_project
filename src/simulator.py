from typing import List
from src.event_handler import CostumerServed, Event
from src.models import Costumer, CostumerGenerator, Reception, SharifPlus
from time import sleep, perf_counter


class Simulator:
    def __init__(self, costomer_generator: CostumerGenerator, sharif_plus: SharifPlus, \
         reception: Reception):
        self.costomer_generator = costomer_generator
        self.sharif_plus = sharif_plus
        self.reception = reception
        self.costumer_location = {}
        self.ordered_costumer = {}
        self.served_costumer = 0
        self.time = 0
        self.events = {}

    def add_events(self, events: List[Event]):
        for event in events:
            if event.end_time in self.events:
                self.events[event.end_time].append(event)
            else:
                self.events[event.end_time] = [event]

    def run_events(self):
        if self.time in self.events:
            events: List[Event] = self.events[self.time]
            for event in events:
                if type(event) == CostumerServed:
                    self.sharif_plus.shops[event.shop_id].free_worker(event.worker_id)
                    self.ordered_costumer.pop(event.costumer_id)
                else:
                    pass
            self.events.pop(self.time)

    def add_ordered_costumers(self, costumers: List[Costumer]):
        for costumer in costumers:
            self.ordered_costumer[costumer.id] = costumer
            self.served_costumer += 1

    def run(self, number_of_costumer: int):
        start = perf_counter()
        while self.served_costumer < number_of_costumer:
            costumers = self.costomer_generator.get_costomer(self.time)
            self.reception.add_to_queue(costumers)
            costumers = self.reception.serve()
            self.sharif_plus.add_to_queue(costumers)
            # print(f'queue len  is : {len(self.sharif_plus.shops[0].pq.queues[0])}')
            events, costumers = self.sharif_plus.serve(self.time)
            self.add_events(events)
            self.add_ordered_costumers(costumers)
            self.run_events()

            self.time += 1
            # if self.time % 100000 == 0:
            print(f'time is :{self.time}')
            sleep(1.5)
                # print(perf_counter() - start)
