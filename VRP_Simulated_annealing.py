import random
from VRP_Metropolis import metropolis

DEPTH = 20
T = 2
ALPHA = 0.3

def generate_random_solution(city_number, car_number):
    city_number -= 1
    k_pick = [0]*car_number
    vehicle_route = [list() for _ in range(car_number)]
    remaining = [i for i in range(1, city_number+1)]
    for i in range(car_number-1):
        if city_number-sum(k_pick) != car_number - i:
            k_pick[i] = random.randint(1, city_number-sum(k_pick)-(car_number-(i+1)))
        else:
            k_pick[i] = 1
    k_pick[-1] = city_number - sum(k_pick)
    for i in range(len(k_pick)):
        vehicle_route[i].append(0)
        for _ in range(k_pick[i]):
            ran_choice = random.choice(remaining)
            vehicle_route[i].append(ran_choice)
            remaining.remove(ran_choice)
    return vehicle_route

def value(route, cost):
    length_of_route = [sum([cost[route[i][j]][route[i][j+1]] for j in range(len(route[i])-1)]) for i in range(len(route))]
    return max(length_of_route)

def get_input():
    city_number, car_number = map(int, input().split())
    cost = []
    city_number += 1
    for _ in range(city_number):
        cost.append(list(map(int, input().split())))
    return (city_number, car_number, cost)

def simulated_annealing(city_number, car_number, cost):
    s = generate_random_solution(city_number, car_number)
    t = T
    s_star = s.copy()
    for _ in range(DEPTH):
        s = metropolis(cost, s, t)
        if value(s, cost) < value(s_star, cost):
            s_star = s
        t = t*ALPHA
    return s_star

def main():
    city_number, car_number, cost = get_input()
    ans = simulated_annealing(city_number, car_number, cost)
    print(car_number)
    for i in range(len(ans)):
        print(len(ans[i]))
        for city in ans[i]:
            print(city, end = ' ')
        print()
    print('Value:',value(ans, cost))


if __name__ == '__main__':
    main()
