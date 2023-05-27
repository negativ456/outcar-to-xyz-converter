from helpers.helpers import (get_element, unite_outcar, stress_to_arr)


def write_to_xyz(xyz_path, coords, lattice_arr, energy, stress):
    with open(xyz_path, 'a') as f:
        f.write(str(len(coords)) + '\n')
        lattice_str = ' '.join(map(' '.join, lattice_arr))
        f.write(
            f'Lattice="{lattice_str}" Properties=species:S:1:pos:R:3:forces:R:3 energy={energy} stress="{stress}" pbc="T T T"\n')
        for index, coord in enumerate(coords):
            position_str = ' '.join(coord)
            f.write(f'{get_element(index)} {position_str}\n')
        f.close()


def convert_outcar_xyz(outcar_path, xyz_path):
    coords = []
    lattice_arr = []
    first_lattice = False
    stress = ''
    energy = ''
    # free_energy = ''
    with open(outcar_path, 'r') as f:
        outcar = f.readlines()

    for i, line in enumerate(outcar):
        if "FORCE on cell =-STRESS in cart. coord.  units (eV):" in line:
            stress = stress_to_arr(outcar[i + 13].split()[1:])
        if "direct lattice vectors" in line:
            if first_lattice:
                start_index = i + 1
                for lattice_line in outcar[start_index:]:
                    if "length of vectors" in lattice_line:
                        break
                    else:
                        lattice_arr.append(lattice_line.split()[:3])
            first_lattice = True
        if "POSITION" in line:
            start_index = i + 2
            for position_line in outcar[start_index:]:
                if "------" in position_line:
                    break
                else:
                    coords.append(position_line.split())
        if coords and lattice_arr:
            # if "free energy    TOTEN" in line:
            #     free_energy = line.split()[4]
            if "energy(sigma->0)" in line:
                if line.split().__len__() == 7:
                    energy = line.split()[6]
                    write_to_xyz(xyz_path, coords, lattice_arr, energy, stress)
                    coords = []
                    lattice_arr = []
                    energy = ''
                    # free_energy = ''
    f.close()


convert_outcar_xyz('OUTCAR', 'structure.xyz')
