import pulp
import numpy as np
import fractions
def data_pre(vec):
    for i in range(len(vec)):
        try:
            if isinstance(vec[i], str) and '/' in vec[i]:
                # Convert the string representation of a fraction to a floating-point number
                vec[i] = float(fractions.Fraction(vec[i]))
            else:
                # Convert other numerical strings to floating-point numbers
                vec[i] = float(vec[i])
        except ValueError as e:
            print(f"error when converting {vec[i]} to floating-point numbers: {e}")
    return vec

c=input('please input c:').split()
b=input('please input b:').split()
A=[]

for i in range(len(b)):
    A.append(input(f'please input A[{i}]:').split())

# data pre-processing
c = data_pre(c)
b = data_pre(b)
for i in range(len(A)):
    A[i] = data_pre(A[i])

# --------------------------reference cases(verify multiple solutions)--------------------------
# c = [-10, -20]
# b = [3, 8, 4]
# A = [[0.25, 0.4], [1, 0], [0, 1]]

# c=[-1,-1]
# b=[6,20]
# A=[[2,1],[4,5]]
# --------------------------reference cases(verify multiple solutions)--------------------------

# --------------------------reference cases(verify mixed integer programming)--------------------------
# c = [-2,-3,-4]
# b = [600, 60000]
# A = [[1.5, 3, 5], [280, 250, 400]]

# 课本习题6.2
# c = [-1,-1]
# b = [51/14, 1/3]
# A = [[1, 9/14], [-2, 1]]
# --------------------------reference cases(verify mixed integer programming)--------------------------

# --------------------------reference cases(verify scalable integer programming)--------------------------
# c = [-2,-66,70,-69,18,98,68,79,-87,-56,-17,-79,-37,4,42]
# b = [97,132,72,132,168,87,113,67,135,179,186,191,121,155,92]
# A = [[8,19,6,10,8,4,15,3,17,2,18,5,4,10,9],
#  [4,18,7,11,1,10,4,1,16,2,6,7,6,2,1],
#  [11,13,10,3,5,14,16,14,1,2,14,16,4,18,2],
#  [15,4,2,19,2,4,19,18,16,7,16,8,19,11,3],
#  [14,1,4,11,3,14,2,4,9,4,6,4,12,12,4],
#  [2,7,6,10,5,3,4,2,2,11,4,5,14,13,16],
#  [10,14,18,4,6,7,7,9,11,7,4,6,15,1,2],
#  [11,3,5,5,12,2,6,3,14,8,5,6,6,4,12],
#  [16,14,18,11,13,5,7,12,1,12,4,8,6,18,19],
#  [2,14,18,12,1,5,1,4,13,18,14,8,4,5,6],
#  [18,13,15,2,7,11,14,19,3,3,6,2,8,13,7],
#  [7,4,7,15,5,6,16,2,2,15,6,16,11,2,4],
#  [15,3,8,1,8,3,14,5,3,6,19,12,7,8,1],
#  [14,2,5,19,16,5,2,3,10,6,9,13,6,4,18],
#  [8,13,10,5,10,5,3,1,19,18,14,2,11,1,7]]
# --------------------------reference cases(verify scalable integer programming)--------------------------

def find_multiple_solutions():
    # Define the problem as an integer programming problem seeking to minimize the objective function, and solve it using the cutting-plane method
    prob = pulp.LpProblem("ILP", pulp.LpMinimize)

    # Define decision variables and their lower bounds, where the number of decision variables depends on the length of vector c
    variables = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(1, len(c) + 1)]

    # Define the objective function
    object_function = pulp.lpSum([c[i] * variables[i] for i in range(len(variables))])
    prob += object_function, "Objective"

    # Define constraint conditions
    constraints_list = []
    for i in range(len(b)):
        constraint = pulp.lpSum([A[i][j] * variables[j] for j in range(len(variables))]) <= b[i]
        constraints_list.append(constraint)
    for constraint in constraints_list:
        prob += constraint

    # First, use the cutting-plane method to find a solution
    prob.solve()
    solutions = [[int(pulp.value(variable)) for variable in variables]]

    # Save the solution and calculate the minimum value
    ans = np.sum(np.array(c) * np.array(solutions))

    # Find an integer characteristic vector
    intEigenvector = find_intEigenvector(c)
    right = 0
    left = 0
    # Search to the right until no solution is found
    while True:
        right += 1
        vec_to_verify = np.array(intEigenvector) * right + np.array(solutions[0])
        vec_to_verify = [int(x) for x in vec_to_verify]
        prob_other = prob.copy()
        prob_other += (variables[0] == vec_to_verify[0])
        prob_other.solve()
    # If there is no solution, then exit the current loop
        if prob_other.status == -1:
            break
        # continue
    # If a solution exists, verify if it matches the existing vector
        solutions_now = [int(pulp.value(variable)) for variable in variables]
        if np.array_equal(np.array(solutions_now), vec_to_verify):
            solutions.append(vec_to_verify)

    # Search to the left until no solution is found
    while True:
        left -= 1
        vec_to_verify = np.array(intEigenvector) * left + np.array(solutions[0])
        vec_to_verify = [int(x) for x in vec_to_verify]
        prob_other = prob.copy()
        prob_other += (variables[0] == vec_to_verify[0])
        prob_other.solve()
    # If there is no solution, then exit the current loop
        if prob_other.status == -1:
            break
    # If a solution exists, verify if it matches the existing vector
        solutions_now = [int(pulp.value(variable)) for variable in variables]
        if np.array_equal(np.array(solutions_now), vec_to_verify):
            solutions.append(vec_to_verify)

    return solutions, ans

def is_feasible_solution(vector, prob):
    # Check if each constraint condition is satisfied
    for constraint in prob.constraints.values():
        flag = (pulp.lpSum(vector) <= 0)
        if flag:
            return False

    # Check if the domain of each integer variable is satisfied
    for var in prob.variables():
        if var.cat == 'Integer' and not pulp.value(var).is_integer():
            return False

    return True


def find_intEigenvector(c):
    probV = pulp.LpProblem("ILPV")

    # Define decision variables and their lower bounds. The number of decision variables depends on the length of c
    variables = [pulp.LpVariable(f'y{i}', cat='Integer') for i in range(1, len(c) + 1)]

    # Define constraint conditions
    constraint = pulp.lpSum([c[j] * variables[j] for j in range(len(c))]) == 0
    probV += constraint
    epsilon = 0.1
    probV += variables[0] >= epsilon

    probV.solve()

    intEigenvector = [pulp.value(variable) for variable in variables]

    return intEigenvector


if __name__ == "__main__":
    solutions, ans = find_multiple_solutions()
    for solution in solutions:
        print("")
        print("Solution:")
        for i in range(len(solution)):
            print(f"x{i+1} = {solution[i]},", end="")
    print("")
    print(f"min = {ans}")
