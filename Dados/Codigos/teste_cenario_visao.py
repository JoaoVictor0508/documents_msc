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

    for line in open(f"C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\testes_mestrado\\teste_cenario_visao_quad_menor\\teste_cenario_visao_quad_menor\\visao_cenario_visao_quadrado_menor_{i:02d}.txt", 'r'): 
        lines_visao.append(line.rstrip().split(";"))

    tamanho_visao = len(lines_visao[1:])
    print(f"Quantidade de amostras Visão: {tamanho_visao}")

    for data in lines_visao[int(0.25*tamanho_visao):int(0.85*tamanho_visao)]:
        pos_x_vision.append(float(data[0])/1000.0)
        pos_y_vision.append(float(data[1])/1000.0)
        pos_theta_vision.append(float(data[2])*180.0/np.pi)

    for line in open(f"C:\\Users\\joaov\\Documents\\GitHub\\documents_msc\\Dados\\testes_mestrado\\teste_cenario_visao_quad_menor\\teste_cenario_visao_quad_menor\\laser_cenario_visao_quadrado_menor_{i:02d}.txt", 'r'): 
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

    for vision_point in np.array(list(zip(pos_x_vision, pos_y_vision))):
        distances = np.linalg.norm(laser_interpolated - vision_point, axis=1)

        min_error = np.min(distances)
        closest_index = np.argmin(distances)
        closest_point = laser_interpolated[closest_index]

        error_x = vision_point[0] - closest_point[0]
        error_y = vision_point[1] - closest_point[1]

        errors_normal_laser.append(abs(min_error))
        
        errors_x_laser.append(pow(error_x, 2))
        errors_y_laser.append(pow(error_y, 2))

        errors_laser.append(pow(min_error, 2))

    print(f"Mean error laser: {np.sqrt(np.mean(errors_laser)):.5f} m".replace('.', ','))
    print(f"Mean error x laser: {np.sqrt(np.mean(errors_x_laser)):.5f} m".replace('.', ','))
    print(f"Mean error y laser: {np.sqrt(np.mean(errors_y_laser)):.5f} m".replace('.', ','))
    print(f"Max error to laser: {np.sqrt(max(errors_laser)):.5f} m".replace('.', ','))
    print(f"{np.sqrt(np.mean(errors_laser)):.5f};{np.sqrt(np.std(errors_laser)):.5f};{np.sqrt(np.mean(errors_x_laser)):.5f};{np.sqrt(np.std(errors_x_laser)):.5f};{np.sqrt(np.mean(errors_y_laser)):.5f};{np.sqrt(np.std(errors_y_laser)):.5f};{np.sqrt(max(errors_laser)):.5f};{tamanho_visao}".replace('.', ','))
    print("##############################################")

    # print(f"{np.sqrt(np.mean(errors_laser)):.5f};{np.sqrt(np.mean(errors_x_laser)):.5f};{np.sqrt(np.mean(errors_y_laser)):.5f};{np.sqrt(max(errors_laser)):.5f}".replace('.', ','))

    plt.figure()

    plt.scatter(interp_x, interp_y, c='black', label='laser interpolated')
    plt.scatter(pos_x_laser, pos_y_laser, c='g', label='Laser')
    plt.scatter(pos_x_vision, pos_y_vision, c='b', label='Vision')
    plt.tight_layout()

    plt.show()