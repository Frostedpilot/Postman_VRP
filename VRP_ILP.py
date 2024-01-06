#Import library
from ortools.linear_solver import pywraplp

#Input
city_number,car_number = map(int,input().split())
cost = []
city_number+=1
for i in range(city_number):
    cost.append(list(map(int, input().split())))


def main(cost):
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        return

    infinity = solver.infinity()

    # x and y are integer non-negative variables.
    VRP_x = [[[solver.IntVar(0,1,'VRP_x['+str(i)+","+str(j)+","+str(k)+"]") for k in range(city_number)] for j in range(city_number)] for i in range(car_number)]
    t = [[solver.IntVar(0,city_number,'t['+str(i)+","+str(j)+"]") for j in range(city_number)] for i in range(car_number)]

    print("Number of variables =", solver.NumVariables())

    #Remove (i,j) route
    for i in range(car_number):
        solver.Add(sum(VRP_x[i][k][k] for k in range(city_number))<=0)

    #A demand node is met once, by a single vehicle           
    for k in range(1,city_number):
        solver.Add(sum(VRP_x[i][j][k] if j!=k else 0 for j in range(city_number) for i in range(car_number) )<=1)
        solver.Add(sum(VRP_x[i][j][k] if j!=k else 0 for j in range(city_number) for i in range(car_number) )>=1)

    #All of cars must start and finish
    for i in range(car_number):
        solver.Add(sum(VRP_x[i][0][k] for k in range(city_number))<=1)
        solver.Add(sum(VRP_x[i][k][0] for k in range(city_number))<=1)
        solver.Add(sum(VRP_x[i][0][k] for k in range(city_number))>=1)
        solver.Add(sum(VRP_x[i][k][0] for k in range(city_number))>=1)
    
    #Moi thanh pho chi duoc phan cho 1 xe
    #Outcoming
    for i in range(car_number):
        for j in range(city_number):
            solver.Add(sum(VRP_x[i][j][k] if j!=k else 0 for k in range(city_number)) <= 1 ) #Outcoming
    
    #Enter p also exit p
    for i in range(car_number):
        for j in range(city_number):
            solver.Add(sum(VRP_x[i][j][k] for k in range(city_number)) - sum(VRP_x[i][k][j] for k in range(city_number)) <= 0 )
            solver.Add(sum(VRP_x[i][j][k] for k in range(city_number)) - sum(VRP_x[i][k][j] for k in range(city_number)) >= 0 )
    
    #Eliminate subtours
    for i in range(car_number):
        for j in range(city_number):
            for k in range(city_number):
                if j!=k and (j!=0 and k!= 0):
                    solver.Add(-t[i][k]+t[i][j]+1-(2*city_number)*(1-VRP_x[i][j][k])<=0)
    print("Number of constraints =", solver.NumConstraints())

    objective = solver.IntVar(0,infinity, 'objective')
    for i in range(car_number):
        solver.Add(sum([VRP_x[i][j][k] * cost[j][k] for k in range(city_number) for j in range(city_number)])-objective<=0)
    
    solver.Minimize(objective)

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        tour = list()
        next_city = 0
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
        print(f"\nProblem solved in {solver.wall_time():d} milliseconds\n")
        return tour, solver.Objective().Value()
    else:
        print("The problem does not have an optimal solution.")


tour, mininmax_distance = main(cost)
print(car_number)
print(mininmax_distance)
for i in range(len(tour)):
    print(len(tour[i]))
    for city in tour[i]:
        print(city, end = ' ')
    print()

