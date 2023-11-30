from CBR import CBR
from classes import User, Case, Book
import pandas as pd

# Definir cases_db amb ids
# Exemple (tindrà aquesta forma) emplenar a partir de csv drive:
cases_db = {
    'Case_id': [1,2,3,4,5,6,7,8],
    'User_id': [1,1,2,2,3,2,3,4], # Poden repetir-se
    'Book_id': [0,0,0,0,0,0,0,0], # Poden repetir-se
    'User_preferences': [0,0,0,0,0,0,0,0],
    #'Comprado': [] ?
    'Rating': [0,0,0,0,0,0,0,0], # Valoracions de l'1 al 5 (de moment)
    #'Timestep': []
}
# Això s'haurà d'emplenar a partir del csv drive, en el cas de users també al ask():
# Definir users_db (propies instancies usuaris)
users_db = {
    'User_id': [1,2,3,4],
    'Genero' : ['Hombre', 'Mujer', 'Hombre', 'Mujer'],
    'Edad': ['Adulto','Adulto','Adulto','Adulto'],
    'Hobbies': ['Playa', 'Montaña', 'Playa', 'Playa']
}
cases_db = pd.DataFrame(cases_db)
users_db = pd.DataFrame(users_db)

# ------------------ Carreguem dataset i inicialitzem instancies -----------------

cases_db = pd.read_csv("Casos.csv")
users_db = pd.read_csv("Usuarios.csv")
books_db = pd.read_csv("my_data_books_1.csv")

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


cbr = CBR(books_db, cases_db, users_db)

'''
if __name__ == '__main__':

    ask_questions()
'''
# Creem instancies, ho posem en llistes tot per provar
# Convertim bases de dades en llistes d'instancies
lista_instancias_usuarios = []

for row in range(len(users_db)):
    row_elements = users_db.loc[row]
    instance = User(row_elements[0], row_elements[1:])
    lista_instancias_usuarios.append(instance)

lista_instancias_libros = []
for row in range(len(books_db)):
    row_elements = books_db.loc[row]
    instance = Book(row_elements[0], row_elements[1] ,row_elements[2:])
    lista_instancias_libros.append(instance)

lista_instancias_casos = []
for row in range(len(cases_db)):
    row_elements = cases_db.loc[row]
    instance = Case(row_elements[0], lista_instancias_usuarios[row_elements[1]-1] 
                    ,row_elements[2:6], lista_instancias_libros[row_elements[6]])
    lista_instancias_casos.append(instance)

# --------------------------------- Fem proves ------------------------------
case1 = lista_instancias_casos[15]
case2 = lista_instancias_casos[43]

sim_users = cbr._custom_similarity_users(case1, case2)
print('User 1:','\n', case1.get_user().get_user_profile())
print('User 2:','\n',case2.get_user().get_user_profile())
print('Similaritat Users',sim_users)

case3 = lista_instancias_casos[0]
case4 = lista_instancias_casos[20]
case5 = lista_instancias_casos[25]
case6 = lista_instancias_casos[18]


lis_most_similar_cases = [case1, case2, case3, case4, case5, case6]
actual_case = lista_instancias_casos[33]
three_most_similar_cases_by_books = cbr.reuse(lis_most_similar_cases, actual_case)
print(three_most_similar_cases_by_books)

#print(cbr.index_tree.tree.hijos['Hombre'].valores)

#cbr.index_tree.insertar_caso(9,{'Genero': 'Mujer','Edad': 'Adulto','Hobbies': 'Playa'})

#print(cbr.index_tree.tree.hijos['Hombre'].valores)
#print(cbr.index_tree.tree.hijos['Mujer'].hijos['Playa'].valores)

#print(cbr.index_tree.buscar_casos({'Genero': 'Hombre','Edad': 'Adulto','Hobbies': 'Montaña'}))

#print(cbr.index_tree)

#sim_custom = cbr._custom_similarity(user_db.iat[0,1], user_db.iat[3,1])
#sim_jaccard = cbr._jaccard_similarity(user_db.iat[0,1], user_db.iat[3,1])

#print(sim_custom)
#print(sim_jaccard)