import numpy as np
import cmath
import itertools

FOURIER_DT = 0.001

# Dada una lista finita de frecuencias enteras n en [0, -1, 1, -2, 2, ...] y los pesos de Fourier correspondientes de c_n, 
# reconstruya la curva original de f(t) en el tiempo t (0< =t<1) por síntesis de Fourier.

# Matemáticamente, f(t) = suma(c_n*e^(n*2*pi*i*t) 
# Cuantas más frecuencias (ciclos) tengamos, más cerca estará f(t) de la curva original.

def fourier_synthesis(frequencies, weights, t):
    origin = [complex(0, 0)]
    components = origin + [cn * cmath.exp(n*2*cmath.pi*1j*t) for n, cn in zip(frequencies, weights)]
    return list(itertools.accumulate(components))


# Resultados de traducción
# Dado un conjunto de puntos complejos que representan una curva cerrada y una lista finita de frecuencias enteras 
# n en [0, -1, 1, -2, 2, ...], calcule los coeficientes (pesos) de la serie de Fourier.

# Matemáticamente, si f(t) es una función compleja del tiempo (0<=t<1), entonces para cada frecuencia de
# ciclo de n, el peso n-ésimo denotado por c_n es:
# c_n = int_0^1 f(t)*e^(-n*2*pi*i*t)dt
# Cuantas más frecuencias (ciclos) tengamos, más cerca se podrá reconstruir f(t) mediante la síntesis de Fourier.
def fourier_analysis(frequencies, points):
    weights = []

    # Selecciona el punto coincidente de la lista de puntos, según t, si 0<=t<1.
    def f(t):
        idx = min(len(points) - 1, max(0, round(t * len(points))))
        return points[idx]

    for n in frequencies:
        # se alcula la integral numéricamente:
        # cn = sum_t f(t)*e^(-n*2*pi*i*t)*dt, donde t va de 0 a 1 discretamente, con un tamaño de paso de dt
        cn = sum([f(t) * cmath.exp(-n*2*cmath.pi*1j*t) * FOURIER_DT for t in np.arange(0, 1, FOURIER_DT)])
        weights.append(cn)

    return weights
