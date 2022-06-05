from ortools.linear_solver import pywraplp
import csv

def LinearProgrammingExample():
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    data = []
    with open('nutrientData.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader: 
            data.append(row[1:])

    #preprocess; ensures entries do not contain strings, aside from names.
    for sett in data:
        for idx in range(len(sett)):
            if idx == 0:
                continue
            length = len(sett[idx])
            if '.' in sett[idx]: #If the only non-numeric value is a zero, it is a float. 
                if len(sett[idx]) - 1 == length - 1:
                    sett[idx] = float(sett[idx])
                    continue
            if sett[idx].isnumeric():
                sett[idx] = float(sett[idx])
            else:
                sett[idx] = 0
    
    variables = []
    #Initialize solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
   
    i = 0
    my_dict = {}
    
    while i < len(data):
        # dictionary with string value and object key. Entry "banana" holds banana object for solver.
        entry = data[i][0]
        
        my_dict[entry] = solver.NumVar(0, solver.infinity(), entry)
        i+=1

    print('Number of variables =', solver.NumVariables())

    vitaminA = calories = sugar = calcium = sodium = carbo = iron = protein = objective = 0
    
    i = 0
    while i < len(data):
            # calories > 0, otherwise we get a lot of water varieties.
            if (data[i][2] >0):
                entry = data[i][0]
                #These are the equations. the my_dict[entry] is the unknown 'variable'
                # for intsnace, iron = B*iron quantity + A* iron +... where amounts of B and A are not known.
                calories += my_dict[entry] * data[i][2]
                protein += my_dict[entry] * data[i][3]
                carbo += my_dict[entry] * data[i][6]
                calcium += my_dict[entry] * data[i][9]
                iron += my_dict[entry] * data[i][10]
                vitaminA += my_dict[entry] * data[i][19]
            
                # one item max restraint, 100 kilo max of each item
                solver.Add(my_dict[entry] <=1)
                
                # equation for sugar, the objective we are minimizing
                objective += my_dict[entry]*data[i][8]
            i+=1

    # the constraints:
    solver.Add(vitaminA >= 700)
    solver.Add(calories <= 2000.0)
    solver.Add(calories >= 1500.0)
    solver.Add(calcium >=2000.0)
    solver.Add(carbo <= 130)
    solver.Add(iron >= 7)
    #solver.Add(objective >= 80)
    solver.Add(protein >= 40)


    #Objective:
    solver.Minimize(objective)

    

    print('Number of constraints =', solver.NumConstraints())
    # Solve the system using simplex
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Sugar =', solver.Objective().Value())

        i = 0
        for item in my_dict.values():
            
            if(item.solution_value() >0):
                print(item, item.solution_value())
            i+=1

    else:
        print('The problem does not have an optimal solution.')
        
    print('total calories:', calories.solution_value())
    print('total carbs:', carbo.solution_value())
    print('total calcium:', calcium.solution_value())
    print('total iron:', iron.solution_value())
    print('total vitamina:', vitaminA.solution_value())

    
    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    #print('Problem solved in %d iterations' % solver.iterations())
LinearProgrammingExample()
