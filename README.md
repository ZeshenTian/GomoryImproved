# Never Forget Solutions: Improve Gomory's Cutting Plane Method by One-Dimensional Linear Search
### Abstract
A common method for solving integer programming problems is the Gomory cutting plane method. However, this method has the issue of forgetting solutions, which motivated us to make improvements. We use the Schmidt orthogonalization method to determine the direction vector of the constraint conditions, and then perform a one-dimensional search in this direction to obtain all optimal solutions. Extensive instances of multiple integer programming problems demonstrate the correctness of our algorithm.

### Preface
1. We solve our problems using the `pulp` package.
2. We can solve both pure integer programming problems and mixed integer programming problems, and we can output all optimal solutions.
3. We define the problem as a minimization problem. To solve a maximization problem, one only needs to add a negative sign to each coefficient in the objective function and also add a negative sign to the final result.

### Input
The first line inputs the coefficient vector `c`, the second line inputs the constraint vector `b`, and each subsequent line inputs one row of the coefficient matrix `A`. Press Enter after the first and second lines, and the input will automatically stop after entering the number of rows equal to the length of `b`.

### Data Preprocessing
Convert the vectors `b` and `c` and every value in the matrix `A` from string type to float type using the `data_pre()` function.

### Problem Definition
1. Define the problem as a minimization problem.
2. Define all decision variables and their lower bounds using list comprehension and save them in the list `variables`.
3. Calculate the objective function by taking the dot product of the coefficient vector `c` and the vector `variables`.
4. Define the constraints by taking the dot product of the coefficient matrix `A` and the vector `variables`, and compare it with the constraint vector `b`.

### One-Dimensional Linear Search
1. Use the cutting plane method to find a solution and save the solution in the list `solutions`, and calculate the minimum value of this problem.
2. Use the Schmidt orthogonalization method to find a pure integer orthogonal vector `intEigenvector` of the coefficient vector `c`. Redefine this problem as an integer programming problem by defining the number of decision variables according to the number of variables and setting the constraint that the dot product of the coefficient vector `c` and the vector `variables` equals 0. To exclude the zero vector, add a constraint `x1 >= epsilon` (where `epsilon` is any small number between 0 and 1, we take it as 0.1).
3. Use two pointers `left` and `right` to specify the step size of searching left and right. Use list comprehension to calculate the vector `vec_to_verify` after searching. Add the constraint `x1 == vec_to_verify[0]` and solve the original integer programming problem. If a solution exists and the solution is exactly the same as `vec_to_verify`, then it proves that this is also an optimal solution. If there is no solution, exit the search. If a solution exists but is not equal to `vec_to_verify`, continue the search.
4. After the search is completed, output all optimal solutions.

### Experiments
We used a total of five test cases. First, we used two test cases from the original paper to verify that the algorithm can solve multiple optimal solutions, as follows:

```
c = [-10, -20]
b = [3, 8, 4]
A = [[0.25, 0.4], [1, 0], [0, 1]]

c=[-1,-1]
b=[6,20]
A=[[2,1],[4,5]]
```

Secondly, we used two test cases to verify that the algorithm can solve mixed integer programming problems, as follows:

```
c = [-2,-3,-4]
b = [600, 60000]
A = [[1.5, 3, 5], [280, 250, 400]]

c = [-1,-1]
b = [51/14, 1/3]
A = [[1, 9/14], [-2, 1]]
```

Finally, we used one test case to verify that the algorithm can solve large-scale integer programming problems, as follows:

```
c = [-2,-66,70,-69,18,98,68,79,-87,-56,-17,-79,-37,4,42]
b = [97,132,72,132,168,87,113,67,135,179,186,191,121,155,92]
A = [[8,19,6,10,8,4,15,3,17,2,18,5,4,10,9],
[4,18,7,11,1,10,4,1,16,2,6,7,6,2,1],
[11,13,10,3,5,14,16,14,1,2,14,16,4,18,2],
[15,4,2,19,2,4,19,18,16,7,16,8,19,11,3],
[14,1,4,11,3,14,2,4,9,4,6,4,12,12,4],
[2,7,6,10,5,3,4,2,2,11,4,5,14,13,16],
[10,14,18,4,6,7,7,9,11,7,4,6,15,1,2],
[11,3,5,5,12,2,6,3,14,8,5,6,6,4,12],
[16,14,18,11,13,5,7,12,1,12,4,8,6,18,19],
[2,14,18,12,1,5,1,4,13,18,14,8,4,5,6],
[18,13,15,2,7,11,14,19,3,3,6,2,8,13,7],
[7,4,7,15,5,6,16,2,2,15,6,16,11,2,4],
[15,3,8,1,8,3,14,5,3,6,19,12,7,8,1],
[14,2,5,19,16,5,2,3,10,6,9,13,6,4,18],
[8,13,10,5,10,5,3,1,19,18,14,2,11,1,7]]
```

For these five test cases, the algorithm yielded correct results, demonstrating its correctness.

### To Be Improved...

1. Slow solving speed for large-scale integer programming problems.
2. Unable to solve 0-1 programming problems.


