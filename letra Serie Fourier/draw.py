import matplotlib.pyplot as plt
import matplotlib.animation as animation
from fourier import fourier_analysis, fourier_synthesis

NUMBER_OF_FRAMES = 350

FPS = 25

NUMBER_OF_EPICYCLES = 125 #Mayor precision



# Normaliza las coordenadas del punto para que la forma pueda caber en el rango (-1, 1) para mostrar. 


def normalize(coords):
    x_min = min([c[0] for c in coords])
    x_max = max([c[0] for c in coords])
    y_min = min([c[1] for c in coords])
    y_max = max([c[1] for c in coords])

    ratio = 0.8 * 2 / max(x_max - x_min, y_max - y_min)

    def norm(c):
        return (c[0] - x_min/2 - x_max/2)*ratio, (c[1] - y_min/2 - y_max/2)*ratio

    return [norm(c) for c in coords]


# Crea una lista de cadenas poligonales
def calculate_polygonal_chains(coords):
    # Convierte las coordenadas en una serie de puntos complejos.
    points = [complex(x, y) for x, y in normalize(coords)]

    # Las frecuencias de los ciclos son números enteros: [..., -2, -1, 0, 1, 2, ...]
    # Para fines de dibujo, queremos las frecuencias en orden absoluto creciente: [0, -1, 1, -2, 2, ...]
    frequencies = list(range(-NUMBER_OF_EPICYCLES // 2 + 1, NUMBER_OF_EPICYCLES // 2 + 1))
    frequencies = sorted(frequencies, key=abs)

    weights = fourier_analysis(frequencies, points)
    # El radio del círculo n-ésimo es solo la magnitud del peso n-ésimo
    circle_radii = [abs(cn) for cn in weights]

    polygonal_chains = []
    for i in range(NUMBER_OF_FRAMES):
        t = i / NUMBER_OF_FRAMES
        polygonal_chain = fourier_synthesis(frequencies, weights, t)
        polygonal_chains.append(polygonal_chain)

    return polygonal_chains, circle_radii


# Obtiene el contorno de la curva de las cadenas poligonales: el último punto de cada cuadro
def get_outline(polygonal_chains):
    points = [p[-1] for p in polygonal_chains]
    px = [p.real for p in points]
    py = [p.imag for p in points]
    return px, py


def draw_fourier_animation(coords):
    polygonal_chains, circle_radii = calculate_polygonal_chains(coords)

    # Cada objeto se dibujará dos veces: uno para la visualización normal y otro para la visualización ampliada
    circles0 = []
    circles1 = []
    lines0 = []
    lines1 = []

    fig, axes = plt.subplots(1, 2)
    axes[0].set_aspect('equal')
    axes[0].axis('off')

    axes[1].set_aspect('equal')
    axes[1].axis('off')

    for idx in range(NUMBER_OF_EPICYCLES):
        # El círculo n-ésimo estará centrado en el punto n-ésimo de la cadena poligonal
        cx = polygonal_chains[0][idx].real
        cy = polygonal_chains[0][idx].imag
        circle0 = plt.Circle((cx, cy), circle_radii[idx], color='green', fill=False, lw=1)
        circles0.append(circle0)
        circle1 = plt.Circle((cx, cy), circle_radii[idx], color='green', fill=False, lw=1)
        circles1.append(circle1)

        # La línea n-ésima se denota simplemente por el punto n-ésimo y n+1-ésimo de la cadena poligonal
        p0x = polygonal_chains[0][idx].real
        p0y = polygonal_chains[0][idx].imag
        p1x = polygonal_chains[0][idx + 1].real
        p1y = polygonal_chains[0][idx + 1].imag
        line0 = axes[0].plot([p0x, p1x], [p0y, p1y], color='darkblue')[0]
        lines0.append(line0)
        line1 = axes[1].plot([p0x, p1x], [p0y, p1y], color='darkblue')[0]
        lines1.append(line1)

    # Para dibujar la aproximación final de la curva f(t)
    curve_x, curve_y = [], []
    curve0, = axes[0].plot([], [], lw=2, color='black')
    curve1, = axes[1].plot([], [], lw=2, color='black')

    # Para dibujar todo el contorno de la curva f(t)
    outline_x, outline_y = get_outline(polygonal_chains)
    axes[0].plot(outline_x, outline_y, lw=1, color='black')
    outline1, = axes[1].plot(outline_x, outline_y, lw=1, color='black')

    # El rango de la primera parcela se establece en (-1, 1), el rango de 
    # la segunda parcela se cierra y se centra alrededor del último punto de la cadena poligonal.
    axes[0].set_xlim((-1, 1))
    axes[0].set_ylim((-1, 1))
    axes[1].set_xlim(polygonal_chains[0][-1].real - 0.05, polygonal_chains[0][-1].real + 0.05)
    axes[1].set_ylim(polygonal_chains[0][-1].imag - 0.05, polygonal_chains[0][-1].imag + 0.05)

    def init():
        for c in circles0:
            axes[0].add_patch(c)
        for c in circles1:
            axes[1].add_patch(c)
        return [outline1] + circles0 + circles1 + lines0 + lines1 + [curve0, curve1]

    def animate(i):
        # Actualiza los círculos, la línea poligonal y la curva de dibujo.
        for ii in range(NUMBER_OF_EPICYCLES):
            circles0[ii].center = (polygonal_chains[i][ii].real, polygonal_chains[i][ii].imag)
            circles1[ii].center = (polygonal_chains[i][ii].real, polygonal_chains[i][ii].imag)

            new_p0x = polygonal_chains[i][ii].real
            new_p0y = polygonal_chains[i][ii].imag
            new_p1x = polygonal_chains[i][ii + 1].real
            new_p1y = polygonal_chains[i][ii + 1].imag
            lines0[ii].set_data([new_p0x, new_p1x], [new_p0y, new_p1y])
            lines1[ii].set_data([new_p0x, new_p1x], [new_p0y, new_p1y])

        curve_x.append(polygonal_chains[i][-1].real)
        curve_y.append(polygonal_chains[i][-1].imag)
        curve0.set_data(curve_x, curve_y)
        curve1.set_data(curve_x, curve_y)

        # Actualizar el rango de la segunda figura
        axes[1].set_xlim(polygonal_chains[i][-1].real - 0.05, polygonal_chains[i][-1].real + 0.05)
        axes[1].set_ylim(polygonal_chains[i][-1].imag - 0.05, polygonal_chains[i][-1].imag + 0.05)

        return [outline1] + circles0 + circles1 + lines0 + lines1 + [curve0, curve1]

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=NUMBER_OF_FRAMES, interval=10, blit=True)
    plt.show()
