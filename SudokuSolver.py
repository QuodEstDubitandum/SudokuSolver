from ortools.sat.python import cp_model
from csv import reader
from csv import writer

model = cp_model.CpModel()
x=[]
for i in range(81):
    x.append(model.NewIntVar(1,9,'x[{}]'.format(i)))

# reading input sudoku
f = open('input.csv','r')
csv_reader = reader(f)
input_list=[]
for row in csv_reader:
    input_list += row
f.close()

# changing the (by the input determined) x[i]
for i in range(81):
    if int(input_list[i])!=0:
        x[i]=int(input_list[i])

# row elements have to be unique    
for i in range(9):
    for j in range(9):
        for k in range(j+1,9):
            model.Add(x[9*i+j]!=x[9*i+k])

# column elements have to be unique
for i in range(9):
    for j in range(9):
        for k in range(j+1,9):
            model.Add(x[9*j+i]!=x[9*k+i])
            
# unpacking grids into a new list so we can compare row-wise
y=[]
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                y.append(x[27*i+3*j+9*k+l])
                
# grid elements (in rows now) have to be unique                
for i in range(9):
    for j in range(9):
        for k in range(j+1,9):
            model.Add(y[9*i+j]!=y[9*i+k])
                
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL:
    print('Solver successful')
else:
      print('Error occurred')  

# writing the solution back into a csv file 
g = open('output.csv','w')
csv_writer = writer(g,delimiter=',',lineterminator='\n')
solution=[]
for i in range(9):
    for j in range(9):
        solution.append(str(solver.Value(x[9*i+j])))
    csv_writer.writerow(solution)
    solution=[]
g.close()
