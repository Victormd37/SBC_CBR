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


cbr = CBR(cases_db, users_db, books_db)


'''
print(cbr.index_tree)

user = users_db.loc[4]
print(user)
case = cases_db.loc[24]
caso = Case(51, User(user[0], user[1:]), case[2:6])

s = cbr.retrieve(caso)
s1 =[instancia.get_caseid() for instancia in s]
print(s)
print(s1)
'''
# # Creem instancies, ho posem en llistes tot per provar
# # Convertim bases de dades en llistes d'instancies
print(len(cbr.books_inst))
lista_instancias_casos = []
for row in range(len(cases_db)):
    row_elements = cases_db.loc[row]
    instance = Case(row, cbr.users_inst[row_elements[0]] 
                    ,row_elements[1:10], cbr.books_inst[row_elements[10]], rating = row_elements[11],timestamp= row)
    lista_instancias_casos.append(instance)

print(len(lista_instancias_casos))

# # --------------------------------- Fem proves ------------------------------


'''
case1 = lista_instancias_casos[15]
case2 = lista_instancias_casos[43]
case3 = lista_instancias_casos[0]
case4 = lista_instancias_casos[20]
case5 = lista_instancias_casos[25]
case6 = lista_instancias_casos[18]


list_most_similar_cases = [case1, case2, case3, case4, case5, case6]
actual_case = lista_instancias_casos[33]
three_most_similar_cases_by_books = cbr.reuse(list_most_similar_cases, actual_case)
print(three_most_similar_cases_by_books)
'''

# #print(cbr.index_tree.tree.hijos['Hombre'].valores)

# #cbr.index_tree.insertar_caso(9,{'Genero': 'Mujer','Edad': 'Adulto','Hobbies': 'Playa'})

# #print(cbr.index_tree.tree.hijos['Hombre'].valores)
# #print(cbr.index_tree.tree.hijos['Mujer'].hijos['Playa'].valores)

# #print(cbr.index_tree.buscar_casos({'Genero': 'Hombre','Edad': 'Adulto','Hobbies': 'Montaña'}))

# #print(cbr.index_tree)