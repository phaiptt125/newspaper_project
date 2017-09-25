# Computing Weighted Edit Distance #
# The code is adapted from http://www.nltk.org/_modules/nltk/metrics/distance.html
#...............................................................

#Creating a matrix to store output
def InitializingMatrix(len1, len2):
    lev = []
    for i in range(len1):
        lev.append([0] * len2)  # initialize 2D array to zero
    for i in range(len1):
        lev[i][0] = i           # column 0: 0,1,2,3,4,...
    for j in range(len2):
        lev[0][j] = j           # row 0: 0,1,2,3,4,...
    return lev

#Say, lev = InitializingMatrix(5, 3) will give a matrix of
#
#[4, 0, 0]
#[3, 0, 0]
#[2, 0, 0]
#[1, 0, 0]
#[0, 1, 2]
#
# Next function will print this matrix out
#...............................................................

#Printing matrix: 
def PrintMatrix(mat):
   NumRow = len(mat)
   for ind in range(NumRow):
      print(mat[NumRow-ind-1][:])

#...............................................................

def ComputeMinStep(lev, i, j, s1, s2):
    c1 = s1[i - 1]
    c2 = s2[j - 1]

    # skipping a character in s1
    a = lev[i - 1][j] + 1
    # skipping a character in s2
    b = lev[i][j - 1] + 1
    # substitution
    c = lev[i - 1][j - 1] + (c1 != c2)

    # minimize distance in a step
    lev[i][j] = min(a, b, c)

#...............................................................

def EditDistance(s1, s2):

    len1 = len(s1)
    len2 = len(s2)
    lev = InitializingMatrix(len1+1, len2+1)

    for i in range(len1):
        for j in range(len2):
            ComputeMinStep(lev, i + 1, j + 1, s1, s2)

    Distance = lev[len1][len2]
    return Distance

#...............................................................





