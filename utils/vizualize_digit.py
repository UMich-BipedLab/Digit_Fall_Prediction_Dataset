import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from utils import DynamicsCalculator as dc


def vizualize_digit2D(q_all):
    """
    Vizualize a trajectory over a 2D plot
    """
    # generate all required joint positions
    p_COM = []
    p_left_toe_pitch = []
    p_shin_to_tarsus_left = []
    p_knee_to_shin_left = []
    p_left_knee = []
    p_left_hip_pitch = []
    for q in q_all:
        p_COM.append(dc.get_position(q, "p_COM"))
        p_left_toe_pitch.append(dc.get_position(q, "p_left_toe_pitch"))
        p_shin_to_tarsus_left.append(dc.get_position(q, "p_shin_to_tarsus_left"))
        p_knee_to_shin_left.append(dc.get_position(q, "p_knee_to_shin_left"))
        p_left_knee.append(dc.get_position(q, "p_left_knee"))
        p_left_hip_pitch.append(dc.get_position(q, "p_left_hip_pitch"))
    
    # convert lists to numpy array
    p_COM = np.array(p_COM)
    p_left_toe_pitch = np.array(p_left_toe_pitch)
    p_shin_to_tarsus_left = np.array(p_shin_to_tarsus_left)
    p_knee_to_shin_left = np.array(p_knee_to_shin_left)
    p_left_knee = np.array(p_left_knee)
    p_left_hip_pitch = np.array(p_left_hip_pitch)
    
    # set up plotting
    plt.figure()
    line_1 = plt.plot([0, 0.7071], [0, 0.7071 ], color='red', linewidth=4)[0]
    line_2 = plt.plot([0, 0.7071], [0, 0.7071 ], color='orange', linewidth=4)[0]
    line_3 = plt.plot([0, 0.7071], [0, 0.7071 ], color='yellow', linewidth=4)[0]
    line_4 = plt.plot([0, 0.7071], [0, 0.7071 ],color='green', linewidth=4)[0]
    line_5 = plt.plot([0, 0.7071], [0, 0.7071 ],color='indigo', linewidth=4)[0]   
    dot = plt.plot([0], [0.7071],'*', linewidth=6, color='violet')[0]
    
    plt.axhline(y = 0.0, color = 'black')
    plt.xlim(-1.2, 1.2)
    plt.ylim(-0.2, 1.3)
    
    # index to cut off trajectory if digit robot falls
    cut_off_index = len(q_all)-1
    if p_COM[-1, 2] < 0.5:
        cut_off_index = np.where(p_COM[:, 2] < 0.5)[0][0]
    
    for i in range(0, cut_off_index, 10):
        # get the current join positions
        p_COM_curr = p_COM[i]
        p_left_toe_pitch_curr = p_left_toe_pitch[i]
        p_shin_to_tarsus_left_curr = p_shin_to_tarsus_left[i]
        p_knee_to_shin_left_curr = p_knee_to_shin_left[i]
        p_left_knee_curr = p_left_knee[i]
        p_left_hip_pitch_curr = p_left_hip_pitch[i]
        q_curr = q_all[i]
        
        # set the joint positions to line plots
        line_1.set_data([p_shin_to_tarsus_left_curr[0], p_left_toe_pitch_curr[0]], [p_shin_to_tarsus_left_curr[2], p_left_toe_pitch_curr[2]])
        line_2.set_data([p_knee_to_shin_left_curr[0], p_shin_to_tarsus_left_curr[0]], [p_knee_to_shin_left_curr[2], p_shin_to_tarsus_left_curr[2]])
        line_3.set_data([p_left_knee_curr[0], p_knee_to_shin_left_curr[0]], [p_left_knee_curr[2], p_knee_to_shin_left_curr[2]])
        line_4.set_data([p_left_hip_pitch_curr[0], p_left_knee_curr[0]], [p_left_hip_pitch_curr[2], p_left_knee_curr[2]])
        line_5.set_data([q_curr[0], p_left_hip_pitch_curr[0]], [q_curr[2], p_left_hip_pitch_curr[2]])
        
        # set center of mass position
        dot.set_data([p_COM_curr[0], p_COM_curr[2]])
        
        # print(i)
    
        plt.pause(0.0001)

    plt.show()
    
    
def vizualize_digit3D(q_all):
    """
    Vizualize a trajectory over a 3D plot
    """
    data_dict = {"p_COM":                        np.zeros(shape=(len(q_all), 3)),
                 "p_LeftToeFront":               np.zeros(shape=(len(q_all), 3)),
                 "p_RightToeFront":              np.zeros(shape=(len(q_all), 3)),
                 "p_LeftToeBack":                np.zeros(shape=(len(q_all), 3)),
                 "p_RightToeBack":               np.zeros(shape=(len(q_all), 3)),
                 "p_left_toe_pitch":             np.zeros(shape=(len(q_all), 3)),
                 "p_right_toe_pitch":            np.zeros(shape=(len(q_all), 3)),
                 "p_shin_to_tarsus_left":        np.zeros(shape=(len(q_all), 3)),
                 "p_shin_to_tarsus_right":       np.zeros(shape=(len(q_all), 3)),
                 "p_knee_to_shin_left":          np.zeros(shape=(len(q_all), 3)),
                 "p_knee_to_shin_right":         np.zeros(shape=(len(q_all), 3)),
                 "p_left_knee":                  np.zeros(shape=(len(q_all), 3)),
                 "p_right_knee":                 np.zeros(shape=(len(q_all), 3)),
                 "p_left_hip_pitch":             np.zeros(shape=(len(q_all), 3)),
                 "p_right_hip_pitch":            np.zeros(shape=(len(q_all), 3)),
                 "p_base":                       q_all[:, :3],
                 "p_shoulder_pitch_joint_left":  np.zeros(shape=(len(q_all), 3)),
                 "p_shoulder_pitch_joint_right": np.zeros(shape=(len(q_all), 3)),
                 "p_shoulder_yaw_joint_left":    np.zeros(shape=(len(q_all), 3)),
                 "p_shoulder_yaw_joint_right":   np.zeros(shape=(len(q_all), 3)),
                 "p_elbow_joint_left":           np.zeros(shape=(len(q_all), 3)),
                 "p_elbow_joint_right":          np.zeros(shape=(len(q_all), 3))
                 }
    
    joint_names = list(data_dict.keys())
    
    plot_info = [   # [start_position,                end_position,                  line color]
                    ["p_LeftToeFront",               "p_LeftToeBack",                "black"],
                    ["p_RightToeFront",              "p_RightToeBack",               "black"],
                    ["p_shin_to_tarsus_left",        "p_left_toe_pitch",             "red"],
                    ["p_shin_to_tarsus_right",       "p_right_toe_pitch",            "red"],
                    ["p_knee_to_shin_left",          "p_shin_to_tarsus_left",        "orange"],
                    ["p_knee_to_shin_right",         "p_shin_to_tarsus_right",       "orange"],
                    ["p_left_knee",                  "p_knee_to_shin_left",          "yellow"],
                    ["p_right_knee",                 "p_knee_to_shin_right",         "yellow"],
                    ["p_left_hip_pitch",             "p_left_knee",                  "green"],
                    ["p_right_hip_pitch",            "p_right_knee",                 "green"],
                    ["p_base",                       "p_left_hip_pitch",             "blue"],
                    ["p_base",                       "p_right_hip_pitch",            "blue"],
                    ["p_shoulder_pitch_joint_left",  "p_base",                       "indigo"],
                    ["p_shoulder_pitch_joint_right", "p_base",                       "indigo"],
                    ["p_shoulder_yaw_joint_left",    "p_shoulder_pitch_joint_left",  "slategrey"],
                    ["p_shoulder_yaw_joint_right",   "p_shoulder_pitch_joint_right", "slategrey"],
                    ["p_elbow_joint_left",           "p_shoulder_yaw_joint_left",    "mediumblue"],
                    ["p_elbow_joint_right",          "p_shoulder_yaw_joint_right",   "mediumblue"],
                ]
    
    
    # calculate and store all joint positions in a trajectory                   
    for idx, q in enumerate(q_all):
        for joint_name in joint_names:
            if joint_name == "p_base":
                continue
            data_dict[joint_name][idx, :] = dc.get_position(q, joint_name)
            
            
    # index to cut off trajectory if digit robot falls
    cut_off_index = len(q_all)-1
    if data_dict["p_COM"][-1, 2] < 0.5:
        cut_off_index = np.where(data_dict["p_COM"][:, 2] < 0.5)[0][0]
        
    axes = plt.axes(projection="3d")
    
    for i in range(0, cut_off_index, 20):
        # set up axes
        axes.cla()
        axes.set_xlim3d(left=-1, right=1) 
        axes.set_ylim3d(bottom=-1, top=1) 
        axes.set_zlim3d(bottom=0, top=2) 
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        
        for start_point, end_point, line_color in plot_info:
            axes.plot([data_dict.get(start_point)[i, 0], data_dict.get(end_point)[i, 0]],
                      [data_dict.get(start_point)[i, 1], data_dict.get(end_point)[i, 1]],
                      [data_dict.get(start_point)[i, 2], data_dict.get(end_point)[i, 2]],
                      linewidth=6,
                      color=line_color)
        
        plt.pause(0.0001)
    
    plt.show()
