# Problem 1
# ---------
def median( A ):
    A.sort()
    if len(A) % 2 == 1:
        center = len(A)/2
        return A[center]
    else:
        center_left = len(A)/2 - 1
        center_right = len(A)/2
        return (A[center_right] + A[center_left]) / 2.0

# Problem 2
# ---------
def is_quasidrome(s):
    if is_palindrome(s):
        return True
    for i in range(len(s)):
        sub = s[:i] + s[i+1:]
        if is_palindrome(sub):
            return True
    return False

def is_palindrome(s):
    rev = s[::-1]
    for i in range(len(s)):
        if s[i] != rev[i]:
            return False
    return True

# Problem 3
# ---------
def is_permutation( A, B ):
    return (sorted(A) == sorted(B))

# Problem 4
# ---------
def count_triangles( edges ):
    vertices = []
    for edge in edges:
        if edge[0] not in vertices:
            vertices.append(edge[0])
        if edge[1] not in vertices:
            vertices.append(edge[1])
    count = 0
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            for k in range(j+1, len(vertices)):
                if is_triangle(vertices[i], vertices[j], vertices[k], edges):
                    count = count + 1
    return count

def is_triangle(v1, v2, v3, edges):
    e12, e13, e23 = False, False, False

    for e in edges:
        if (e[0] == v1 and e[1] == v2) or (e[1] == v1 and e[0] == v2):
            e12 = True
        elif (e[0] == v1 and e[1] == v3) or (e[1] == v1 and e[0] == v3):
            e13 = True
        elif (e[0] == v2 and e[1] == v3) or (e[1] == v2 and e[0] == v3):
            e23 = True

        if e12 and e13 and e23:
            return True
    return False