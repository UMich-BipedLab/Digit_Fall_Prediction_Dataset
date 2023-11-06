## Digit Fall Dataset

This dataset is comprised of simulation and hardware trajectories with various faults for the Digit robot during the task of standing. The simulation trajectories contain abrupt, incipient, and intermittent faults, while the hardware trajectories contain abrupt and incipient faults.

### Contents
- [Repository Organization](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/tree/main#repository-organization)
- [Installation](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#installation)
- [Downloading the Dataset](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#downloading-the-dataset)
- [Loading the Dataset](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#loading-the-dataset)
- [Dataset Information](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#dataset-information)
   - [Background](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#background)
   - [Simulation Data Generation](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#simulation-data-generation)
    - [Abrupt Faults](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#abrupt-faults)
    - [Incipient Faults](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#incipient-faultsv)
    - [Intermittent Faults](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#intermittent-faults)
   - [Hardware Data Generation](https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/README.md#hardware-data-generation)

### Repository Organization
```
.
├── c_function 
├── utils
│   ├── DynamicsCalculator.py 
│   ├── dataset.py
│   ├── params.yaml
└── README.md
└── main.py
```
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

### Downloading the Dataset
[Download the digit data folder](https://drive.google.com/drive/folders/16OIbha19oqi7Iw0b9ZPmbNT7O6e3dWlQ?usp=sharing) and extract it in Digit_Fall_Prediction_Dataset root folder. Keep the folder name as digit data.

### Loading the Dataset
```
# create the DatasetLoader class
dl = DatasetLoader()
# load the dataset 
dl.load_dataset(transform_real_trajectories=True, remove_hardware_data_after_killed=True, subtract_initial_angle_sim=True)
```


### Dataset Information
#### Background

Falls can be attributed to faults, which are defined as unforeseen deviations in one or more operation variables. As depicted in Figure 1, faults can be classified into three types based on their time dependency: abrupt, incipient, and intermittent. Abrupt faults are rapidly varying, incipient faults are drift-like, and intermittent faults are sporadic. As we discuss in [1] each of these fault types can arise during real-world operation.

Relevant Definitions:

* Critical faults: faults that lead to falls

* Lead time: the time to react

     * Defined as the difference between the time of the actual fall and the predicted fall
* Unsafe trajectories: trajectories with critical faults
 
<p align="center">
<img src="https://images.squarespace-cdn.com/content/v1/611a553f61f55233affe305b/a9cd689f-faae-4fb5-9fc4-eb97bd179447/faults_time_dependency_2.png?format=1000w"  width="600" />
    
   </p>      
<p align="center">
   Figure 1
    </p>
    
#### Simulation Data Generation

To generate the trajectories, we employ Agility’s MuJoCo-based simulator in conjunction with a standing controller [2]. The objective of the controller is to maintain both the center of mass and the zero-moment point within the support polygon. The faults are simulated by applying forces of various magnitudes to the robot’s torso in the x-direction (i.e., sagittal plane). To simulate minor disturbances that might induce slight oscillations in the robot’s standing posture, we introduce impulsive forces with a 0.075s duration, ranging from 0 - 202.4N, at the start of each trajectory.

##### Abrupt faults
Abrupt faults are simulated using impulsive forces with a duration of 0.075s, randomly uniformly distributed within a range of 0 - 414.8N. The range is chosen such that half of the trajectories contain critical abrupt faults. The impulsive forces are introduced randomly within a period of 1.5s, and a total of 900 trajectories were simulated. 

##### Incipient faults
Incipient faults are simulated with trapezoidal force profiles, as depicted in Figure 2. These profiles have a slope of 480N/s over a varying duration to result in a desired constant amplitude over a time duration of 1s; the resulting force amplitudes of incipient faults are randomly uniformly distributed between 0 - 57.6N. The range is chosen such that half of the trajectories contain critical abrupt faults, and the incipient faults are introduced randomly within a period of 1.5s. A total of 900 trajectories were simulated
<p align="center">
<img src="https://github.com/UMich-BipedLab/Digit_Fall_Prediction_Dataset/blob/main/utils/trap_force_profile_2.png"  width="600" /> 
</p>
<p align="center">
   Figure 2
    </p>   
    
##### Intermittent faults
Emulating the unpredictable nature of intermittent faults, we apply two distinct forces. These forces are designed to mimic either abrupt or intermittent faults. The first force’s magnitude remains within the safe range, while the second force’s magnitude can potentially lead to a fall or maintain stability. Similar to the abrupt and incipient faults, the two forces are each applied within a period of 1.5s. The time between the application of the two forces is 2s. 



#### Hardware Data Generation
To prevent the Digit robot from getting damaged during data collection, the hardware data generation is carried out with Digit attached to a gantry. Additionally, the motor power is “killed” when the robot starts to fall, thereby allowing the gantry to catch it. Note that we attempt to “kill” the motors prior to the gantry catching the robot.  Impulsive and trapezoidal forces are introduced to the robot’s torso by pushing Digit with a pole. To emulate the trapezoidal forces that result in an incipient fault, the pole is first rested on Digit before pushing. Twenty-seven (27) safe and 13 unsafe trajectories are collected for abrupt faults, while 26 safe and
15 unsafe trajectories are collected for incipient faults. Figure 3 depicts the experimental setup of the hardware data.

<p align="center">
<img src="https://static1.squarespace.com/static/611a553f61f55233affe305b/t/6548f541f268e87c0e0bb7da/1699280193802/File+%281%29.jpg"  height="400" /> 
</p>
<p align="center">
   Figure 3
    </p>   
    
#### References
1. M. E. Mungai, G. Prabhakaran, and J. Grizzle, “Fall Prediction for Bipedal Robots: The Standing Phase,” arXiv preprint arXiv:2309.14546 (2023), Submitted to ICRA 2024.
2. G. Gibson, “Terrain-aware bipedal locomotion,” Ph.D. dissertation, University of Michigan, 2023.






