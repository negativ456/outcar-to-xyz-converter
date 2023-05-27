import numpy as np


def get_element(index):
    if index < 8:
        return 'Ta'
    elif 8 <= index < 40:
        return 'Hf'
    else:
        return 'C'


def generate_str(index, array):
    str_sum = ''
    for item in array:
        str_sum += ' ' + item
    return get_element(index) + str_sum


def stress_to_arr(stress_str):
    output_matrix = np.zeros((3, 3))
    output_matrix[0, 0] = stress_str[0]
    output_matrix[0, 1] = stress_str[3]
    output_matrix[0, 2] = stress_str[5]
    output_matrix[1, 1] = stress_str[1]
    output_matrix[1, 2] = stress_str[4]
    output_matrix[2, 2] = stress_str[2]

    output_matrix = np.triu(output_matrix) + np.triu(output_matrix, 1).T

    return ' '.join(map(str, output_matrix.flatten()))


def unite_outcar(outcar_paths, xyz_path):
    final = []
    for outcar_path in outcar_paths:
        with open(outcar_path, 'r') as f:
            outcar = f.readlines()
        arr = ' '.join(map(''.join, outcar)).split('------------------------ aborting loop because EDIFF is reached ----------------------------------------')
        for i, x in enumerate(arr[1:]):
            if i % 5 == 0:
                final.append(x)
    with open(xyz_path, 'w') as f:
        f.write(''.join(final))
        f.close()