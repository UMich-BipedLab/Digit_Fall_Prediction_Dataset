## Digit Fall Dataset

This dataset comprises of simulation and hardware trajectories of the Digit robot, where a force is applied
to the robot in a standing position

### Data Description

One of the three kinds of forces, abrupt, incipient and intermittent, was applied to the robot and the resulting trajectory was recorded.

#### Simulation Data

We employ Agility’s MuJoCo-based simulator in conjunction with a standing controller. Three different kind of faults were applied, abrupt, incipient and intermittent. These faults are simulated by applying forces of various magnitudes to the robot’s torso in the x-direction (i.e., sagittal plane).   To simulate minor disturbances that might induce slight oscillations in the robot’s standing posture, we introduce impulsive forces with a 0.075s duration, ranging from 0 - 202.4N, at the start of each trajectory.

##### Abrupt faults
Abrupt faults are simulated using impulsive forces with a duration of 0.075s, randomly uniformly distributed within a range of 0 - 414.8N. A total of 900 trajectories were simulated

##### Incipient faults
Incipient faults are simulated with trapezoidal force profiles as depicted in Figure 3. These profiles have a slope of 480N. A total of 900 trajectories were simulated

##### Intermittent faults
Emulating the unpredictable nature of intermittent faults, we apply two distinct forces. These forces are designed to mimic either abrupt or intermittent faults. A total of 100 trajectories were simulated 

### Installation

1. Clone the repository

   ```
   git clone https://github.com/Emungai/Fault_Detection_Diagnostics.git
   OR
   git clone git@github.com:Emungai/Fault_Detection_Diagnostics.git
   ```
2. Generate shared libraries

   ```
   # create a build folder
   cd Fault_Detection_Diagnostics && cd c_functions
   mkdir build

   # build libraries
   cd build
   cmake ..
   make all
   ```
3. Create python virtual environment and install packages (this was tested with python 3.6.9)

   ```
   cd Fault_Detection_Diagnostics
   mkdir .venvs && cd .venvs
   python3 -m venv digit_venv
   source digit_venv/bin/activate
   pip3 install --upgrade pip
   pip3 install -r requirements.txt
   ```

### Downloading the dataset

### Loading the dataset
```
# create the DatasetLoader class
dl = DatasetLoader()
# load the dataset 
dl.load_dataset(transform_real_trajectories=True, remove_hardware_data_after_killed=True, subtract_initial_angle_sim=True)
```