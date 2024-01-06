from ortools.sat.python import cp_model
model = cp_model.CpModel()

city_number,car_number = map(int,input().split())
cost = []
city_number+=1
for i in range(city_number):
    cost.append(list(map(int, input().split())))

alpha = int(city_number/car_number) - 1
beta = int(city_number/car_number) + 2


def VRP(cost):
    #Khoi tao bien, diem den j co nam tren duong di cua xe i khong
    VRP_x = [[[model.NewIntVar(0,1,'VRP_x['+str(i)+","+str(j)+","+str(k)+"]") for k in range(city_number)] for j in range(city_number)] for i in range(car_number)]
    t = [[model.NewIntVar(0,city_number,'t['+str(i)+","+str(j)+"]") for j in range(city_number)] for i in range(car_number)]
    ##ADD CONSTRAINT##
    
    #A demand node is met once, by a single vehicle           
    for k in range(1,city_number):
        model.Add(sum(VRP_x[i][j][k] if j!=k else 0 for j in range(city_number) for i in range(car_number) )==1)

    #All of cars must start and finish
    for i in range(car_number):
        model.Add(sum(VRP_x[i][0][k] for k in range(city_number))==1)
        model.Add(sum(VRP_x[i][k][0] for k in range(city_number))==1)
    
    #Moi thanh pho chi duoc phan cho 1 xe
    #Outcoming
    for i in range(car_number):
        for j in range(city_number):
            model.Add(sum(VRP_x[i][j][k] if j!=k else 0 for k in range(city_number)) <= 1 ) #Outcoming
    
    #Enter p also exit p
    for i in range(car_number):
        for j in range(city_number):
            model.Add(sum(VRP_x[i][j][k] for k in range(city_number)) - sum(VRP_x[i][k][j] for k in range(city_number)) == 0 )
    
    #Eliminate subtours
    for i in range(car_number):
        for j in range(city_number):
            for k in range(city_number):
                if j!=k and (j!=0 and k!= 0):
                    model.Add(t[i][k]>=t[i][j]+1-(2*city_number)*(1-VRP_x[i][j][k]))
    
    # Create the objective function (minimize max distance)
    # objective = max([sum(VRP_x[i][j][k] * cost[j][k] for j in range(city_number) for k in range(city_number)) for i in range(car_number)])
    objective = model.NewIntVar(0,100000, 'objective')
    for i in range(car_number):
        model.Add(objective>=sum([VRP_x[i][j][k] * cost[j][k] for k in range(1,city_number) for j in range(city_number)]))
    # model.AddMaxEquality(objective, [sum([VRP_x[i][j][k] * cost[j][k] for k in range(city_number) for j in range(city_number)]) for i in range(car_number)])
    model.Minimize(objective)
    
    # Create a solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Extract the solution
        tour = list()
        for i in range(car_number):
            tour.append([])
            current_city = 0
            while True:
                tour[i].append(current_city)
                for j in range(city_number):
                    if solver.Value(VRP_x[i][current_city][j]) == 1:
                        next_city = j
                if next_city == 0:
                    break
                current_city = next_city
        for i in range(car_number):
            for j in range(city_number):
                for k in range(city_number):
                    print(solver.Value(VRP_x[i][j][k]), end = ' ')
                print()
            print("--------------")
        return tour, solver.ObjectiveValue()
tour, mininmax_distance = VRP(cost)
print(car_number)
print(mininmax_distance)
for i in range(len(tour)):
    print(len(tour[i]))
    for city in tour[i]:
        print(city, end = ' ')
    print()
