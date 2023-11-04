import os
import sys

curr_dir, _ = os.path.split(os.path.realpath(__file__))
SRC_DIR = os.path.join(curr_dir, "..", "src")
sys.path.append(SRC_DIR)

import numpy as np
from typing import Dict
from DynamicsCalculator import DynamicsCalculator
from RosbagParser import RosbagParser


class DatasetLoader():
    def __init__(self) -> None:
        self.pos_data = None
        self.ang_mom_data = None
        self.time_data = None
        self.vel_data = None
        self.q_data = None
        self.qdot_data = None
        self.trajectories = None
        self.trajectory_info = {}
    
    
    def load_dataset(self,
                     transform_real_trajectories: bool,
                     remove_hardware_data_after_killed: bool,
                     subtract_initial_angle_sim: bool):
        """
        Loads the digit dataset. This includes q, qdot, time, position, velocity and angular momentum data.

        Args
        ----
        transform_real_trajectories: bool
            A flag to transform the real/hardware trajectories to the world coordinates
        remove_hardware_data_after_killed: bool
            A flag to remove all hardware data after the robot is killed/e-stopped
        subtract_initial_angle_sim: bool
            A flag to subtract the inital q and qdot values from the rest of the q and qdot values
        """
        generate = False
        rosbag_parser = RosbagParser()
        dyn_calc = DynamicsCalculator(rosbag_parser=rosbag_parser)

        self.pos_data, self.vel_data, self.ang_mom_data,\
            self.time_data, self.q_data, self.qdot_data,\
                self.command_torque_data, self.motor_torque_measured_data, self.real_labels = dyn_calc.get_all_data_in_all_rosbags(generate=generate)

        self.trajectories = list(self.pos_data.keys())
        self.extract_trajectory_info()
        
        # make changes to the hardware data
        if transform_real_trajectories:
            self.transform_real_trajectories()
        if remove_hardware_data_after_killed:
            self.remove_hardware_data_after_killed()
            
        # make changes to the sim data
        if subtract_initial_angle_sim:
            self.subtract_initial_angle_sim()
        
    
    
    def transform_real_trajectories(self):
        """
        Transforms real/hardware trajectories to the correct frame of reference
        """
        yaw_angle_offsets = {}
        pos_offsets = {}
        for traj in self.q_data:
            yaw_angle_offsets[traj] = self.q_data[traj][0, 3]
            pos_offsets[traj] = self.q_data[traj][0, 0:3]
        def get_z_transform_mat(yaw_angle_offset, pos_offset):
            z_rot_mat = np.array([[np.cos(yaw_angle_offset), -np.sin(yaw_angle_offset), 0.0],\
                                  [np.sin(yaw_angle_offset), np.cos(yaw_angle_offset),  0.0],\
                                  [0.0,                      0.0,                       1.0]])
            z_transform_mat = np.identity(4)
            z_transform_mat[:3, :3] = z_rot_mat
            z_transform_mat[:3, 3] = pos_offset
            return np.linalg.inv(z_transform_mat)
        
        for traj in self.pos_data:
            if self.is_real_data(trajectory=traj):
                z_transform_mat = get_z_transform_mat(yaw_angle_offsets[traj], pos_offsets[traj])
                # transform relative com position and contact position
                self.pos_data[traj]["p_COM_rel"] = self.pos_data[traj]["p_COM_rel"] @ z_transform_mat[:3, :3].T
                row, col = self.pos_data[traj]["p_contact"].shape
                p_contact = np.ones((row, col+1))
                p_contact[:, :3] = self.pos_data[traj]["p_contact"]
                self.pos_data[traj]["p_contact"] = (p_contact @ z_transform_mat.T)[:, :3]

                # transform velocity
                self.vel_data[traj]["v_COM"] = self.vel_data[traj]["v_COM"] @ z_transform_mat[:3, :3].T

                # transform relative com and contact angular momentum
                self.ang_mom_data[traj]["p_COM_rel"] = self.ang_mom_data[traj]["p_COM_rel"] @ z_transform_mat[:3, :3].T
                self.ang_mom_data[traj]["p_contact"] = self.ang_mom_data[traj]["p_contact"] @ z_transform_mat[:3, :3].T
                
    
    def is_real_data(self, trajectory: str):
        """
        Checks if a trajectory is real/hardware

        Args
        ----
        trajectory: str
            The trajectory to check

        Returns:
            True if it is a real/hardware trajectory. False, otherwise
        """
        return "hardware" in trajectory
    
    
    def is_sim_data(self, trajectory: str):
        """
        Checks if a trajectory is simulation

        Args
        ----
        trajectory: str
            The trajectory to check

        Returns:
            True if it is a simulation trajectory. False, otherwise
        """
        return "sim" in trajectory
    
    
    def extract_trajectory_info(self):
        """
        Extracts information about a trajectory

        Args
        ----
        trajectory: str
            The trajectory to check
        """
        for traj in self.trajectories:
            info = {"hardware_data": self.is_real_data(traj),
                    "force_type": "slow" if self.is_slow_acting(traj) else "fast",
                    "time_of_force_application": self.get_t_force_applied(traj),
                    "time_of_pertubation_application": 6.0,
                    "force_magnitude": self.get_force_applied(traj),
                    "pertubation_magnitude": self.get_pertubation_force_applied(traj)}
            self.trajectory_info[traj] = info
            
    
    def is_slow_acting(self, trajectory: str):
        """
        Checks if a trajectory is a slow-acting/incipient one

        Args
        ----
        trajectory: str
            The trajectory to check

        Returns:
            True if it is a slow-acting/incipient trajectory. False, otherwise
        """
        return "fd_1.0" in trajectory or "slow" in trajectory
    
    
    def get_t_force_applied(self, trajectory: str):
        if self.is_real_data(trajectory=trajectory):
            return None
        info = trajectory.replace(".bag", "").split("_")
        ft_idx = info.index("ft")
        return float(info[ft_idx+1])
    
    
    def get_force_applied(self, trajectory: str):
        if self.is_real_data(trajectory=trajectory):
            return None
        info = trajectory.replace(".bag", "").split("_")
        ft_idx = info.index("f")
        return float(info[ft_idx+1])

    
    def get_pertubation_force_applied(self, trajectory: str):
        if self.is_real_data(trajectory=trajectory):
            return None
        info = trajectory.replace(".bag", "").split("_")
        ft_idx = info.index("pertb")
        return float(info[ft_idx+1])
    
    
    def remove_hardware_data_after_killed(self):
        for traj in self.trajectories:
            if self.is_real_data(traj):
                try:
                    motor_killed_idx = np.where(self.motor_torque_measured_data[traj][:, 3]==0)[0][0] # using 3rd index just because (it should be the knee)
                except IndexError:
                    motor_killed_idx = len(self.motor_torque_measured_data[traj])

            self.pos_data, self.vel_data, self.ang_mom_data,\
                self.q_data, self.qdot_data, self.command_torque_data,\
                    self.motor_torque_measured_data, self.time_data = self._truncate_data_helper(
                                                                            start_idx=0,
                                                                            end_idx=motor_killed_idx-1,
                                                                            traj=traj,
                                                                            pos_data=self.pos_data,
                                                                            vel_data=self.vel_data,
                                                                            ang_mom_data=self.ang_mom_data,
                                                                            q_data=self.q_data,
                                                                            qdot_data=self.qdot_data,
                                                                            command_torque_data=self.command_torque_data,
                                                                            motor_torque_measured_data=self.motor_torque_measured_data,
                                                                            time_data=self.time_data
                                                                            )
        
        
    def subtract_initial_angle_sim(self):
        for traj in self.time_data:
            if self.is_sim_data(traj):
                self.q_data[traj] -= self.q_data[traj] - self.q_data[traj][0]
                self.qdot_data[traj] -= self.q_data[traj] - self.q_data[traj][0]                  
            
    
    def _truncate_data_helper(self,
                            start_idx: int,
                            end_idx: int,
                            traj: str,
                            pos_data: Dict[str, Dict[str, np.ndarray]],
                            vel_data: Dict[str, Dict[str, np.ndarray]],
                            ang_mom_data: Dict[str, Dict[str, np.ndarray]],
                            q_data: Dict[str, np.ndarray],
                            qdot_data: Dict[str, np.ndarray],
                            command_torque_data: Dict[str, np.ndarray],
                            motor_torque_measured_data: Dict[str, np.ndarray],
                            time_data: Dict[str, np.ndarray]):
        """
        A helper function to truncate data. It truncates features, given
        a start and an end index.

        Args
        ----
        start_idx: int
            The start index to keep (inclusive) data from
        end_idx: int
            The end index (inclusive) to keep data to
        traj: str
            The trajectory that needs to be truncated
        pos_data: Dict[str, Dict[str, np.ndarray]]
            The position data that needs to be truncated
        vel_data: Dict[str, Dict[str, np.ndarray]]
            The velocity data that needs to truncated
        ang_mom_data: Dict[str, Dict[str, np.ndarray]]
            The angular momentum data that needs to be truncated
        q_data: Dict[str, np.ndarray
            The q data that needs to be truncated
        qdot_data: Dict[str, np.ndarray
            The qdot data that needs to be truncated
        command_torque_data: Dict[str, np.ndarray]
            The command torque data that needs to be truncated
        motor_torque_measured_data: Dict[str, np.ndarray]
            The motor torque measured data that needs to be truncated
        time_data: Dict[str, np.ndarray]
            The time data that needs to be truncated

        Returns
        -------
        pos_data_trunc: dict
            Truncated position data
        ang_mom_data_trunc: dict
            Truncated angular momentum data
        vel_data_trunc: dict
            Trucated velocity data
        q_data_trunc: dict
            Trucated q data
        qdot_data_trunc: dict
            Trucated qdot data
        command_torque_data_trunc: dict
            Trucated qdot data
        motor_torque_measured_data_trunc: dict
            Trucated qdot data
        time_data_trunc: dict
            Truncated time data
        """
        assert end_idx >= 0 and start_idx >= 0

        # truncate the position data
        for link in pos_data[traj]:
            pos_data[traj][link] = pos_data[traj][link][start_idx:end_idx+1, :]

        # truncate the angular momentum data
        for link in ang_mom_data[traj]:
            ang_mom_data[traj][link] = ang_mom_data[traj][link][start_idx:end_idx+1, :]

        # truncate the end of velocity data
        for link in vel_data[traj]:
            vel_data[traj][link] = vel_data[traj][link][start_idx:end_idx+1, :]

        # truncate the end portion of 1 data
        q_data[traj] = q_data[traj][start_idx:end_idx+1, :]

        # truncate the end portion of qdot data
        qdot_data[traj] = qdot_data[traj][start_idx:end_idx+1, :]
        
        # truncate the end portion of command torque data
        command_torque_data[traj] = command_torque_data[traj][start_idx:end_idx+1, :]

        # truncate the end portion of motor torque measured data
        motor_torque_measured_data[traj] = motor_torque_measured_data[traj][start_idx:end_idx+1, :]

        # truncate the end portion of time data
        time_data[traj] = time_data[traj][start_idx:end_idx+1]

        return pos_data, vel_data, ang_mom_data, q_data, qdot_data, command_torque_data, motor_torque_measured_data, time_data
    

if __name__ == "__main__":
    dl = DatasetLoader()
    dl.load_dataset(transform_real_trajectories=True, remove_hardware_data_after_killed=True)
    print("end ")
    