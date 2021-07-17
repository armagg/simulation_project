from src.simulator import Simulator
from src.models import CostumerGenerator, Reception, SharifPlus

N = 1000

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
    return Simulator(
        custumer_generator,
        sharif_plus,
        reception
    )


if __name__ == '__main__':
    simulator = prepare(*get_inputs())
    simulator.run(N)