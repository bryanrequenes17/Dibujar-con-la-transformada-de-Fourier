import numpy as np
from scipy.spatial import distance_matrix

#Dada una matriz de distancia, ordene los números de índice [0, 1, ..., longitud-1] de manera 
# greedy: comenzando desde 0, elige el índice libre más cercano a continuación

def greedy(dist_mat):
    length = dist_mat.shape[0]
    current_node_idx = 0  # Puede ser aleatorio entre 0 y longitud-1
    node_order = [current_node_idx]

    free_node_indices = set(range(length))
    free_node_indices.remove(current_node_idx)
    while free_node_indices:
        next_node_idx = np.argmin([dist_mat[current_node_idx][i] if i in free_node_indices else np.inf
                                   for i in range(length)])
        free_node_indices.remove(next_node_idx)
        node_order.append(next_node_idx)
        current_node_idx = next_node_idx

    return node_order


def opt2swap(tour, i, j):
    return tour[:i] + tour[i:j][::-1] + tour[j:]


# Implementa el algoritmo 2-opt
def opt2(coord_order, dist_mat):
    tour = coord_order + [coord_order[0]] 
    length = len(tour)

    min_change = -1
    while min_change < 0:
        min_change = 0
        for i in range(1, length - 2):
            for j in range(i + 2, length):
                # Si intercambiamos estos dos nodos, la duración total del recorrido cambiaría en esta cantidad
                change = dist_mat[tour[i-1], tour[j-1]] - \
                         dist_mat[tour[i-1], tour[i]] + \
                         dist_mat[tour[i], tour[j]] - \
                         dist_mat[tour[j-1], tour[j]]

                if change < min_change:
                    min_change = change
                    tour = opt2swap(tour, i, j)

    return tour[0:-1]


def solve_tsp(original_points):
    dist_mat = distance_matrix(original_points, original_points)
    point_order = greedy(dist_mat)
    points_in_order = [original_points[i] for i in point_order]  #Orden de punto inicial por algoritmo Greedy

    return points_in_order
