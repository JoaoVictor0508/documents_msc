import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

pos_x_ekf = []
pos_x_ekf_sem_correcao = []
pos_y_ekf = []
pos_y_ekf_sem_correcao = []
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

vel_x_imu = []
vel_y_imu = []
vel_theta_imu = []

pos_x_vision = []
pos_y_vision = []
pos_theta_vision = []
lines_visao = []

pos_x_laser = []
pos_y_laser = []
lines_laser = []

tempo_laser = []

flag_att_pose = []

sum = 0

# for line in open('/home/robofei/Sambashare/teste_cenario_encoder_imu_quad_maior/visao/log_mestrado.txt', 'r'): 
#     lines_visao.append(line.rstrip().split(";"))

# for data in lines_visao:
#     pos_x_vision.append(float(data[0])/1000.0)
#     pos_y_vision.append(float(data[1])/1000.0)
#     pos_theta_vision.append(float(data[2]))

for line in open('C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\teste_integral\\ekf\\teste_5_dia_14.txt'):
    lines_ekf.append(line.rstrip().split(";"))

for data in lines_ekf[1:]:
    pos_x_ekf.append(float(data[0])/1000.0)
    accel_x.append(float(data[1])/1000.0)
    accel_y.append(float(data[2])/1000.0)

    vel_x_imu.append(float(data[3])/1000.0)
    vel_y_imu.append(float(data[4])/1000.0)
    vel_theta_imu.append(float(data[5])/1000.0)

    vel_x_encoder.append(float(data[6])/1000.0)
    vel_y_encoder.append(float(data[7])/1000.0)
    vel_theta_encoder.append(float(data[8])/1000.0)

    pos_y_ekf.append(float(data[9])/1000.0)

    flag_att_pose.append(int(data[11]))

    if(int(data[11]) == 0):
        pos_x_ekf_sem_correcao.append(float(data[0])/1000.0)
        pos_y_ekf_sem_correcao.append(float(data[9])/1000.0)

vx_accel = []
vy_accel = []
for i in range(len(accel_x)-1):
    vx_accel.append(accel_x[i]*0.05 + vel_x_imu[i])
    vy_accel.append(accel_y[i]*0.05 + vel_y_imu[i])

fig = plt.figure()
plt.plot(range(len(vx_accel)), vx_accel, c='r', label='EKF Vel X IMU')
plt.plot(range(len(vel_x_imu)), vel_x_imu, c='g', label='EKF Vel X IMU')
plt.plot(range(len(vel_x_encoder)), vel_x_encoder, c='b', label='Encoder Vel X')
plt.plot(range(len(vel_theta_imu)), vel_theta_imu, c='y', label='EKF Vel State X')


fig = plt.figure()
plt.plot(range(len(vy_accel)), vy_accel, c='r', label='EKF Vel Y IMU')
plt.plot(range(len(vel_y_imu)), vel_y_imu, c='g', label='EKF Vel Y IMU')
plt.plot(range(len(vel_y_encoder)), vel_y_encoder, c='b', label='Encoder Vel Y')
plt.plot(range(len(vel_theta_encoder)), vel_theta_encoder, c='y', label='EKF Vel State Y')

# fig = plt.figure()
# plt.scatter(pos_x_ekf, pos_y_ekf, c='r', label='EKF')
# plt.scatter(pos_x_ekf_sem_correcao, pos_y_ekf_sem_correcao, c='orange', label='EKF sem correção')

for line in open('C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\teste_integral\\laser\\teste_5_dia_14.txt', 'r'): 
    lines_laser.append(line.rstrip().split(";"))

for data in lines_laser:
    tempo_laser.append(sum)
    pos_x_laser.append(float(data[1]))
    pos_y_laser.append(float(data[2]))
    sum += 1

tempo_laser = np.array(tempo_laser)

t_fine = np.linspace(0, len(pos_x_laser), len(pos_x_laser)*5)
interp_x = interp1d(tempo_laser, pos_x_laser, kind='quadratic', fill_value='extrapolate')(t_fine)
interp_y = interp1d(tempo_laser, pos_y_laser, kind='quadratic', fill_value='extrapolate')(t_fine)
# fig = plt.figure()
# ax1 = fig.add_subplot(111)

laser_interpolated = np.array(list(zip(interp_x, interp_y)))

# fig = plt.figure()

# plt.plot(range(len(vel_x_imu)), vel_x_imu, c='r', label='EKF Vel X')
# plt.plot(range(len(vel_x_encoder)), vel_x_encoder, c='g', label='Encoder Vel X')

# fig = plt.figure()

# plt.plot(range(len(vel_y_imu)), vel_y_imu, c='r', label='EKF Vel Y')
# plt.plot(range(len(vel_y_encoder)), vel_y_encoder, c='g', label='Encoder Vel Y')

fig = plt.figure()

plt.plot(range(len(accel_x)), accel_x, c='r', label='EKF Accel X')
plt.plot(range(len(accel_y)), accel_y, c='g', label='EKF Accel Y')

# fig = plt.figure()
# plt.plot(range(len(pos_x_ekf)), pos_x_ekf, c='r', label='EKF')

fig = plt.figure()

plt.scatter(interp_x, interp_y, c='black', label='laser interpolated')
plt.scatter(pos_x_laser, pos_y_laser, c='g', label='Laser')
# axs[2, 1].scatter(pos_x_vision, pos_y_vision, c='b', label='Vision')
plt.scatter(pos_x_ekf, pos_y_ekf, c='r', label='EKF')
plt.scatter(pos_x_ekf_sem_correcao, pos_y_ekf_sem_correcao, c='orange', label='EKF sem correção')

plt.title("Posições do EKF e do laser - 8 segundos sem correção")
plt.legend()

plt.show()