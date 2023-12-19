from CBR import CBR
from classes import User, Case, Book
import pandas as pd


# ------------------ Carreguem dataset i inicialitzem instancies -----------------
cases_db = pd.read_csv("df_casos.csv")
users_db = pd.read_csv("df_usuarios.csv")
books_db = pd.read_csv("my_data_books_new.csv")

books_db = books_db.drop(['tema', 'valoracion'], axis='columns')

# Funció per tractar atributs multislots
def convert_string_to_list(string): 
    string = string[2:-2]
    values = string.split("', '")
    return values

# Apply the conversion function to relevant columns
columns_to_convert = ['contiene', 'formato', 'idioma']
for column in columns_to_convert:
    books_db[column] = books_db[column].apply(convert_string_to_list)

# # --------------------------------- Prova sistema complet ------------------------------
def avaluacio():
    cbr = CBR(cases_db, users_db, books_db) #Iniciem el sistema
    #run = True
    mean_confidence_values = []
    for num_cases_retrieve in [10,20,30]:
        confidence_values = []
        for num_usuario in range(len(cbr.users)):
            new_case = Case(cbr.number_cases,cbr.users_inst[num_usuario],None) #Realitzem les preguntes inicials al usuari
            sim_cases = cbr.retrieve(new_case,num_cases_retrieve) #Fem retrieve dels casos més similars
            best_cases = cbr.reuse(sim_cases, new_case) #Fem reuse per adaptar la solució amb els casos similars i els llibres
            for conf_val, _, _ in best_cases:
                confidence_values.append(conf_val)
        avarage_conf_val = sum(confidence_values)/len(confidence_values)
        mean_confidence_values.append(avarage_conf_val)
    print(mean_confidence_values)
    return mean_confidence_values

mean_confidence_values = avaluacio()


import matplotlib.pyplot as plt

# Datos
etiquetas = [10, 20, 30]
valores = mean_confidence_values

# Ancho de las barras (puedes ajustar este valor según tus preferencias)
ancho_barras = 8

# Crear gráfico de barras con barras más anchas
plt.bar(etiquetas, valores, width=ancho_barras)

# Establecer etiquetas personalizadas en el eje x
plt.xticks(etiquetas)

# Añadir etiquetas y título
plt.xlabel('Límite Retrieve')
plt.ylabel('Confidence Value Medio')
plt.title('Análisis de Calidad')

for etiqueta, valor in zip(etiquetas, valores):
    plt.text(etiqueta, valor, f'{valor:.2f}', ha='center', va='bottom')

# Mostrar el gráfico
plt.show()

# Avaluem satisfacció

media1 = 4.54

media2 = 4.38

media3 = 3.61

etiquetas = ['media 1', 'media 2', 'media 3']
valores = [media1, media2, media3]
# Ancho de las barras (puedes ajustar este valor según tus preferencias)
ancho_barras = 8

# Crear gráfico de barras con barras más anchas
plt.bar(etiquetas, valores, width=ancho_barras)

# Establecer etiquetas personalizadas en el eje x
plt.xticks(etiquetas)

# Añadir etiquetas y título
plt.xlabel('Límite Retrieve')
plt.ylabel('Confidence Value Medio')
plt.title('Análisis de Calidad')

for etiqueta, valor in zip(etiquetas, valores):
    plt.text(etiqueta, valor, f'{valor:.2f}', ha='center', va='bottom')

# Mostrar el gráfico
plt.show()