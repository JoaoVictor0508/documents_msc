import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Caminho do arquivo
file_path = "C:\\Users\\joaov\\OneDrive\\Documentos\\resultados_mestrado.xlsx"

# Carrega todas as abas do Excel em um dicionário de DataFrames
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# Exibe os nomes das abas para confirmação
print(sheet_names)

cenarios = [
    'Visão',
    'Encoder + IMU',
    'Encoder + Visão',
    'IMU + Encoder',
    'IMU + Visão',
    'Modelo + IMU',
    'Modelo + Encoder',
    'Modelo + Visão'
]

cenarios_artigo_rc = [
    'Modelo + Visão',
    'IMU + Visão',
    'Encoder + Visão',
    'Visão'
]

cenarios_artigo_rc_names = [
    'Model + Vision',
    'IMU + Vision',
    'Encoder + Vision',
    'Vision'
]

df = []
df_robocup = []

for sheet_name in cenarios:
    df.append(pd.read_excel(file_path, sheet_name=sheet_name))

for sheet_name in cenarios_artigo_rc:
    df_robocup.append(pd.read_excel(file_path, sheet_name=sheet_name))

print(df[0].head())
print(df[1].head())

print(df[2]['Erro médio - Laser'][0:11])

# plt.figure()

# bplots = plt.boxplot(df[3]['Erro médio - Laser'][0:11],  vert = 0, patch_artist = False)
# plt.boxplot(df[4]['Erro médio - Laser'][0:11],  vert = 0, patch_artist = False, positions=[1])

data_menor = []
data_menor_media=[]
data_maior = []
data_maior_media = []

data_menor_orientacao = []
data_maior_orientacao = []
data_menor_orientacao_media = []
data_maior_orientacao_media = []
data_menor_orientacao_maximo = []
data_maior_orientacao_maximo = []
data_menor_orientacao_maximo_media = []
data_maior_orientacao_maximo_media = []

data_menor_erro_distancia_maximo = []
data_menor_erro_distancia_maximo_media = []
data_maior_erro_distancia_maximo = []
data_maior_erro_distancia_maximo_media = []

for i in range(len(df)):
    data_menor.append(df[i]['Erro médio - Laser'][0:11])
    data_menor_media.append(np.mean(df[i]['Erro médio - Laser'][0:11]))
    data_maior.append(df[i]['Erro médio - Laser'][12:23])
    data_maior_media.append(np.mean(df[i]['Erro médio - Laser'][12:23]))

    data_menor_erro_distancia_maximo.append(df[i]['Erro máximo - Laser'][0:11])
    data_menor_erro_distancia_maximo_media.append(np.mean(df[i]['Erro máximo - Laser'][0:11]))

    data_maior_erro_distancia_maximo.append(df[i]['Erro máximo - Laser'][12:23])
    data_maior_erro_distancia_maximo_media.append(np.mean(df[i]['Erro máximo - Laser'][12:23]))

    if i != 0:
        data_menor_orientacao.append(df[i]['Erro médio Theta - Visão'][0:11])
        data_maior_orientacao.append(df[i]['Erro médio Theta - Visão'][12:23])
        data_menor_orientacao_media.append(np.mean(df[i]['Erro médio Theta - Visão'][0:11]))
        data_maior_orientacao_media.append(np.mean(df[i]['Erro médio Theta - Visão'][12:23]))
        data_menor_orientacao_maximo.append(df[i]['Erro max Theta - Visão'][0:11])
        data_maior_orientacao_maximo.append(df[i]['Erro max Theta - Visão'][12:23])
        data_menor_orientacao_maximo_media.append(np.mean(df[i]['Erro max Theta - Visão'][0:11]))
        data_maior_orientacao_maximo_media.append(np.mean(df[i]['Erro max Theta - Visão'][12:23]))

data_menor_robocup = []
data_menor_media_robocup = []
data_maior_robocup = []
data_maior_media_robocup = []

data_menor_erro_distancia_maximo_robocup = []
data_maior_erro_distancia_maximo_robocup = []

for i in range(len(df_robocup)):
    data_menor_robocup.append(df_robocup[i]['Erro médio - Laser'][0:11])
    data_menor_media_robocup.append(np.mean(df_robocup[i]['Erro médio - Laser'][0:11]))
    data_maior_robocup.append(df_robocup[i]['Erro médio - Laser'][12:23])
    data_maior_media_robocup.append(np.mean(df_robocup[i]['Erro médio - Laser'][12:23]))
    data_menor_erro_distancia_maximo_robocup.append(df_robocup[i]['Erro máximo - Laser'][0:11])
    data_maior_erro_distancia_maximo_robocup.append(df_robocup[i]['Erro máximo - Laser'][12:23])

print(data_menor_erro_distancia_maximo_media)

# data = [df[3]['Erro médio - Laser'][0:11], df[4]['Erro médio - Laser'][0:11]]

# ARTIGO ROBOCUP

# fig, ax = plt.subplots()

# bp = ax.boxplot(data_menor_robocup, labels = cenarios_artigo_rc_names, patch_artist = True, vert = False)
# # plt.title('RMSE - Ground Tru - Cenário Quadrado Menor')
# plt.xlabel('Mean error [m]')
# plt.tight_layout()
# plt.grid()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_maior_robocup, labels = cenarios_artigo_rc_names, patch_artist = True, vert = False)
# plt.xlabel('Mean error [m]')
# plt.tight_layout()
# plt.grid()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_menor_erro_distancia_maximo_robocup, labels = cenarios_artigo_rc_names, patch_artist = True, vert = False)
# plt.xlabel('Max error [m]')
# plt.tight_layout()
# plt.grid()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_maior_erro_distancia_maximo_robocup, labels = cenarios_artigo_rc_names, patch_artist = True, vert = False)
# plt.xlabel('Max error [m]')
# plt.tight_layout()
# plt.grid()



# DISSERTAÇÃO

fig, ax = plt.subplots()

bp = ax.violinplot(data_menor, showmeans=True, showmedians=True, showextrema=True)

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_menor, labels = cenarios, patch_artist = True, vert = False)
# # plt.title('Erro médio - Laser - Cenário Quadrado Menor')
# plt.xlabel('Erro médio (m)')
# plt.grid()
# plt.tight_layout()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_maior, labels = cenarios, patch_artist = True, vert = False)
# # plt.title('Erro médio - Laser - Cenário Quadrado Maior')
# plt.xlabel('Erro médio (m)')
# plt.grid()
# plt.tight_layout()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_menor_erro_distancia_maximo, labels = cenarios, patch_artist = True, vert = False)
# # plt.title('Erro máximo - Laser - Cenário Quadrado Menor')
# plt.xlabel('Erro máximo (m)')
# plt.grid()
# plt.tight_layout()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_maior_erro_distancia_maximo, labels = cenarios, patch_artist = True, vert = False)
# # plt.title('Erro máximo - Laser - Cenário Quadrado Maior')
# plt.xlabel('Erro máximo (m)')
# plt.grid()
# plt.tight_layout()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_menor_orientacao, labels = cenarios[1:8], patch_artist = True, vert = False)
# # plt.title('Erro de orientação médio - Visão - Cenário Quadrado Menor')
# plt.xlabel('Erro médio (deg)')
# plt.grid()
# plt.tight_layout()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_maior_orientacao, labels = cenarios[1:8], patch_artist = True, vert = False)
# # plt.title('Erro de orientação médio - Visão - Cenário Quadrado Maior')
# plt.xlabel('Erro médio (deg)')
# plt.grid()
# plt.tight_layout()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_menor_orientacao_maximo, labels = cenarios[1:8], patch_artist = True, vert = False)
# # plt.title('Erro de orientação máximo - Visão - Cenário Quadrado Menor')
# plt.xlabel('Erro máximo (deg)')
# plt.grid()
# plt.tight_layout()

# fig, ax = plt.subplots()
# bp = ax.boxplot(data_maior_orientacao_maximo, labels = cenarios[1:8], patch_artist = True, vert = False)
# # plt.title('Erro de orientação máximo - Visão - Cenário Quadrado Maior')
# plt.xlabel('Erro máximo (deg)')
# plt.grid()
# plt.tight_layout()

plt.figure()

width = 0.35
values = np.arange(len(cenarios))

plt.bar(values, data_menor_media, width, label='Menor', color='lightblue')
plt.bar(values+width, data_maior_media, width, label='Maior', color='steelblue')

plt.legend()

plt.xticks(values, cenarios[::-1], rotation=45)
plt.ylabel('Erro médio - Laser (m)')
# plt.title('Erro médio comparado com o Laser')
plt.tight_layout()
# plt.grid()

# plt.figure()

# plt.bar(values, data_menor_erro_distancia_maximo_media, width, label='Menor', color='lightblue')
# plt.bar(values+width, data_maior_erro_distancia_maximo_media, width, label='Maior', color='steelblue')

# plt.legend()

# plt.xticks(values, cenarios, rotation=45)
# plt.ylabel('Erro máximo - Laser (m)')
# plt.title('Média do erro máximo comparado com o Laser')

# plt.figure()

# width = 0.35
# values = np.arange(len(cenarios)-1)

# plt.bar(values, data_menor_orientacao_media, width, label='Menor', color='lightblue')
# plt.bar(values+width, data_maior_orientacao_media, width, label='Maior', color='steelblue')

# plt.xticks(values[0:7], cenarios[0:7], rotation=45)
# plt.ylabel('Erro médio de orientação (deg)')
# plt.title('Erro médio de orientação comparado com o sistema de visão')
# plt.legend()

# plt.figure()

# plt.bar(values, data_menor_orientacao_maximo_media, width, label='Menor', color='lightblue')
# plt.bar(values+width, data_maior_orientacao_maximo_media, width, label='Maior', color='steelblue')

# plt.xticks(values[0:7], cenarios[0:7], rotation=45)
# plt.ylabel('Erro médio de orientação (deg)')
# plt.title('Erro médio de orientação comparado com o sistema de visão')
# plt.legend()

plt.show()

# df = pd.read_excel('C:\\Users\\joaov\\OneDrive\\Documentos\\resultados_mestrado.xlsx', sheet_name='Cenário 1 - final')

# print(df.head())