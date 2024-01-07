from random import randint
import pyperclip

def generate_cost(n, k):
    n = n+1
    cost = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(len(cost)):
        for j in range(i+1,len(cost)):
            cost[i][j] = cost[j][i] = randint(0,100)
    return cost

if __name__ == '__main__':
    res = input('> ').split()
    n = int(res[0])
    k = int(res[1])
    a = generate_cost(n, k)
    w = f'{n} {k}\n'
    for a in generate_cost(n, k):
        w += ' '.join(list(map(str, a))) + '\n'
    pyperclip.copy(w)
