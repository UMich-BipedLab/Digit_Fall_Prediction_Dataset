import os
import ctypes
import numpy as np

"""
This function demonstrates how to load and use the c_functions
Note that the c_functions should only be used with the original (non pre-processed) q and qdot.
 P_com_rel = P_com - 0.5*(P_rightToeMid + P_leftToeMid)
"""

def _convert_c_array_to_np(prefix, c_array):
    if prefix == "p" or prefix == "L" or prefix == "v":
        size = (3,)
        length = size[0]
        return _convert_c_array_to_np_vector(c_array, length)
    
    elif prefix == "Jp":
        size = (3, 30)
        nrow = size[0]
        ncol = size[1]
        return _convert_c_array_to_np_matrix(c_array, nrow, ncol)
    
    else:
        raise NotImplementedError
    

def _convert_c_array_to_np_vector(AM_arr, arr_length):
    np_arr = np.zeros(arr_length)
    j = 0
    for j in range(0, arr_length):
        np_arr[j] = AM_arr[j]

    return np_arr


def _convert_c_array_to_np_matrix(AM_arr, nrow, ncol):
    np_matrix = np.zeros((nrow, ncol))
    for j in range(0, ncol):
        for i in range(0, nrow):
            np_matrix[i, j] = AM_arr[i + j * nrow]
    
    return np_matrix


def _create_c_array(array_length):
    AM_ar = (ctypes.c_double * array_length)
    
    return AM_ar


def _load_c_functions(ref_point):
    filename = "lib" + ref_point + ".so"
    curr_dir, _ = os.path.split(os.path.realpath(__file__))
    SHARED_LIB_PATH = os.path.join(curr_dir, "..", "c_functions", "build")
    func = ctypes.CDLL(os.path.join(SHARED_LIB_PATH, filename))
    
    return func


def get_position(q, ref_point):
    x_ar = (ctypes.c_double * len(q))(*q)
    prefix = "p"
    func = _load_c_functions(ref_point)
    c_array = _create_c_array(3)()
    eval("func." + ref_point + "(c_array, x_ar)")
    pos = _convert_c_array_to_np(prefix, c_array)

    return pos

    
def get_velocity(q, dq, reference_point):
    c_q = (ctypes.c_double * len(q))(*q)
    c_dq = (ctypes.c_double * len(dq))(*dq)
    func = _load_c_functions(reference_point)
    c_array = _create_c_array(90)()
    eval("func." + reference_point + "(c_array, c_q)")
    prefix = "Jp"
    np_arr = _convert_c_array_to_np(prefix, c_array)
    
    dq_np_arr = np.zeros((30, 1))
    for j in range(30):
        dq_np_arr[j] = dq[j]

    vel_arr = np_arr @ dq_np_arr

    return vel_arr.squeeze()


def get_vel_com(q, dq):
    c_q = (ctypes.c_double * len(q))(*q)
    c_dq = (ctypes.c_double * len(dq))(*dq)
    reference_point = "v_COM"
    prefix = "v"
    func = _load_c_functions(reference_point)
    c_array = _create_c_array(3)()
    eval("func." + reference_point + "(c_array, c_q, c_dq)")
    vel_com = _convert_c_array_to_np(prefix, c_array)

    return vel_com


def get_angular_momentum(q, dq, custom_point_pos, custom_point_vel):    
    c_q = (ctypes.c_double * len(q))(*q)
    c_dq = (ctypes.c_double * len(dq))(*dq)
    c_pos = (ctypes.c_double * 3)(*custom_point_pos)
    c_vel = (ctypes.c_double * 3)(*custom_point_vel)
    
    c_array = _create_c_array(3)()
    func = _load_c_functions("L_world_about_point")
    eval("func." + "L_world_about_point" + "(c_array, c_q, c_dq, c_pos, c_vel)")
    prefix = "L"
    ang_momentum = _convert_c_array_to_np(prefix, c_array)
    return ang_momentum


if __name__ == "__main__":
    ang_mom = get_angular_momentum(np.zeros(30), np.zeros(30), [1,2, 3], [3, 4, 56])
    print(ang_mom)
    pos = get_position(np.zeros(30), np.zeros(30), "p_COM")
    print(pos)
    vel_com = get_vel_com(np.zeros(30), np.zeros(30))
    print(vel_com)
    vel = get_velocity(np.zeros(30), np.zeros(30), "p_COM")
    print(vel)
    