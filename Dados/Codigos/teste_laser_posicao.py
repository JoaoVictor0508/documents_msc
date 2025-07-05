import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

pos_x_ekf = []
pos_y_ekf = []
pos_theta_ekf = []
vel_x_ekf = []
vel_x_theo = []
vel_x_encoder = []
vel_y_ekf = []
vel_y_theo = []
vel_y_encoder = []
vel_theta_encoder = []
vel_theta_theo = []
accel_x = []
accel_y =[]
gyro_w = []
lines_ekf = []

pos_x_vision = []
pos_y_vision = []
pos_theta_vision = []
lines_visao = []

pos_x_laser = []
pos_y_laser = []
lines_laser = []

tempo_laser = []

sum = 0

flag_att_pose = []
pos_x_ekf_sem_correcao = []
pos_y_ekf_sem_correcao = []

for line in open('C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\testes_mestrado\\teste_cenario_encoder_visao_quad_maior\\teste_cenario_encoder_visao_quad_maior\\ekf\\teste_final_sem_visao_8s.txt'):
    lines_ekf.append(line.rstrip().split(";"))

for data in lines_ekf[1:]:
    pos_x_ekf.append(float(data[0])/1000.0)
    pos_y_ekf.append(float(data[1])/1000.0)

    flag_att_pose.append(int(data[11]))

    if(int(data[11]) == 0):
        pos_x_ekf_sem_correcao.append(float(data[0])/1000.0)
        pos_y_ekf_sem_correcao.append(float(data[1])/1000.0)

for line in open('C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\testes_mestrado\\teste_cenario_encoder_visao_quad_maior\\teste_cenario_encoder_visao_quad_maior\\laser\\teste_final_sem_visao_8s_editado.txt', 'r'): 
    lines_laser.append(line.rstrip().split(";"))

for data in lines_laser:
    tempo_laser.append(sum)
    pos_x_laser.append(float(data[1]))
    pos_y_laser.append(float(data[2]))
    sum += 1

t_fine = np.linspace(0, len(pos_x_laser), len(pos_x_laser)*5)
interp_x = interp1d(tempo_laser, pos_x_laser, kind='quadratic', fill_value='extrapolate')(t_fine)
interp_y = interp1d(tempo_laser, pos_y_laser, kind='quadratic', fill_value='extrapolate')(t_fine)

laser_interpolated = np.array(list(zip(interp_x, interp_y)))
vision_data = np.array(list(zip(pos_x_vision, pos_y_vision, pos_theta_vision)))

fig = plt.figure()

plt.scatter(interp_x, interp_y, c='black', label='Ground Truth')
# plt.scatter(pos_x_laser, pos_y_laser, c='g', label='Laser')
# axs[2, 1].scatter(pos_x_vision, pos_y_vision, c='b', label='Vision')
plt.scatter(pos_x_ekf, pos_y_ekf, c='r', label='EKF')
plt.scatter(pos_x_ekf_sem_correcao, pos_y_ekf_sem_correcao, c='b', label='EKF without SSL-Vision')
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.tight_layout()

plt.legend()

plt.show()









# for line in open('C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\teste_integral\\ekf\\teste_5_dia_14.txt'):
#     lines_ekf.append(line.rstrip().split(";"))

# for data in lines_ekf[1:]:
#     pos_x_ekf.append(float(data[0])/1000.0)
#     pos_y_ekf.append(float(data[9])/1000.0)

#     flag_att_pose.append(int(data[11]))

#     if(int(data[11]) == 0):
#         pos_x_ekf_sem_correcao.append(float(data[0])/1000.0)
#         pos_y_ekf_sem_correcao.append(float(data[9])/1000.0)

# for line in open('C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\teste_integral\\laser\\teste_5_dia_14.txt', 'r'): 
#     lines_laser.append(line.rstrip().split(";"))

# for data in lines_laser:
#     tempo_laser.append(sum)
#     pos_x_laser.append(float(data[1]))
#     pos_y_laser.append(float(data[2]))
#     sum += 1

# t_fine = np.linspace(0, len(pos_x_laser), len(pos_x_laser)*5)
# interp_x = interp1d(tempo_laser, pos_x_laser, kind='quadratic', fill_value='extrapolate')(t_fine)
# interp_y = interp1d(tempo_laser, pos_y_laser, kind='quadratic', fill_value='extrapolate')(t_fine)

# laser_interpolated = np.array(list(zip(interp_x, interp_y)))
# vision_data = np.array(list(zip(pos_x_vision, pos_y_vision, pos_theta_vision)))

# fig = plt.figure()

# plt.scatter(interp_x, interp_y, c='black', label='Ground Truth')
# # plt.scatter(pos_x_laser, pos_y_laser, c='g', label='Laser')
# # axs[2, 1].scatter(pos_x_vision, pos_y_vision, c='b', label='Vision')
# plt.scatter(pos_x_ekf, pos_y_ekf, c='r', label='EKF')
# plt.scatter(pos_x_ekf_sem_correcao, pos_y_ekf_sem_correcao, c='b', label='EKF without SSL-Vision')
# plt.xlabel("X (m)")
# plt.ylabel("Y (m)")
# plt.tight_layout()

# plt.legend()

# plt.show()