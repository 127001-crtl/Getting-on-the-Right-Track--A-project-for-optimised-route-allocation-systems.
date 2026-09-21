import random
#python code!
#This is practice for Nearest neighbour construction:
'''
Logic: 
1. we need to create a random graph
2. choose a random starting point
3. find closest neighbour
4. go to neighbour
5. delete previous point
6. continue until no more routes.
'''

# creating the graph
def createGraph():
#   ^^^ first trial ^^^
    side = 4 #for testing purposes replace w random.randint(5, 50)
    global defaultList #since it is very very importnat
    defaultList = [
        [random.randint(0, 100) for _ in range(side)]
        for _ in range(side)
    ]


    print(str(defaultList).replace("], ", "]\n").replace("[[", "[").replace("]]", "]"))
    
    
def findStartingPoint(array):
    if not array or not array[0]:
        raise ValueError("array must contain at least one point")

    row = random.randrange(len(array))
    column = random.randrange(len(array[row]))
    return row, column
    

def findClosest(array, startingPoint):
    row, column = startingPoint
    neighbours = []
    for neighbourRow, neighbourColumn in (
        (row, column - 1),
        (row, column + 1),
        (row - 1, column),
        (row + 1, column),
    ):
        if 0 <= neighbourRow < len(array) and 0 <= neighbourColumn < len(array[neighbourRow]):
            neighbours.append(array[neighbourRow][neighbourColumn])

    if not neighbours:
        raise ValueError("starting point has no neighbours")
    

    #Finds ←→↓↑ values.
    smallest = neighbours[0]
    for x in neighbours:
        if x < smallest:
            smallest = x  # Update if a smaller value is found
    print(f"Smallest neighbour: {smallest},", "neighbours:", neighbours, "startingPoint:", startingPoint)

    return smallest

def main():
    createGraph()    
    startingPoint = findStartingPoint(defaultList)
    smallest = findClosest(defaultList, startingPoint)

    return ''
#now we need to solve. we need to take the path of least resistance. we need to find the closest neighbour and then go to that neighbour and then delete the previous point in a seperate graph and continue until no more routes.
def solve(array, startingPoint, ):
    row, column = startingPoint
    
main()

'''
[[90, 82, 37, 57, 31, 39], [70, 36, 
9, 32, 42, 73], [13, 0, 25, 97, 100, 
40], [76, 87, 56, 63, 55, 43], [14, 100, 
72, 10, 30, 16], [40, 16, 79, 37, 40, 
66], [53, 42, 19, 74, 44, 0], [65, x ,x ,x]
'''
'''
[
[90, 82, 37, 57, 31, 39], 
[70, 36, 9, 32, 42, 73], 
[13, 0, 25, 97, 100, 40], 
[76, 87, 56, 63, 55, 43], 
[14, 100, 72, 10, 30, 16], 
[40, 16, 79, 37, 40, 66], 
[53, 42, 19, 74, 44, 0], 
[65, x ,x ,x, x ,x]
]
'''

