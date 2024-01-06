# Select first case
import random

DEPTH = 1000

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

def get_neighbour(cost, current):
    route = []
    for car in current:
        route += car
    for i in range(len(route)):
        if i == len(route)-1:
            if route[i-1] != 0:
                picked = route[i]
                route.pop(i)
                for j in range(1,len(route)+1):
                    route.insert(j, picked)
                    if value(revert(route), cost) < value(current, cost):
                        return revert(route)
                    route.pop(j)
                route.insert(i, picked)
            else:
                break
        else:
            if route[i] != 0 and route[i-1]+route[i+1] != 0:
                picked = route[i]
                route.pop(i)
                for j in range(1,len(route)+1):
                    route.insert(j, picked)
                    if value(revert(route), cost) < value(current, cost):
                        return revert(route)
                    route.pop(j)
                route.insert(i, picked)
    return current

def hill_climbing(city_number, car_number, cost):
    current = generate_random_solution(city_number, car_number)
    neighbour = []
    for i in range(DEPTH):
        # print(f'Iteration no. {i}')
        neighbour = get_neighbour(cost, current)
        if value(neighbour, cost) >= value(current, cost):
            return current
        current = neighbour
    return current

def main():
    city_number, car_number, cost = get_input()
    ans = hill_climbing(city_number, car_number, cost)
    print(car_number)
    for i in range(len(ans)):
        print(len(ans[i]))
        for city in ans[i]:
            print(city, end = ' ')
        print()

if __name__ == '__main__':
    main()
