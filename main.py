from src.data_collectors import CostumerTimes, SampleLength
from src.simulator import Simulator
from src.models import CostumerGenerator, Reception, SharifPlus

N = 1000000

def get_inputs():
    tmp = input().strip().split(', ')
    n, landa, miu, alpha = int(tmp[0]) , *(float(tmp[i]) for i in range(1, 4))
    workers_parametes = []
    for _ in range(n):
        workers_parametes.append(list(map(float, input().strip().split(', '))))
    
    return (landa, miu, alpha, workers_parametes) 


def prepare(landa, miu, alpha, workers_parametes):
    custumer_generator = CostumerGenerator(landa, alpha)
    reception = Reception(miu)
    sharif_plus = SharifPlus(workers_parametes)
    costumer_time = CostumerTimes()
    sample_legth = SampleLength()
    return Simulator(
        custumer_generator,
        sharif_plus,
        reception,
        costumer_time,
        sample_legth
    )


if __name__ == '__main__':
    simulator = prepare(*get_inputs())
    simulator.run(N)
    print(simulator.costumer_time.number_of_exhuated_costomers)
    print(simulator.costumer_time.total_time_avg, simulator.costumer_time.queue_time_avg)

