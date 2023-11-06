import numpy as np
import DynamicsCalculator as dc

def vizualize_digit(q):

    dir=feat_info['dir']
    file_name=feat_info['file_name']
    mat=spio.loadmat(dir+file_name, struct_as_record=False, squeeze_me=True)
    data=mat['stab_data']
    x=data.x_all
    q=x[0:6,:]
    t=data.t_all
    if 'cont' in feat_info['file_name']:
        # feat_info['truncate_beginning']=1
        t_start=0.26    
        start_idx=np.where(t>=t_start)[0][0]
        t = (t-t[start_idx])

    [row_num, col_num] = q.shape

    if stop_idx == 10.5:
        stop_idx= col_num
  
    if hasattr(data,'f_ext_all'):
        f_ext= data.f_ext_all
    else:
        f_ext=np.zeros((2,x.shape[-1]))

    
    p_com=data.p_com

    
    p_toe=data.p_toe
    p_heel=data.p_heel
    Ptorso = Ptorso_fun(q)
    Phip = Phip_fun(q)
    Pknee = Pknee_fun(q)


    plt.figure()
    line_1 = plt.plot([0, 0.7071], [0, 0.7071 ], color='blue', linewidth=4)[0]
    line_2 = plt.plot([0, 0.7071], [0, 0.7071 ], color='black', linewidth=4)[0]
    line_3 = plt.plot([0, 0.7071], [0, 0.7071 ], color='red', linewidth=4)[0]
    line_4 = plt.plot([0, 0.7071], [0, 0.7071 ],color='blue', linewidth=4)[0]
    dot1 = plt.plot([0], [0.7071],'*', linewidth=6, color='green')[0]
    plt.axhline(y = 0.0, color = 'black')
    plt.xlim(-0.5,4.6)
    plt.ylim(-0.5,1.6)

    for i in range(start_idx,stop_idx):
        Pknee_now= Pknee[:,i]
        Phip_now = Phip[:,i]
        Ptorso_now = Ptorso[:,i]
        Pfoot_now=q[0:2,i]
        Pheel_now=p_heel[:,i]
        Ptoe_now = p_toe[:,i]
        Pcom_now=p_com[:,i]
        
        line_1.set_data([Ptoe_now[0], Pheel_now[0]], [Ptoe_now[1],Pheel_now[1] ])
        line_2.set_data([Pfoot_now[0], Pknee_now[0]], [Pfoot_now[1],Pknee_now[1] ])
        line_3.set_data([Pknee_now[0], Phip_now[0]], [Pknee_now[1],Phip_now[1] ])
        line_4.set_data([Phip_now[0], Ptorso_now[0]], [Phip_now[1],Ptorso_now[1] ])
        dot1.set_data([Pcom_now[0]], [Pcom_now[1]])
        # plt.axhline(y = 0.0, color = 'black')

        if t[i] >= t_fall_predicted:
            plt.text(1,1.5, 'fall predicted', fontsize='large')
            plt.text(1,1.25, 't_fall_predicted: ' + str(t[i]), fontsize='large')
            plt.text(1,1.0, 'escape time: ' + str(t_escape), fontsize='large')
            break

        plt.pause(1e-8)

    plt.show()    