from CBR import CBR
from classes import User, Case, Book
import pandas as pd
import random

random.seed(33)

# ------------------ Carreguem dataset i inicialitzem instancies -----------------
cases_db = pd.read_csv("df_casos.csv")
casos_extra = pd.read_csv("df_casos_extra.csv")
users_db = pd.read_csv("df_usuarios.csv")
users_extra = pd.read_csv("df_usuarios_extra.csv")
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
    mean_confidence_values = []
    confidence_values = []
    i = len(cases_db)
    incremento = [i, 5000, 10000, 15000, 20000, 25000]
    for k in range(len(incremento)):
        usuarios = users_extra[:int(casos_extra.loc[incremento[k]]["usuario"])]
        cbr = CBR(casos_extra[:incremento[k]], usuarios, books_db)
        for j in range(100):
            r = random.randint(0, len(cbr.users_inst)-1)
            new_case = Case(cbr.number_cases,cbr.users_inst[r],None) #Realitzem les preguntes inicials al usuari
            sim_cases = cbr.retrieve(new_case,30) #Fem retrieve dels casos més similars
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
etiquetas = [f"{len(cases_db)}", "5000", "10000", "15000", "20000", "25000"]
valores = mean_confidence_values

# Ancho de las barras (puedes ajustar este valor según tus preferencias)

# Crear gráfico de barras con barras más anchas
plt.bar(etiquetas, valores)

# Establecer etiquetas personalizadas en el eje x
plt.xticks(etiquetas)

# Añadir etiquetas y título
plt.xlabel('Número de Casos')
plt.ylabel('Confidence Value Medio')
plt.title('Degradación de la calidad')

plt.ylim(0.5, 1)

for etiqueta, valor in zip(etiquetas, valores):
    plt.text(etiqueta, valor, f'{valor:.2f}', ha='center', va='bottom')

# Mostrar el gráfico
plt.show()