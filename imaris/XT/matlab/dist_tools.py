#!/usr/bin/python

# TODO:
#  - add documentation
#  - sanity/type checks

from numpy import array, linalg
def dist(p1, p2):
    point1 = array(p1)
    point2 = array(p2)
    return(linalg.norm(point1 - point2))

def largest_dist_idx(point, pointlist):
    # print point
    # print pointlist
    distances = [()] * len(pointlist)
    for i, cand in enumerate(pointlist):
        distances[i] = dist(point, cand)
    # print distances
    maxdist = max(distances)
    return([distances.index(maxdist), maxdist])

from scipy import reshape, sqrt
from numpy.matlib import repmat, repeat, sum, where
def dist_matrix_euclidean(points):
    num_points = len(points)
    # print len(repmat(points, num_points, 1))
    # print len(repeat(points, num_points, axis=0))
    dist_mat = sqrt(sum((repmat(points, num_points, 1) -
                        repeat(points, num_points, axis=0))**2, axis=1))
    return dist_mat.reshape((num_points, num_points))

def get_max_dist_pair(matrix):
    # Takes a distance matrix and finds the pair having the largest
    # distance to each other. Returns a tuple of index numbers.
    maxdist = 0
    pair = (-1, -1)
    for row_num, row in enumerate(matrix):
        row_max = max(row)
        if row_max > maxdist:
            maxdist = row_max
            max_pos = where(row == row_max)[0][0]
            pair = (row_num, max_pos)
            # print [row_num] + [where(row == row_max)[0][0]] + [maxdist]
            # print pair
    return pair

from numpy import ma
def find_neighbor(pid, dist_mat, mask):
    """Finds the closest neighbor in a given distance matrix.

    Takes a reference point and looks up the closest neighbor in a
    masked distance matrix. The mask can be used to exclude selected
    points in the calculation, for example when they have already been
    processed earlier. Otherwise use a 0-mask.

    Args:
        pid: the index of the reference point
        dist_mat: the euclidean distance matrix of all points
        mask: binary array to use as a mask

    Returns:
        closest: index of the closest neighbor
    """
    masked_dists = ma.array(dist_mat[pid], mask=mask)
    closest = masked_dists.argmin()
    return closest


if __name__ == "__main__":
    print "This module provides just functions, no direct interface."
