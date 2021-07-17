from src.models import Costumer




class SampleLength:
    def __init__(self) -> None:
        pass

    def sample_main(self):
        pass

    def sample_sharifplus(self):
        pass

class CostumerTimes:
    def __init__(self, number_to_dump= None, destination_file= None) -> None:
        self.number_to_dump = number_to_dump
        self.des = destination_file
        self.tmp_data = {}
        self.data = [[] for _ in range(5)] #frist dimention is pr and second is 0: total_time, 1:total queue time, 2  
        self.exhaust_tmp_data = {}
        self.number_of_exhuated_costomers = 0
        self.total_time_avg = [0 for _ in range(5)]
        self.total_time_num = [0 for _ in range(5)]
        self.queue_time_avg = [0 for _ in range(5)]
        self.queue_time_num = [0 for _ in range(5)]
    def compute_averages(self):
        for i in range(5):
            sum_ = 0
            for j in self.data[i][1]:
                sum_ += j 
            self.total_time_avg[i] = self.total_time_num[i] * self.total_time_avg[i] + sum_
            self.total_time_num[i] += len(self.data[i])
            self.total_time_avg[i] /= self.total_time_num[i]

            for j in self.data[i][0]:
                sum_ += j 
            self.queue_time_avg[i] = self.queue_time_num[i] * self.queue_time_avg[i] + sum_
            self.queue_time_num[i] += len(self.data[i])
            self.queue_time_avg[i] /= self.queue_time_num[i]
        del self.data
        self.data = [[] for _ in range(5)]


    def add_data(self, costumer: Costumer, time, costumer_id = None):

        

        if len(self.data[0]) > 1000: 
            self.compute_averages()
        if  costumer_id is None:
            costumer_id = costumer.id
        


        if costumer_id in self.tmp_data :
           self.tmp_data[costumer_id].append(time)
           if len(self.tmp_data[costumer_id]) == 5:
                tmp = self.tmp_data.pop(costumer_id)
                self.data[tmp[0]].append([tmp[4] - tmp[1], tmp[4] - tmp[3] + tmp[2] - tmp[1]])
        elif costumer:
            self.tmp_data[costumer.id] = [costumer.priority, time]
    
    def exhaust(self, id, time):
        self.number_of_exhuated_costomers +=1
        if id in self.tmp_data:
            length = len(self.tmp_data[id])
            if length == 2 or length == 3: # costumer exhaust in reception queue
                tmp = time - self.tmp_data[id][1]
                self.data[self.tmp_data[id][0]].append([tmp, tmp])
            elif length == 4:
                self.data[self.tmp_data[id][0]].append([time - self.tmp_data[id][1], self.tmp_data[id][3] - self.tmp_data[id][1]])
            self.tmp_data.pop(id)