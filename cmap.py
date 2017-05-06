from random import randint
import pandas

def initial_map_stat():
    map_matrix = [[0 for i in range(25)] for j in range(25)]
    map_matrix[0][1] = 2
    map_matrix[1][2] = 2
    map_matrix[2][3] = 2
    map_matrix[3][4] = 2
    map_matrix[0][5] = 2
    map_matrix[1][6] = 2
    map_matrix[3][8] = 2
    map_matrix[4][9] = 2
    map_matrix[5][6] = 2
    map_matrix[6][7] = 2
    map_matrix[7][8] = 2
    map_matrix[8][9] = 2
    map_matrix[5][10] = 2
    map_matrix[6][11] = 2
    map_matrix[7][12] = 2
    map_matrix[8][13] = 2
    map_matrix[9][14] = 2
    map_matrix[11][12] = 2
    map_matrix[12][13] = 2
    map_matrix[10][15] = 2
    map_matrix[11][16] = 2
    map_matrix[12][17] = 2
    map_matrix[13][18] = 2
    map_matrix[14][19] = 2
    map_matrix[15][16] = 2
    map_matrix[16][17] = 2
    map_matrix[17][18] = 2
    map_matrix[18][19] = 2
    map_matrix[15][20] = 2
    map_matrix[16][21] = 2
    map_matrix[18][23] = 2
    map_matrix[19][24] = 2
    map_matrix[20][21] = 2
    map_matrix[21][22] = 2
    map_matrix[22][23] = 2
    map_matrix[23][24] = 2
    map_matrix[1][0] = 2
    map_matrix[2][1] = 2
    map_matrix[3][2] = 2
    map_matrix[4][3] = 2
    map_matrix[5][0] = 2
    map_matrix[6][1] = 2
    map_matrix[8][3] = 2
    map_matrix[9][4] = 2
    map_matrix[6][5] = 2
    map_matrix[7][6] = 2
    map_matrix[8][7] = 2
    map_matrix[9][8] = 2
    map_matrix[10][5] = 2
    map_matrix[11][6] = 2
    map_matrix[12][7] = 2
    map_matrix[13][8] = 2
    map_matrix[14][9] = 2
    map_matrix[12][11] = 2
    map_matrix[13][12] = 2
    map_matrix[15][10] = 2
    map_matrix[16][11] = 2
    map_matrix[17][12] = 2
    map_matrix[18][13] = 2
    map_matrix[19][14] = 2
    map_matrix[16][15] = 2
    map_matrix[17][16] = 2
    map_matrix[18][17] = 2
    map_matrix[19][18] = 2
    map_matrix[20][15] = 2
    map_matrix[21][16] = 2
    map_matrix[23][18] = 2
    map_matrix[24][19] = 2
    map_matrix[21][20] = 2
    map_matrix[22][21] = 2
    map_matrix[23][22] = 2
    map_matrix[24][23] = 2
    return map_matrix

def rand_situation():
    map_matrix = initial_map_stat()
    choice1 = [[7,12], [11,12], [17,12], [13,12]]
    del choice1[randint(0,3)]
    for e in choice1:
        map_matrix[e[0]][e[1]] = 0
        map_matrix[e[1]][e[0]] = 0
    choice2 = [[1,6], [5,6], [3,8], [9,8], [15,16], [21,16], [19,18], [23,18]]
    i = randint(0,3)
    choice2 = [choice2[2*i], choice2[2*i+1]]
    for e in choice2:
        map_matrix[e[0]][e[1]] = 0
        map_matrix[e[1]][e[0]] = 0
    choice3 = [[5,10], [15,10], [1,2], [3,2], [9,14], [19,14], [21,22], [23,22]]
    i = randint(0,7)
    i2 = randint(0,7)
    while i == i2:
        i = randint(0,7)
        i2 = randint(0,7)
    choice3 = [choice3[i], choice3[i2]]
    for e in choice3:
        map_matrix[e[0]][e[1]] = 1
        map_matrix[e[1]][e[0]] = 1
    return map_matrix

def solution(tree, destination, ans):
    if tree[destination] == -1:
        ans.append(12)
        return ans
    else:
        ans.append(destination)
        return solution(tree, tree[destination], ans)

def find_path(map_matrix, destination):
    tree = [-1]*25
    distance = [111]*25
    distance[12] = 0
    temp = []
    for i in range(25):
        temp.append(i)
    while len(temp)!=0:
        min_distance = 111
        node = -1
        for i in range(len(distance)):
            if distance[i] < min_distance and i in temp:
                min_distance = distance[i]
                node = i
        temp.remove(node)
        for i in range(25):
            if map_matrix[node][i] and (i in temp) and (distance[node] + map_matrix[node][i] < distance[i]):
                tree[i]=node
                distance[i]=distance[node]+map_matrix[node][i]
    ans = []
    return solution(tree, destination, ans)

def get_destination(ddid):
    read = pandas.read_csv("data/order.csv")
    return read.loc[read["ddid"]==int(ddid)]["destination"].values[0]
