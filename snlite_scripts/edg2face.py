import math

def intersect_line_plane(v1, v2, plane_co, plane_no):
    u = l2[0]-l1[0], l2[1]-l1[1], l2[2]-l1[2]
    h = l1[0]-plane_co[0], l1[1]-plane_co[1], l1[2]-plane_co[2]
    dot = plane_no[0]*u[0] + plane_no[1]*u[1] + plane_no[2]*u[2]

    if abs(dot) > 1.0e-5:
        f = -(plane_no[0]*h[0] + plane_no[1]*h[1] + plane_no[2]*h[2]) / dot
        return l1[0]+u[0]*f, l1[1]+u[1]*f, l1[2]+u[2]*f
    else:
        # parallel to plane
        return False

def obtain_normal3(p1, p2, p3):
    """
    http://stackoverflow.com/a/8135330/1243487
    finds the normal of a triangle defined by passing 3 vectors

    input: three 3-element-iterables (tuples or lists)
    output: one 3-element tuple representing the direction of the face (not normalized)
    """
    return [
        ((p2[1]-p1[1])*(p3[2]-p1[2]))-((p2[2]-p1[2])*(p3[1]-p1[1])),
        ((p2[2]-p1[2])*(p3[0]-p1[0]))-((p2[0]-p1[0])*(p3[2]-p1[2])),
        ((p2[0]-p1[0])*(p3[1]-p1[1]))-((p2[1]-p1[1])*(p3[0]-p1[0]))
    ]

def length(v):
    """
    gives you the length of the 3-element-vector
    
    input: vector-like
    output: scalar length
    """
    return math.sqrt((v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2]))

def sub_v3_v3v3(a, b):
    """
    subtract b from a.

    inputs: two 3-element-vector-like-iterables, a and b
    output: one 3-element-vector-like tuple
    """
    return a[0]-b[0], a[1]-b[1], a[2]-b[2]

def edge_2_face(edge, face):

    plane_co = ... # any point on plane
    plane_no = ... # plane.normal  (any 3 verts will do, normal"-sign" not important)

    new_co = intersect_line_plane(v1, v2, plane_co, plane_no)

    if new_co:
        new_vertex = verts.new(new_co)   # create
        A_len = length(sub_v3_v3v3(v1, new_co))
        B_len = length(sub_v3_v3v3(v2, new_co))

        vertex_reference = v1_ref if (A_len < B_len) else v2_ref
        bm.edges.new([vertex_reference, new_vertex])  # this could be just node indices
    else:
        print('parallel to plane')
