def max_length_of_route(route, cost):
    length_of_route = [sum([cost[route[i][j]][route[i][j+1]] for j in range(len(route[i])-1)]) for i in range(len(route))]
    return max(length_of_route)
def greedy_criterion(car_number, cost, vehicle_route, remain_cities):
    chosen_car = 0
    chosen_city = 0
    minimax_value = 9999
    for i in range(car_number):
        for city in remain_cities:
            vehicle_route[i].append(city)
            if max_length_of_route(vehicle_route, cost) < minimax_value:
                chosen_car = i
                chosen_city = city
                minimax_value = max_length_of_route(vehicle_route, cost)
            vehicle_route[i].pop()
    vehicle_route[chosen_car].append(chosen_city)
    remain_cities.remove(chosen_city)

def greedy(city_number, car_number, cost):
    remain_cities = [i for i in range(1,city_number)]
    vehicle_route = []
    for i in range(car_number):
        vehicle_route.append([0])
    while True:
        greedy_criterion(car_number, cost, vehicle_route, remain_cities)
        if len(remain_cities) == 0:
            break
    return vehicle_route

def main():
    #Input
    city_number,car_number = map(int,input().split())
    cost = []
    city_number+=1
    for i in range(city_number):
        cost.append(list(map(int, input().split())))
    remain_cities = [i for i in range(1,city_number)]
    vehicle_route = []
    for i in range(car_number):
        vehicle_route.append([0])
    while True:
        greedy_criterion(car_number, cost, vehicle_route, remain_cities)
        if len(remain_cities) == 0:
            break
    print(car_number)
    for i in range(len(vehicle_route)):
        print(len(vehicle_route[i]))
        for city in vehicle_route[i]:
            print(city, end = ' ')
        print()
