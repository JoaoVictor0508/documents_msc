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

for i in range(1, 11, 1):
    print(f"Scenario {i}")

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
    accel_y = []
    gyro_z = []
    lines_ekf = []

    pos_x_vision = []
    pos_y_vision = []
    pos_theta_vision = []
    lines_visao = []

    pos_x_laser = []
    pos_y_laser = []
    lines_laser = []

    tempo_laser = []
    error_scenarios = []
    error_x_scenarios = []
    error_y_scenarios = []
    error_theta_scenarios = []
    sum = 0

    for line in open(f"C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\testes_mestrado\\teste_cenario_encoder_imu_quad_maior\\teste_cenario_encoder_imu_quad_maior\\visao\\visao_cenario_encoder_imu_quad_maior_{i:02d}.txt", 'r'):
        lines_visao.append(line.rstrip().split(";"))

    for data in lines_visao[1:]:
        pos_x_vision.append(float(data[0])/1000.0)
        pos_y_vision.append(float(data[1])/1000.0)
        pos_theta_vision.append(float(data[2])*180.0/np.pi)

    for line in open(f"C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\testes_mestrado\\teste_cenario_encoder_imu_quad_maior\\teste_cenario_encoder_imu_quad_maior\\ekf\\ekf_cenario_encoder_imu_quad_maior_{i:02d}.txt", 'r'):
        lines_ekf.append(line.rstrip().split(";"))

    tamanho_ekf = len(lines_ekf[1:])
    print(f"Quantidade de amostras EKF: {tamanho_ekf}")

    for data in lines_ekf[int(0.30*tamanho_ekf):int(0.88*tamanho_ekf)]:
        pos_x_ekf.append(float(data[0])/1000.0)
        pos_y_ekf.append(float(data[1])/1000.0)
        pos_theta_ekf.append(float(data[2])) #*np.pi/180.0)
        vel_x_ekf.append(float(data[3])/1000.0)
        vel_y_ekf.append(float(data[4])/1000.0)

        vel_x_encoder.append(float(data[5])/1000.0)
        vel_y_encoder.append(float(data[6])/1000.0)
        vel_theta_encoder.append(float(data[7])) #*np.pi/180.0)

        accel_x.append(float(data[8])/1000.0)
        accel_y.append(float(data[9])/1000.0)
        gyro_z.append(float(data[10])) #*np.pi/180.0)

    for line in open(f"C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\testes_mestrado\\teste_cenario_encoder_imu_quad_maior\\teste_cenario_encoder_imu_quad_maior\\laser\\laser_cenario_encoder_imu_quad_maior_{i:02d}.txt", 'r'): 
        lines_laser.append(line.rstrip().split(";"))

    for data in lines_laser[1:]:
        tempo_laser.append(sum)
        pos_x_laser.append(float(data[1]))
        pos_y_laser.append(float(data[2]))
        sum += 1

    tempo_laser = np.array(tempo_laser)

    t_fine = np.linspace(0, len(pos_x_laser), len(pos_x_laser)*5)
    interp_x = interp1d(tempo_laser, pos_x_laser, kind='quadratic', fill_value='extrapolate')(t_fine)
    interp_y = interp1d(tempo_laser, pos_y_laser, kind='quadratic', fill_value='extrapolate')(t_fine)

    laser_interpolated = np.array(list(zip(interp_x, interp_y)))
    vision_data = np.array(list(zip(pos_x_vision, pos_y_vision, pos_theta_vision)))

    errors_laser = []
    errors_x_laser = []
    errors_y_laser = []
    errors_normal_laser = []

    errors_vision = []
    errors_x_vision = []
    errors_y_vision = []
    errors_theta_vision = []

    for ekf_point in np.array(list(zip(pos_x_ekf, pos_y_ekf))):
        distances = np.linalg.norm(laser_interpolated - ekf_point, axis=1)

        min_error = np.min(distances)
        closest_index = np.argmin(distances)
        closest_point = laser_interpolated[closest_index]

        error_x = ekf_point[0] - closest_point[0]
        error_y = ekf_point[1] - closest_point[1]

        errors_normal_laser.append(abs(min_error))
        
        errors_x_laser.append(pow(error_x, 2))
        errors_y_laser.append(pow(error_y, 2))

        errors_laser.append(pow(min_error, 2))

    print(f"Mean error laser: {np.sqrt(np.mean(errors_laser)):.5f} m".replace('.', ','))
    print(f"Mean error x laser: {np.sqrt(np.mean(errors_x_laser)):.5f} m".replace('.', ','))
    print(f"Mean error y laser: {np.sqrt(np.mean(errors_y_laser)):.5f} m".replace('.', ','))
    print(f"Max error to laser: {np.sqrt(max(errors_laser)):.5f} m".replace('.', ','))
    print("##############################################")

    log_theta_vision = []

    for ekf_point in np.array(list(zip(pos_x_ekf, pos_y_ekf, pos_theta_ekf))):
        distances = np.linalg.norm(vision_data[:, :2] - ekf_point[:2], axis=1)

        min_error = np.min(distances)
        closest_index = np.argmin(distances)
        closest_point_vision = vision_data[closest_index]

        log_theta_vision.append(closest_point_vision[2])

        error_x = ekf_point[0] - closest_point_vision[0]
        error_y = ekf_point[1] - closest_point_vision[1]
        error_theta = ekf_point[2] - closest_point_vision[2]
        
        errors_x_vision.append(pow(error_x, 2))
        errors_y_vision.append(pow(error_y, 2))
        errors_theta_vision.append(pow(error_theta, 2))

        errors_vision.append(pow(min_error, 2))

    print(f"Mean error vision: {np.sqrt(np.mean(errors_vision)):.5f} m".replace('.', ','))
    print(f"Mean error x vision: {np.sqrt(np.mean(errors_x_vision)):.5f} m".replace('.', ','))
    print(f"Mean error y vision: {np.sqrt(np.mean(errors_y_vision)):.5f} m".replace('.', ','))
    print(f"Max error to vision: {np.sqrt(max(errors_vision)):.5f} m".replace('.', ','))
    print(f"Mean error theta: {np.sqrt(np.mean(errors_theta_vision)):.5f} degrees".replace('.', ','))
    print(f"Max error theta to vision: {np.sqrt(max(errors_theta_vision)):.5f} degrees".replace('.', ','))
    # print(f"{np.sqrt(np.mean(errors_laser)):.5f};{np.sqrt(np.mean(errors_x_laser)):.5f};{np.sqrt(np.mean(errors_y_laser)):.5f};{np.sqrt(max(errors_laser)):.5f};{np.sqrt(np.mean(errors_vision)):.5f};{np.sqrt(np.mean(errors_x_vision)):.5f};{np.sqrt(np.mean(errors_y_vision)):.5f};{np.sqrt(max(errors_vision)):.5f};{np.sqrt(np.mean(errors_theta_vision)):.5f};{np.sqrt(max(errors_theta_vision)):.5f};{tamanho_ekf}".replace('.', ','))
    print(f"{np.sqrt(np.mean(errors_laser)):.5f};{np.sqrt(np.std(errors_laser)):.5f};{np.sqrt(np.mean(errors_x_laser)):.5f};{np.sqrt(np.std(errors_x_laser)):.5f};{np.sqrt(np.mean(errors_y_laser)):.5f};{np.sqrt(np.std(errors_y_laser)):.5f};{np.sqrt(max(errors_laser)):.5f};{np.sqrt(np.mean(errors_vision)):.5f};{np.sqrt(np.std(errors_vision)):.5f};{np.sqrt(np.mean(errors_x_vision)):.5f};{np.sqrt(np.std(errors_x_vision)):.5f};{np.sqrt(np.mean(errors_y_vision)):.5f};{np.sqrt(np.std(errors_y_vision)):.5f};{np.sqrt(max(errors_vision)):.5f};{np.sqrt(np.mean(errors_theta_vision)):.5f};{np.sqrt(np.std(errors_theta_vision)):.5f};{np.sqrt(max(errors_theta_vision)):.5f};{tamanho_ekf}".replace('.', ','))

    # plt.figure()
    # plt.plot(range(len(errors_theta_vision)), errors_theta_vision, c='r', label='Theta')

    # plt.figure()
    # plt.title(f"Erro - Teste {i}")

    # plt.plot(range(len(errors_y_vision)), errors_y_vision, c='b', label='Y')
    # plt.plot(range(len(errors_vision)), errors_vision, c='g', label='Normal')
    # plt.plot(range(len(errors_x_vision)), errors_x_vision, c='r', label='X')

    fig = plt.figure()

    plt.scatter(range(len(log_theta_vision)), log_theta_vision, c='r', label='Visão')
    plt.scatter(range(len(pos_theta_ekf)), pos_theta_ekf, c='g', label='EKF')
    plt.xlabel('Amostras')
    plt.ylabel('Theta (graus)')
    plt.legend()
    plt.tight_layout()

    plt.figure()

    plt.scatter(pos_x_ekf, pos_y_ekf, c='r', label='EKF')
    plt.scatter(interp_x, interp_y, c='black', label='laser interpolated')
    plt.scatter(pos_x_laser, pos_y_laser, c='g', label='Laser')
    plt.scatter(pos_x_vision, pos_y_vision, c='b', label='Vision')
    plt.tight_layout()

    # plt.figure()

    # plt.title(f"Velocidade em X - Teste {i}")

    # plt.plot(range(len(vel_x_encoder)), vel_x_encoder, c='b', label='Encoder')
    # plt.plot(range(len(vel_x_ekf)), vel_x_ekf, c='r', label='Vel X EKF')
    # plt.tight_layout()

    # plt.figure()

    # plt.title(f"Velocidade em Y - Teste {i}")

    # plt.plot(range(len(vel_y_encoder)), vel_y_encoder, c='b', label='Encoder')
    # plt.plot(range(len(vel_y_ekf)), vel_y_ekf, c='r', label='Vel Y EKF')
    # plt.tight_layout()

    # plt.figure()
    # plt.title(f"Acelerações - Teste {i}")

    # plt.plot(range(len(accel_x)), accel_x, c='b', label='Aceleração X')
    # plt.plot(range(len(accel_y)), accel_y, c='r', label='Aceleração Y')

    # plt.tight_layout()

    plt.show()