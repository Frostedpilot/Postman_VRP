# Select first case
import random, math

DEPTH = 10000
T = 1 # Need to find a good t

def get_input():
    city_number, car_number = map(int, input().split())
    cost = []
    city_number += 1
    for _ in range(city_number):
        cost.append(list(map(int, input().split())))
    return (city_number, car_number, cost)

def revert(route):
    res = []
    cur = 0
    for i in range(1, len(route)):
        if route[i] == 0:
            res.append(route[cur:i])
            cur = i
    res.append(route[cur:])
    return res

def value(route, cost):
    length_of_route = [sum([cost[route[i][j]][route[i][j+1]] for j in range(len(route[i])-1)]) for i in range(len(route))]
    return max(length_of_route)

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

def get_neighbour(current):
    route = []
    for car in current:
        route += car
    while True:
        i = random.randint(1, len(route)-1)
        if i == len(route)-1:
            if route[i-1] != 0:
                break
        else:
            if route[i] != 0 and route[i-1]+route[i+1] != 0:
                break
    picked = route[i]
    route.pop(i)
    j = random.randint(1, len(route))
    route.insert(j, picked)
    return revert(route)

def metropolis(city_number, car_number, cost):
    current = generate_random_solution(city_number, car_number)
    print(current, value(current, cost))
    neighbour = []
    for i in range(DEPTH):
        # print(f'Iteration no. {i}')
        neighbour = get_neighbour(current)
        if value(neighbour, cost) < value(current, cost):
            current = neighbour
        else:
            if random.random() <= math.exp(-(value(neighbour, cost)-value(current, cost))/T):
                current = neighbour
    return current

def main():
    city_number, car_number, cost = get_input()
    ans = metropolis(city_number, car_number, cost)
    print(ans,'\n',value(ans, cost))

if __name__ == '__main__':
    main()
