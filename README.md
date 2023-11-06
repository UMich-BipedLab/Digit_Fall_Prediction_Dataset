## Digit Fall Dataset

This dataset is comprised of simulation and hardware trajectories with abrupt, incipient, and intermittent faults for the Digit robot during the task of standing. 

### Background

Falls can be attributed to faults, which are defined as unforeseen deviations in one or more operation variables. As depicted in the image below, faults can be classified into three types based on their time dependency: abrupt, incipient, and intermittent. Abrupt faults are rapidly varying, incipient faults are drift-like, and intermittent faults are sporadic. As we discuss in [1] each of these fault types can arise during real-world operation.

Relevant Definitions:

* Critical faults: faults that lead to falls

* Lead time: the time to react

     * Defined as the difference between the time of the actual fall and the predicted fall
#### Simulation Data

We employ Agility’s MuJoCo-based simulator in conjunction with a standing controller [1]. The objective of the controller is to maintain both the center of mass and the zero-moment point within the support polygon. Three different kinds of faults were applied, abrupt, incipient and intermittent. These faults are simulated by applying forces of various magnitudes to the robot’s torso in the x-direction (i.e., sagittal plane).   To simulate minor disturbances that might induce slight oscillations in the robot’s standing posture, we introduce impulsive forces with a 0.075s duration, ranging from 0 - 202.4N, at the start of each trajectory.

##### Abrupt faults
Abrupt faults are simulated using impulsive forces with a duration of 0.075s, randomly uniformly distributed within a range of 0 - 414.8N. A total of 900 trajectories were simulated

##### Incipient faults
Incipient faults are simulated with trapezoidal force profiles, as depicted in the figure below. These profiles have a slope of 480N/s. A total of 900 trajectories were simulated
<p align="center">
<img src="https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/utils/trap_force_profile_2.png" data-canonical-src="[https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/utils/trap_force_profile_2.png)" width="600" />
   </p>
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
