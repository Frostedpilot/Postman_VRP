#Import library
from ortools.linear_solver import pywraplp

#Input
city_number,car_number = map(int,input().split())
cost = []
city_number+=1
for i in range(city_number):
    cost.append(list(map(int, input().split())))

def ILP_VRP(cost):
    solver = pywraplp.Solver.CreateSolver("SAT")
    infinity = solver.infinity()
    # if not solver:
    #     return
    #Initiate variable
    VRP_x = [[[solver.IntVar(0,1,'VRP_x['+str(i)+","+str(j)+","+str(k)+"]") for k in range(city_number)] for j in range(city_number)] for i in range(car_number)]
    t = [[solver.IntVar(0,city_number,'t['+str(i)+","+str(j)+"]") for j in range(city_number)] for i in range(car_number)]
    ##ADD CONSTRAINT##
    
    #A demand node is met once, by a single vehicle           
    for k in range(1,city_number):
        solver.Add(sum(VRP_x[i][j][k] if j!=k else 0 for j in range(city_number) for i in range(car_number) )==1)

    #All of cars must start and finish
    for i in range(car_number):
        solver.Add(sum(VRP_x[i][0][k] for k in range(city_number))==1)
        solver.Add(sum(VRP_x[i][k][0] for k in range(city_number))==1)
    
    #Moi thanh pho chi duoc phan cho 1 xe
    #Outcoming
    for i in range(car_number):
        for j in range(city_number):
            solver.Add(sum(VRP_x[i][j][k] if j!=k else 0 for k in range(city_number)) <= 1 ) #Outcoming
    
    #Enter p also exit p
    for i in range(car_number):
        for j in range(city_number):
            solver.Add(sum(VRP_x[i][j][k] for k in range(city_number)) - sum(VRP_x[i][k][j] for k in range(city_number)) == 0 )
    
    #Eliminate subtours
    for i in range(car_number):
        for j in range(city_number):
            for k in range(city_number):
                if j!=k and (j!=0 and k!= 0):
                    solver.Add(t[i][k]>=t[i][j]+1-(2*city_number)*(1-VRP_x[i][j][k]))
    # Create the objective function (minimize max distance)
    objective = solver.IntVar(0,infinity, 'objective')
    for i in range(car_number):
        solver.Add(objective>=sum([VRP_x[i][j][k] * cost[j][k] for k in range(1,city_number) for j in range(city_number)]))
    
    solver.Minimize(objective)
    print('Solve')
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        tour = list()
        for i in range(car_number):
            tour.append([])
            current_city = 0
            while True:
                tour[i].append(current_city)
                for j in range(city_number):
                    if VRP_x[i][current_city][j].solution_value() == 1:
                        next_city = j
                if next_city == 0:
                    break
                current_city = next_city
        for i in range(car_number):
            for j in range(city_number):
                for k in range(city_number):
                    print(VRP_x[i][j][k].solution_value(), end = ' ')
                print()
            print("--------------")
        return tour, solver.Objective().Value()
    else:
        print("No Solution")

tour, mininmax_distance = ILP_VRP(cost)
print(car_number)
print(mininmax_distance)
for i in range(len(tour)):
    print(len(tour[i]))
    for city in tour[i]:
        print(city, end = ' ')
    print()

    
    
    
