from src.data_collectors import CostumerTimes, SampleLength
from typing import List
from src.event_handler import CostumerServed, Event
from src.models import Costumer, CostumerGenerator, Place, Reception, SharifPlus
from time import sleep, perf_counter


class Simulator:
    def __init__(self, costomer_generator: CostumerGenerator, sharif_plus: SharifPlus, \
         reception: Reception, costumer_time: CostumerTimes, sample_length: SampleLength):
        self.costomer_generator = costomer_generator
        self.sharif_plus = sharif_plus
        self.reception = reception
        self.costumer_place = {}
        self.ordered_costumer = {}
        self.served_costumer = 0
        self.time = 0
        self.events = {}
        self.costumer_time = costumer_time
        self.sample_length = sample_length

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
                    self.handle_service(event)
                    self.costumer_time.add_data(None, self.time, costumer_id=event.costumer_id)
                else:
                    self.handle_exhausting(event)
            self.events.pop(self.time)

    def handle_exhausting(self, event):
        self.costumer_time.exhaust(event.costumer_id, event.priority)
        if event.costumer_id in self.costumer_place:
            place = self.costumer_place[event.costumer_id]
            if place == Place.RECEPTION:
                self.reception.pq.remove(event.costumer_id)
            elif place == Place.QUEUE:
                self.sharif_plus.remove(event.costumer_id, event.priority)
            elif place == Place.WAIT:
                self.ordered_costumer.pop(event.costumer_id)

    def handle_service(self, event):
        self.sharif_plus.shops[event.shop_id].free_worker(event.worker_id)
        try:
            self.ordered_costumer.pop(event.costumer_id)
        except:
            pass
        try:
            self.costumer_place.pop(event.costumer_id)
        except:
            pass
    def add_ordered_costumers(self, costumers: List[Costumer]):
        for costumer in costumers:
            self.ordered_costumer[costumer.id] = costumer
            self.served_costumer += 1

    def update_place(self, costumers: List[Costumer], place: Place):
        for costumer in costumers:
            self.costumer_place[costumer.id] = place
            self.costumer_time.add_data(costumer, self.time)
        
    
    def sample_from_queues(self):
        self.sample_length.sample_main(self.reception.pq.get_number_in_queue())
        self.sample_length.sample_sharifplus()    
    
    
    def run(self, number_of_costumer: int):
        start = perf_counter()
        while self.served_costumer < number_of_costumer:
            #arrival of costumers
            costumers, events = self.costomer_generator.get_costomer(self.time)
            self.add_events(events)
            self.update_place(costumers, Place.RECEPTION)
            self.reception.add_to_queue(costumers)

            #reception of costumers
            costumers = self.reception.serve()
            self.update_place(costumers, Place.QUEUE)
            self.sharif_plus.add_to_queue(costumers)
            events, costumers = self.sharif_plus.serve(self.time)

            #handle events
            self.update_place(costumers, Place.WAIT)
            self.add_events(events)
            self.add_ordered_costumers(costumers)
            self.run_events()

            self.time += 1
            if self.time % 100000 == 0:
                print(f'time is :{self.time}')
                print(f'reception : {self.reception.pq.get_total_numer()}')
                print(f'served: {self.served_costumer}')
        print(perf_counter() - start)
