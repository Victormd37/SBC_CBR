from CBR import CBR
from classes import User, Case, Book
import pandas as pd
import time
import matplotlib.pyplot as plt

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
def main_sense_modificar():
    cbr = CBR(cases_db, users_db, books_db) #Iniciem el sistema
    i = len(cases_db)
    print(cbr.index_tree)
    incremento = [i, 5000, 10000, 15000, 20000, 25000]
    tiempos = []
    for k in range(len(incremento)):
        for j in range(i, incremento[k]):
            row_elements = casos_extra.loc[j]
            if row_elements[0] >= len(cbr.users_inst):
                elems = users_extra.loc[row_elements[0]]
                new_user = User(elems[0], elems[1:])
                cbr.users_inst.append(new_user)
            instance = Case(j, cbr.users_inst[row_elements[0]] 
                                        ,row_elements[1:10].tolist(), cbr.books_inst[int(row_elements[10])], rating=row_elements[11], timestamp=row_elements[12])
            cbr.index_tree.insertar_caso(instance, instance.get_user().get_user_profile())
            cbr.number_cases += 1
        new_case = cbr.inici_usuari()
        start = time.time()
        sim_cases = cbr.retrieve(new_case, 30) #Fem retrieve dels casos més similars, segon element es quants llibres tornem al retrieve
        best_cases = cbr.reuse(sim_cases, new_case) #Fem reuse per adaptar la solució amb els casos similars i els llibres
        end = time.time()
        tiempos.append(end-start)
        i = incremento[k]
    
    plt.plot(incremento, tiempos, marker='o', linestyle='-')

    # Etiquetas y título
    plt.ylabel('Tiempo')
    plt.xlabel('Número de Casos')
    plt.show()

def main_modificar_arbre():
    i = len(cases_db)
    incremento = [i, 5000, 10000, 15000, 20000, 25000]
    tiempos = []
    for k in range(len(incremento)):
        usuarios = users_extra[:int(casos_extra.loc[incremento[k]]["usuario"])]
        cbr = CBR(casos_extra[:incremento[k]], usuarios, books_db)
        print(cbr.index_tree)
        new_case = cbr.inici_usuari()
        start = time.time()
        sim_cases = cbr.retrieve(new_case, 30) #Fem retrieve dels casos més similars, segon element es quants llibres tornem al retrieve
        best_cases = cbr.reuse(sim_cases, new_case) #Fem reuse per adaptar la solució amb els casos similars i els llibres
        end = time.time()
        tiempos.append(end-start)
    
    plt.plot(incremento, tiempos, marker='o', linestyle='-')

    # Etiquetas y título
    plt.ylabel('Tiempo')
    plt.xlabel('Número de Casos')
    plt.show()

main_sense_modificar()