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
Incipient faults are simulated with trapezoidal force profiles, as depicted in the figure below. These profiles have a slope of 480N/s. A total of 900 trajectories were simulated

##### Intermittent faults
Emulating the unpredictable nature of intermittent faults, we apply two distinct forces. These forces are designed to mimic either abrupt or intermittent faults. A total of 100 trajectories were simulated 

### Installation

1. Clone the repository

   ```
   git clone https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset.git
   OR
   git clone git@github.com:UMich-BipedLab/Digit_Fall_Prediction_Dataset.git
   ```
2. Generate shared libraries
- [Download the c_kin](https://drive.google.com/drive/folders/1e2JOxkFBqKKjPFwIzKh90jPmDfrOx2e7?usp=sharing) and extract it in c_functions folder.
- Build the downloaded c functions:

   ```
   # create a build folder
   cd Digit_Fall_Prediction_Dataset && cd c_functions
   mkdir build

   # build libraries
   cd build
   cmake ..
   make all
   ```

### Downloading the dataset
[Download the digit data folder](https://drive.google.com/drive/folders/16OIbha19oqi7Iw0b9ZPmbNT7O6e3dWlQ?usp=sharing) and extract it in Digit_Fall_Prediction_Dataset root folder. Keep the folder name as digit data.

### Loading the dataset
```
# create the DatasetLoader class
dl = DatasetLoader()
# load the dataset 
dl.load_dataset(transform_real_trajectories=True, remove_hardware_data_after_killed=True, subtract_initial_angle_sim=True)
```
