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
    cbr = CBR(cases_db, users_db, books_db)
    # Empezamos preguntando al usuario su username
    pass

cbr = CBR(cases_db, users_db, books_db)

print(cbr.index_tree)


print('Bienvenido al recomendador de libros Bicho3, ahora somos 4!')

r = input("Te has registrado anteriormente? (Si/No)").lower()
if r == "si":
    num_usuario = float("inf")
    while num_usuario not in range(0,len(users_db)):
        try:
            num_usuario = int(input("Introduzca su número de usuario: "))
        except ValueError:
            print("Usuario no encontrado en la base de datos. Porfavor introduzca su número de usuario: ")
    a = input("Quieres contarnos cuales son tus preferencias? o prefieres que las infiramos en función de tu historial? Opciones: 1,2")
    if a == "1":
        print('Ahora queremos saber qué caracterísitcas quieres que contenga el libro que estás buscando:')
        prefs =  cbr.ask_user_prefs()
    else:
        prefs = None
    new_case = Case(cbr.number_cases,cbr.users_inst[num_usuario],prefs)
            
else:
    num_usuario = len(users_db)+1
    print(f'Sú número de usuario és el siguiente: {num_usuario}')
    print('Para recomendarte el mejor libro, primero debemos saber un poco más de tí.')
    new_case = cbr.ask_questions(num_usuario)
    print('Ahora queremos saber qué caracterísitcas quieres que contenga el libro que estás buscando:')
    prefs =  cbr.ask_user_prefs()
    print(new_case.atributes_pref)
    new_case.set_atributes(prefs)
    print(new_case.atributes_pref)
         
#new_case = Case(101,cbr.users_inst[33],['fantasia', 'papel', 'castellano', 'normal', 'juvenil', 'si', 'si', 'intermedio', 'primera_persona'])
sim_cases = cbr.retrieve(new_case)

print(sim_cases)

best_cases = cbr.reuse(sim_cases, new_case)

for i in range(3):
    print(best_cases[i][1].get_book().get_book_features())
    print(best_cases[i][1].get_user().get_username())

print(new_case.get_user_preferences())
new_cases = cbr.revise(best_cases, new_case)

for i in new_cases:
    print(i.get_book().get_title(),i.get_rating(), i.get_timestamp())

print(cbr.number_cases)
cbr.retain(new_cases)

print(cbr.number_cases)
print(cbr.cases)
print(cbr.index_tree)




