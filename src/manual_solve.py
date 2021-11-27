#!/usr/bin/env python
# coding: utf-8

# In[1]:
'''
Student_name: Reddivinod Reddy
Student_ID  : 21244404

'''

#!/usr/bin/python

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.




def solve_1bfc4729(x):
    '''
    solve_1bfc4729 fucntion transforms input x based on the color each cell is having.
    if it find cell with any color other than black, 
    then it fill that row and row-2, also half of first and end columns
    '''
    sizee=x.shape[0]                           #fetch the height of column
    num =np.nonzero(x)                         #Get the number of cells of non black color
    color=[x[y[0]][y[1]] for y in zip(*num)]   #list of cells filled with colors
    x[0]=color[0]                              #fill the color in row and row-2 from top
    x[2]=color[0]
    x[sizee-1]=color[1]                        #fill the color in bottom row and row+2
    x[sizee-3]=color[1]
    x[:,0][0:5]=color[0]                       #fill color in half of first column
    x[:,sizee-1][0:5]=color[0]                 #fill color in half of last column
    x[:,0][5:10]=color[1]                      #fill color in remaining half of first column
    x[:,sizee-1][5:10]=color[1]                #fill color in remaining half of last column
    return x

def solve_0ca9ddb6(x):
    '''
    solve_0ca9ddb6 fucntion transforms input x by adding colors around color=2(orange) and color=1(blue) and ignores remaining colors
    if it find cell with color=2, fills color=4 in the diagonal directions of that cell 
    if it find cell with color=1, fills color=7 in the east,west,north,south directions of that cell
    '''

    Color_1=np.where(x==2)   #if cell with orange color, then  fill all diagonal cells with yellow
    for j in zip(*Color_1):
        x[j[0]-1][j[1]-1]=4
        x[j[0]-1][j[1]+1]=4
        x[j[0]+1][j[1]-1]=4
        x[j[0]+1][j[1]+1]=4
    Color_2=np.where(x==1)   #if cell with blue color, then  fill east,west,north,south side cells with orange
    for i in zip(*Color_2):
        x[i[0]-1][i[1]]=7
        x[i[0]+1][i[1]]=7
        x[i[0]][i[1]+1]=7
        x[i[0]][i[1]-1]=7

    return x

def solve_0dfd9992(x):
    '''
    solve_0dfd9992 fucntion transforms input x by below steps
    1.Check for number of empty/black cells in x 
    2.for each cell check the color of the cell in the same position one row above this cell and check the color of adjacent cell towards left
    3.let me call these cells as east and north cell colors to the cell with black color
    4.extract the 2 rows of the where black cell is found
    5.In this 2 rows find the same pattern where if any cell is having east and north cells as same as colors found in step 2, if yes then 
      use this color to fill black cell
       [6 3 2 3 6 5 6 3 2 3 6 5 6 3 2 3 6 5 6 3 2]
       [5 2 1 2 5 4 5 2 1 2 5 0 5 2 1 2 5 4 5 2 1]
       For the above example to find the value to replace 0,
       east =5 (above 0)
       north=5 (adjacent to 0)
       in the 2 rows same pattern is having value 4, so 0 can be replaced with 4. 
     6.Repeat step 2 to 5 for number of empty/black cells in x found in step 1
     7.if still blacks cells left, then repeat the step 1 to 6, instead fetching rows, extract columns.

    '''

    m=np.where(x==0) 
    mm=len(list(zip(*m)))                        #find the number black cells
    while(mm!=0):                                #Iterate through each black cell step 2 to step 6, see above
        missing=np.where(x==0)                   
        for z in zip(*missing):
            horizontal=np.array([x[z[0]-1],x[z[0]]])  #extract 2 rows one with black cell and one row above that
            east=horizontal[0][z[1]]
            north=horizontal[1][z[1]-1]
            for ind,val in enumerate(list(horizontal[0])):
                if((val==east) & (horizontal[1][ind-1]==north) & (horizontal[1][ind]!=0)):
                        x[z[0]][z[1]]=horizontal[1][ind]
        mm-=1
    k=np.where(x==0)                             #check if any black cells after solving horizontally
    kk=len(list(zip(*k)))
    while(kk!=0):
        missing=np.where(x==0) 
        for z in zip(*missing):
            a=z[1]-1 if(z[1]-1 !=-1) else 15
            vertical=x[:,[z[1],a]]
            vertical=vertical.transpose()          #extracted columns
            tto=list(vertical[0])
            tt=list(vertical[1])
            east=tto[z[0]-1]
            north=tt[z[0]]
            for ind,val in enumerate(list(vertical[0])):
                nr=tt[ind+1] if((ind+1)<=20) else tt[0]
                cval=vertical[0][ind+1] if((ind+1)<=20) else vertical[0][0]
                if((val==east) & (nr==north) & (cval!=0)):
                        x[z[0]][z[1]]=cval

        kk-=1

    return x


def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    if y.shape != yhat.shape:
        print(f"False. Incorrect shape: {y.shape} v {yhat.shape}")
    else:
        print(np.all(y == yhat))


if __name__ == "__main__": main()

