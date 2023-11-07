import numpy as np
import matplotlib.pyplot as plt
from utils import DynamicsCalculator as dc


def vizualize_digit(q_all):
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
    