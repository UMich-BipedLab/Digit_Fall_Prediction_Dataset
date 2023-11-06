from utils import dataset
from utils import DynamicsCalculator as dc
import numpy as np


def load_digit_dataset():
    dl = dataset.DatasetLoader()
    dl.load_dataset(transform_real_trajectories=True,
                    remove_hardware_data_after_killed=True,
                    subtract_initial_value=True)
    
    # extract dataset information
    pos_data = dl.pos_data
    vel_data = dl.vel_data
    ang_mom_data = dl.ang_mom_data
    time_data = dl.time_data
    q_data = dl.q_data
    qdot_data = dl.qdot_data
    trajectory_info = dl.trajectory_info
    
    return dl
    

def dynamics_calculator_example():
    ang_mom = dc.get_angular_momentum(np.zeros(30), np.zeros(30), [1,2, 3], [3, 4, 56])
    print(ang_mom)
    pos = dc.get_position(np.zeros(30), np.zeros(30), "p_COM")
    print(pos)
    vel = dc.get_velocity(np.zeros(30), np.zeros(30), "p_COM")
    print(vel)

    
if __name__ == "__main__":
    dl = load_digit_dataset()
    dynamics_calculator_example()