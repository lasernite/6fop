# Problem 1
# ---------
def is_unique( A ):
    A.sort()
    for i in range(1, len(A)):
        if A[i] == A[i-1]:
            return False
    return True

# Problem 2
# ---------
def matrix_product( A, B, m, n, k ):
    C = [0 for i in range(k*m)]

    for r in range(m):
        for c in range(k):
            s = 0
            for i in range(n):
                s = s + A[i+n*r]*B[c+i*k]
            C[c+r*k] = s
    return C

# Problem 3
# ---------
def mode( A ):
    currMode = None
    maxCount = 0
    for i in range(len(A)):
        currValue = A[i]
        currCount = 0
        for j in range(len(A)):
            if A[j] == currValue:
                currCount = currCount + 1

        if currCount > maxCount:
            currMode = currValue
            maxCount = currCount
    return currMode

# Problem 4
# ---------
def transpose( A, m, n ):
    T = [[0 for c in range(m)] for r in range(n)]
    for i in range(len(A)):
        r = i / n
        c = i % n
        T[c][r] = A[i]

    T_row = []
    for r in range(len(T)):
        T_row += T[r]

    return T_row