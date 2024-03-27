import numpy as np

# Función para calcular el promedio logarítmico
def log_mean(array:np.ndarray):
    """Return log mean (10log(mean(10^(array/10))))

    Args:
        array (`np.ndarray`): Array of levels

    Returns:
        `np.ndarray`: log mean
    """
    return 10 * np.log10(np.mean(10 ** (array / 10)))

def main():
    pass

if __name__ == '__main__':
    main()
