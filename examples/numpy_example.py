import numpy as np


def old_numpy_operations():
    # Using deprecated np.float function
    x = np.float(5.0)

    # Using deprecated np.random.random_integers
    random_ints = np.random.random_integers(1, 10, 5)

    # Using deprecated np.matrix
    matrix = np.matrix([[1, 2], [3, 4]])

    # Using deprecated np.asscalar
    scalar_value = np.asscalar(np.array([42]))

    # Using np.sum with deprecated axis argument type
    arr = np.array([[1, 2], [3, 4]])
    row_sum = np.sum(arr, axis=1.0)

    return x, random_ints, matrix, scalar_value, row_sum


def new_numpy_operations():
    # Using newer alternatives
    x = float(5.0)
    random_ints = np.random.randint(1, 11, 5)
    matrix = np.array([[1, 2], [3, 4]])
    scalar_value = np.array([42]).item()
    arr = np.array([[1, 2], [3, 4]])
    row_sum = np.sum(arr, axis=1)

    return x, random_ints, matrix, scalar_value, row_sum


if __name__ == "__main__":
    old_results = old_numpy_operations()
    new_results = new_numpy_operations()
    print("Old operations results:", old_results)
    print("New operations results:", new_results)
