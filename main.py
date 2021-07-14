def get_inputs():
    tmp = input().strip().split(', ')
    n, landa, miu, alpha = int(tmp[0]) , *(float(tmp[i]) for i in range(1, 4))
    workers_parametes = []
    for _ in range(n):
        workers_parametes.append(list(map(float, input().strip().split(', '))))
    
    return (landa, miu, alpha, workers_parametes) 


def prepare(landa, miu, alpha, workers_parametes):
    # print(alpha, miu, workers_parametes)
    pass
if __name__ == '__main__':
    prepare(*get_inputs())