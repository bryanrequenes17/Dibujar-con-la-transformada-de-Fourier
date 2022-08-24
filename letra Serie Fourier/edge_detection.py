from skimage import feature, io
import matplotlib.pyplot as plt
import numpy as np
import random



SAMPLING_SIZE = 1000

RANDOM_SEED = 0



# Seleccione una cantidad aleatoria de SAMPLING_SIZE de puntos de la lista original
def sampling(coords):
    if len(coords) <= SAMPLING_SIZE:
        return coords

    random.seed(RANDOM_SEED)
    random_indices = list(range(len(coords)))
    random.shuffle(random_indices)
    return [coords[random_indices[i]] for i in range(SAMPLING_SIZE)]


# Regresa con un conjunto de puntos que representan los bordes
def detect_edges(image_name):
    image = io.imread(image_name, as_gray=True)

    # Detección de bordes (Canny edge)
    edges = feature.canny(image, 0.6, 0.1, 0.97, use_quantiles=True)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    ax1.imshow(image, cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('Imagen', fontsize=15)

    edge_im = ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('Detección de bordes', fontsize=15)

    plt.show()

    # Las coordenadas x e y son solo los puntos distintos de cero de la imagen de borde
    x_coords, y_coords = np.nonzero(edge_im.get_array())
    # Los ejes x e y de una imagen difieren de los ejes x e y de un gráfico, por lo que tenemos que pasar de (x,y) a (y,-x).
    # Para con ello no encontrar la imagen volteada.
    points = list(zip(y_coords, -x_coords))

    # Reducir el número de puntos
    points = sampling(points)
    print(f'Número de puntos finales: {len(points)}')

    return points
