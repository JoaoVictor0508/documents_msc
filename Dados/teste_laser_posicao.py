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

for line in open('/home/robofei/Sambashare/teste_cenario_encoder_imu_quad_maior/visao/log_mestrado.txt', 'r'): 
    lines_visao.append(line.rstrip().split(";"))

for data in lines_visao:
    pos_x_vision.append(float(data[0])/1000.0)
    pos_y_vision.append(float(data[1])/1000.0)
    pos_theta_vision.append(float(data[2]))


for line in open('/home/robofei/Sambashare/teste_cenario_encoder_imu_quad_maior/ekf/teste.txt'):
    lines_ekf.append(line.rstrip().split(";"))

for data in lines_ekf[1:]:
    pos_x_ekf.append(float(data[0])/1000.0)
    pos_y_ekf.append(float(data[1])/1000.0)
    pos_theta_ekf.append(float(data[2]) * np.pi/180.0)
    vel_x_ekf.append(float(data[3])/1000.0)
    vel_y_ekf.append(float(data[4])/1000.0)

    vel_x_encoder.append(float(data[5])/1000.0)
    vel_y_encoder.append(float(data[6])/1000.0)
    vel_theta_encoder.append(float(data[7])*np.pi/180.0)

    accel_x.append(float(data[8])/1000.0)
    accel_y.append(float(data[9])/1000.0)
    gyro_w.append(float(data[10])*np.pi/180.0)

for line in open('/home/robofei/Sambashare/teste_cenario_encoder_imu_quad_maior/laser/test.txt', 'r'): 
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
vision_data = np.array(list(zip(pos_x_vision, pos_y_vision, pos_theta_vision)))

errors = []
errors_x = []
errors_y = []
errors_theta = []
errors_normal = []
for ekf_point in np.array(list(zip(pos_x_ekf, pos_y_ekf))):
    distances = np.linalg.norm(laser_interpolated - ekf_point, axis=1)

    min_error = np.min(distances)
    closest_index = np.argmin(distances)
    closest_point = laser_interpolated[closest_index]

    error_x = ekf_point[0] - closest_point[0]
    error_y = ekf_point[1] - closest_point[1]

    errors_normal.append(abs(min_error))
    
    errors_x.append(pow(error_x, 2))
    errors_y.append(pow(error_y, 2))

    errors.append(pow(min_error, 2))

print(f"Max error: {np.sqrt(max(errors))}")

print(np.sum(errors)/len(errors))

print(np.sqrt(np.mean(errors_x)))
print(np.sqrt(np.mean(errors_y)))
print(np.sqrt(np.mean(errors)))

log_theta_vision = []

for ekf_point in np.array(list(zip(pos_x_ekf, pos_y_ekf, pos_theta_ekf))):
    distances_vision = np.linalg.norm(vision_data - ekf_point, axis=1)

    min_error_vision = np.min(distances)
    closest_index_vision = np.argmin(distances_vision)
    closest_point_vision = vision_data[closest_index_vision]
    log_theta_vision.append(closest_point_vision[2])
    error_theta = ekf_point[2] - closest_point_vision[2]
    errors_theta.append(error_theta)

# plt.scatter(pos_x_ekf, pos_y_ekf, c='r', label='EKF')
# plt.scatter(interp_x, interp_y, c='black', label='laser interpolated')
# plt.scatter(pos_x_laser, pos_y_laser, c='g', label='Laser')
# plt.scatter(pos_x_vision, pos_y_vision, c='b', label='Vision')

fig, axs = plt.subplots(3, 2)
axs[1, 0].scatter(range(len(log_theta_vision)), log_theta_vision, c='r', label='Vision')
axs[1, 0].scatter(range(len(pos_theta_ekf)), pos_theta_ekf, c='g', label='EKF')

# axs[0, 1].plot(range(len(errors_normal)), errors_normal, c='r')
axs[0, 1].plot(range(len(gyro_w)), gyro_w, c='r', label='Vel Gyro')
axs[0, 1].plot(range(len(vel_theta_encoder)), vel_theta_encoder, c='g', label='Vel Encoder')

axs[0, 0].plot(range(len(errors_theta)), errors_theta, c='r', label='Error Orientation')

axs[1, 1].plot(range(len(accel_x)), accel_x, c='r', label='Accel X')
axs[1, 1].plot(range(len(accel_y)), accel_y, c='g', label='Accel Y')

axs[2, 0].plot(range(len(vel_x_encoder)), vel_x_encoder, c='r', label='Vel Theo')
axs[2, 0].plot(range(len(vel_x_ekf)), vel_x_ekf, c='g', label='Vel EKF')

axs[2, 1].scatter(interp_x, interp_y, c='black', label='laser interpolated')
axs[2, 1].scatter(pos_x_laser, pos_y_laser, c='g', label='Laser')
axs[2, 1].scatter(pos_x_vision, pos_y_vision, c='b', label='Vision')
axs[2, 1].scatter(pos_x_ekf, pos_y_ekf, c='r', label='EKF')

# plt.scatter(range(len(errors_theta)), errors_theta, c='r', label='Error Orientation')
# plt.scatter(range(len(log_theta_vision)), log_theta_vision, c='r', label='Vision')
# plt.scatter(range(len(pos_theta_ekf)), pos_theta_ekf, c='g', label='EKF')

# plt.xlabel("X (m)")
# plt.ylabel("Y (m)")
# plt.title("Teste 1")

# plt.plot(range(len(vel_x_theo)), vel_x_theo, c='g', label='Vel X Theo')
# plt.plot(range(len(vel_x_encoder)), vel_x_encoder, c='b', label='Vel X Encoder')
# plt.plot(range(len(vel_x_ekf)), vel_x_ekf, c='r', label='Vel X EKF')

# plt.plot(range(len(accel_x)), accel_x, c='g', label='Accel X')
# plt.plot(range(len(accel_y)), accel_y, c='r', label='Accel Y')

# plt.plot(range(len(vel_theta_encoder)), vel_theta_encoder, c='g', label='Vel W Encoder')
# plt.plot(range(len(gyro_w)), gyro_w, c='r', label='Gyro W')

# plt.plot(range(len(vel_y_encoder)), vel_y_encoder, c='b', label='Vel Y Encoder')
# plt.plot(range(len(vel_y_ekf)), vel_y_ekf, c='r', label='Vel Y EKF')
# plt.plot(range(len(vel_y_theo)), vel_y_theo, c='g', label='Vel Y Theo')

# plt.plot(range(len(vel_theta_encoder)), vel_theta_encoder, c='b', label='Vel Theta Encoder')
# plt.plot(range(len(vel_theta_theo)), vel_theta_theo, c='g', label='Vel Theta Theo')

plt.legend()

plt.show()