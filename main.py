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
def main():
    cbr = CBR(cases_db, users_db, books_db) #Iniciem el sistema
    run = True
    while run:
        new_case = cbr.inici_usuari() #Realitzem les preguntes inicials al usuari
        sim_cases = cbr.retrieve(new_case) #Fem retrieve dels casos més similars
        best_cases = cbr.reuse(sim_cases, new_case) #Fem reuse per adaptar la solució amb els casos similars i els llibres
        new_cases = cbr.revise(best_cases, new_case) #Preguntem el feedback a l'usuari
        cbr.retain(new_cases) #Guardem els casos al sistema i a la base de dades
        s = input("Si deseas salir escribe 'exit': ").lower()
        if s=='exit':
            run = False
    cbr.save_databases()

main()




