from CBR import CBR
from classes import User, Case, Book
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime


# ------------------ Carreguem dataset i inicialitzem instancies -----------------

cases_db = pd.read_csv("df_casos_new.csv")
users_db = pd.read_csv("df_usuarios_new.csv")
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

instance = None
# --------------------------------- HUD ------------------------------

def no_tengo_numero_usuario():
    # Función a ejecutar cuando se hace clic en el botón "No tengo número de usuario"
    hide_frames()
    entrada_usuario.delete(0, tk.END)
    nuevo.config(text="Como eres nuevo, debes rellenar todos los campos")
    nuevo_user.pack(fill= "both", expand=1)
    Label1 = tk.Label(nuevo_user, text = f"Este es tu número de usuario: {len(cbr.users_inst)}", bg="beige", font=("Courier", 15)).grid(row = 0, column= 0, columnspan=2, pady = 40)

def cambiar_de_pestaña(event):
    # Función a ejecutar al presionar "Enter"
    numero_usuario = int(entrada_usuario.get())
    if numero_usuario >= len(cbr.users_inst):
        error.config(text="El usuario introducido no existe")
    else:
        global instance
        hide_frames()
        entrada_usuario.delete(0, tk.END)
        instance= cbr.users_inst[numero_usuario]
        print(instance.get_user_profile())
        pref.pack(fill= "both", expand=1)
    # Agrega aquí la lógica para cambiar de pestaña o realizar otras acciones

def preguntar_pref():
    # Función a ejecutar al presionar "Enter"
    global instance
    u_prof = {}
    for key,value in user_prof.items():
        if value.get() == "-":
            return
        if key == "edad":
            if value.get() > 25:
                u_prof[key] = 'adulto'
            elif value.get() == 0:
                return
            else: 
                u_prof[key] = 'joven'
        elif key == "horas_lectura_a_la_semana":
            if value.get() > 13:
                u_prof[key] = 'muchas'
            elif value.get() > 5:
                u_prof[key] = 'normal'
            else: 
                u_prof[key] = 'pocas'
        else:
            u_prof[key] = cbr._procesar_input(value.get())
    combos = [Combo, Combo2, Combo5, Combo6, Combo7]
    for i in combos:
        i.current(0)
    hide_frames()
    entrada_edad.delete(0, tk.END)
    entrada_lectura.delete(0, tk.END)
    prof = pd.DataFrame([u_prof])
    instance = User(len(cbr.users_inst)+1, prof.loc[0])
    print(instance.get_user_profile())
    pref.pack(fill= "both", expand=1)
    # Agrega aquí la lógica para cambiar de pestaña o realizar otras acciones

def hide_frames():
    main.pack_forget()
    pref.pack_forget()
    nuevo_user.pack_forget()
    recom.pack_forget()

def recomendar():
    combos = [myCombo,myCombo2,myCombo3,myCombo4,myCombo5,myCombo6,myCombo7,myCombo8,myCombo9]
    user_prefs = {}
    global instance
    for key,value in user_prefs_dic.items():
        if value.get() == "-":
            if instance.get_username() < len(cbr.users_inst):
                user_prefs[key] = None
            else:
                return
        else:
           user_prefs[key] = cbr._procesar_input(value.get())
    for i in combos:
        i.current(0)
    global best_cases
    user_prefs = list(user_prefs.values())
    caso = Case(cbr.number_cases, instance, user_prefs)
    sim_cases = cbr.retrieve(caso, 30) #Fem retrieve dels casos més similars, segon element es quants llibres tornem al retrieve
    best_cases = cbr.reuse(sim_cases, caso) #Fem reuse per adaptar la solució amb els casos similars i els llibres
    hide_frames()
    recom.pack(fill= "both", expand=1)
    revise(best_cases, caso)

def salir():
    for i in range(len(ratings)):
        if ratings[i].get() > 5 or ratings[i].get()==0:
            return
        new_cases[i].rating = int(ratings[i].get())
    hide_frames()
    error.config(text="")
    nuevo.config(text="")
    main.pack(fill= "both", expand=1) 
    cbr.retain(new_cases)
    

def cerrar_ventana():
    cbr.save_databases()
    ventana.destroy()

def revise(best_cases, new_case):
    for widget in recom.winfo_children():
        if widget != boton_salir and widget != titulo and widget != punt:  # Excluir el botón de la destrucción
            widget.destroy()
    date_today = datetime.now()
    day_90 = datetime(2023, 12, 8) # ja canviarem aquesta data
    difference_days = (date_today - day_90).days
    timestamp = 90 + difference_days
    global new_cases
    new_cases = []
    i = 0
    r1,r2,r3 = tk.IntVar(),tk.IntVar(),tk.IntVar()
    global ratings
    ratings = [r1,r2,r3]
    for sim, case, match_attr in best_cases:
        n_case = Case(new_case.get_caseid()+i,new_case.get_user(), new_case.get_user_preferences())
        conf = round(sim*100, 1)
        contenedorl1 = tk.Frame(recom, borderwidth=2, relief="solid", bg= "beige")
        contenedorl1.grid(row = 1, column= i, padx= 20, pady=10)
        myLabel = tk.Label(contenedorl1, text = f"Te recomendamos el libro '{case.get_book().get_title()}' con una confianza del {conf}%", bg="beige", wraplength=200).grid(column= 0, row = 0, padx=10)
        entrada_usuario = tk.Entry(contenedorl1, font=("Arial", 12), textvariable= ratings[i])
        entrada_usuario.grid(column= 0, row = 1, padx=10, pady= 30)
        myLabel2 = tk.Label(contenedorl1, text = cbr._justify_recomendation(match_attr), bg="beige", wraplength=200).grid(column= 0, row = 2, padx=10, pady= 30)
        n_case.book = case.get_book()
        n_case.timestamp = timestamp
        new_cases.append(n_case)
        i+=1


#####################
# Ventana principal #
#####################
    
ventana = tk.Tk()
ventana.title("Bicho3")
ventana.geometry("800x600")  # Tamaño de la ventana
ventana.resizable(False, False)

ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

################
# Ventana main #
################

main = tk.Frame(ventana, bg="beige", width=800, height=600)
main.pack(fill= "both", expand=1)

# Crear el título en la pantalla principal
titulo = tk.Label(main, text="Bienvenido a Bicho3", font=("Courier", 40), bg="beige")
titulo.grid(row= 0, padx= 110, pady=20)

error = tk.Label(main, text="", font=("Courier", 10), bg="beige")
error.grid(row=3, column= 0, pady=10)

# Crear la casilla para introducir el número de usuario en la pantalla principal
etiqueta_usuario = tk.Label(main, text="¿Ya estás registrado? Introduce tu número de usuario", font=("Courier", 14), bg="beige")
etiqueta_usuario.grid(row= 1, pady=70)

entrada_usuario = tk.Entry(main, font=("Courier", 14))
entrada_usuario.grid(row= 2, pady=10)
entrada_usuario.bind("<Return>", cambiar_de_pestaña)  # Enlace de evento para la tecla "Enter"

# Crear el botón "No tengo número de usuario" en la pantalla principal
boton_no_tengo = tk.Button(main, text="No tengo número de usuario", command=no_tengo_numero_usuario, font=("Courier", 12))
boton_no_tengo.grid(row= 4, pady=180)

########################
# Ventana Usuario Nuevo#
########################

nuevo_user = tk.Frame(ventana, width=800, height=600, bg="beige")
titulo = tk.Label(nuevo_user, text="Cuéntanos un poco sobre ti...", font=("Courier", 14), bg="beige")
titulo.grid(row = 1, column= 0, pady=30, padx = 10, sticky="w")

boton_pref = tk.Button(nuevo_user, text="Siguiente", command= preguntar_pref)
boton_pref.grid(row = 10, column = 0, columnspan=2, pady = 20)

#Pregunta 1:
Label1 = tk.Label(nuevo_user, text = "¿Cuál es tu género?", bg="beige",font=("Courier", 10)).grid(row = 2, column = 0, padx=10, pady=10, sticky="w")
options = ["-","Hombre", "Mujer", "Prefiero no decirlo"]
genero = tk.StringVar()
Combo = ttk.Combobox(nuevo_user, values=options, state="readonly", textvariable=genero)
Combo.current(0)
Combo.grid(row = 2, column = 1, padx=10, sticky="e")

#Pregunta 2:
Label2 = tk.Label(nuevo_user, text = "¿Qué edad tienes? ", bg="beige", font=("Courier", 10)).grid(row = 3, column = 0, padx=10, pady=10, sticky="w")

edad = tk.IntVar()
entrada_edad = tk.Entry(nuevo_user, font=("Courier", 10), textvariable=edad)
entrada_edad.grid(row = 3, column = 1, padx=10,sticky="e")

#Pregunta 3:
Label3 = tk.Label(nuevo_user, text = "¿A qué clase social perteneces?", bg="beige",font=("Courier", 10)).grid(row = 4, column = 0, padx=10, pady=10, sticky="w")
options3 = ["-","Alta", "Media", "Baja"]
clase_social = tk.StringVar()
Combo2 = ttk.Combobox(nuevo_user, values=options3, state="readonly",textvariable=clase_social)
Combo2.current(0)
Combo2.grid(row = 4, column = 1, padx=10,sticky="e")

#Pregunta 4:
Label4 = tk.Label(nuevo_user, text = "¿Cuál es tu situación laboral alctual?", bg="beige",font=("Courier", 10)).grid(row = 5, column = 0, padx=10, pady=10, sticky="w")
options4 = ["-","Trabajador", "Estudiante", "Jubilado", "Nada"]
trabajo = tk.StringVar()
Combo2 = ttk.Combobox(nuevo_user, values=options4, state="readonly",textvariable=trabajo)
Combo2.current(0)
Combo2.grid(row = 5, column = 1, padx=10,sticky="e")

#Pregunta 5
Label2 = tk.Label(nuevo_user, text = "¿Cuántas horas le dedicas a la lectura a la semana?                      ", bg="beige", font=("Courier", 10)).grid(row = 6, column = 0, padx=10, pady=10, sticky="w")

horas_lectura = tk.IntVar()
entrada_lectura = tk.Entry(nuevo_user, font=("Courier", 10), textvariable=horas_lectura)
entrada_lectura.grid(row = 6, column = 1, padx=10,sticky="e")

#Pregunta 5:
Label5 = tk.Label(nuevo_user, text = "¿Qué tipo de música escuchas? ", bg="beige",font=("Courier", 10)).grid(row = 7, column = 0, padx=10, pady=10, sticky="w")
options5 = ["-","Reggeatón", "Techno", "Pop", "Clásica", "Rap", "Heavy Metal"]
musica = tk.StringVar()
Combo5 = ttk.Combobox(nuevo_user, values=options5, state="readonly",textvariable=musica)
Combo5.current(0)
Combo5.grid(row = 7, column = 1, padx=10,sticky="e")

#Pregunta 6:
Label6 = tk.Label(nuevo_user, text = "¿Dónde irías una tarde libre? ", bg="beige",font=("Courier", 10)).grid(row = 8, column = 0, padx=10, pady=10, sticky="w")
options6 = ["-","Bar", "Playa", "Montaña", "Sofá"]
tarde = tk.StringVar()
Combo6 = ttk.Combobox(nuevo_user, values=options6, state="readonly",textvariable=tarde)
Combo6.current(0)
Combo6.grid(row = 8, column = 1, padx=10,sticky="e")

#Pregunta 7:
Label7 = tk.Label(nuevo_user, text = "¿A qué tipo de sitio te irías de vacaciones? ", bg="beige",font=("Courier", 10)).grid(row = 9, column = 0, padx=10, pady=10, sticky="w")
options7 = ["-","Aventura", "Moderno", "Clásico"]
vacaciones = tk.StringVar()
Combo7 = ttk.Combobox(nuevo_user, values=options7, state="readonly",textvariable=vacaciones)
Combo7.current(0)
Combo7.grid(row = 9, column = 1, padx=10,sticky="e")


user_prof = {"genero": genero, "edad": edad, "clase_social": clase_social, "trabajo": trabajo, "horas_lectura_a_la_semana": horas_lectura, "musica": musica, "tarde_libre": tarde, "vacaciones": vacaciones}

########################
# Ventana preferencias #
########################

pref = tk.Frame(ventana, width=800, height=600, bg="beige")
titulo = tk.Label(pref, text="Dinos si tienes alguna preferencia especial para hoy", font=("Courier", 12), bg="beige")
titulo.grid(row = 0, column= 0, columnspan=2, pady=20, padx = 50)

nuevo = tk.Label(pref, text="", font=("Courier", 10), bg="beige")
nuevo.grid(row = 1, column= 0, columnspan=2, pady = 20, padx = 50)

boton_recomendar = tk.Button(pref, text="Recomendar", command= recomendar)
boton_recomendar.grid(row = 11, column = 0, columnspan=2, padx=200, pady= 30)

#Pregunta 1:
Label1 = tk.Label(pref, text = "¿En que sección de la libreria invertirías más tiempo mirando libros?", bg="beige",font=("Courier", 10)).grid(row = 2, column = 0, padx=10, pady=10, sticky="w")
options = ["-","Fantasia", "Ficción Histórica", "Terror", "Humor", "Magia", "Misterio", "Romance", "Ciencia Ficción", "Suspense"]
var1 = tk.StringVar()
myCombo = ttk.Combobox(pref, values=options, state="readonly", textvariable=var1)
myCombo.current(0)
myCombo.grid(row = 2, column = 1, padx=10)

#Pregunta 2:
Label2 = tk.Label(pref, text = "¿A qué clasificación de edad te gustaría que perteneciera tu libro?", bg="beige",font=("Courier", 10)).grid(row = 3, column = 0, padx=10, pady=10, sticky="w")
options2 = ["-","Infantil", "Juvenil", "Adulto"]
var2 = tk.StringVar()
myCombo2 = ttk.Combobox(pref, values=options2, state="readonly",textvariable=var2)
myCombo2.current(0)
myCombo2.grid(row = 3, column = 1, padx=10)

#Pregunta 3:
Label3 = tk.Label(pref, text = "¿Desde qué punto de vista quieres que se explique la historia?", bg="beige",font=("Courier", 10)).grid(row = 4, column = 0, padx=10, pady=10, sticky="w")
options3 = ["-","Primera Persona", "Tercera Persona"]
var3 = tk.StringVar()
myCombo3 = ttk.Combobox(pref, values=options3, state="readonly",textvariable=var3)
myCombo3.current(0)
myCombo3.grid(row = 4, column = 1, padx=10)

#Pregunta 4:
Label4 = tk.Label(pref, text = "¿Quieres leer un libro que pertenezca a una saga?", bg="beige",font=("Courier", 10)).grid(row = 5, column = 0, padx=10, pady=10, sticky="w")

options4 = ["-","Si", "No"]
var4 = tk.StringVar()
myCombo4 = ttk.Combobox(pref, values=options4, state="readonly",textvariable=var4)
myCombo4.current(0)
myCombo4.grid(row = 5, column =1, padx=10)

#Pregunta 5:
Label5 = tk.Label(pref, text = "¿Cuál consideras que debe ser la longitud ideal para tu libro?", bg="beige",font=("Courier", 10)).grid(row =6, column = 0, padx=10, pady=10, sticky="w")

options5 = ["-","Corto", "Normal", "Largo"]
var5 = tk.StringVar()
myCombo5 = ttk.Combobox(pref, values=options5, state="readonly",textvariable=var5)
myCombo5.current(0)
myCombo5.grid(row = 6, column = 1, padx=10)

#Pregunta 6:
Label6 = tk.Label(pref, text = "¿En qué formato disfrutas más un libro?", bg="beige",font=("Courier", 10)).grid(row = 7, column = 0, padx=10, pady=10, sticky="w")

options6 = ["-","Audiolibro", "Papel", "Ebook"]
var6 = tk.StringVar()
myCombo6 = ttk.Combobox(pref, values=options6, state="readonly",textvariable=var6)
myCombo6.current(0)
myCombo6.grid(row = 7, column = 1, padx=10)

#Pregunta 7:
Label7 = tk.Label(pref, text = "Teniendo en cuenta tu sitio habitual de lectura, ¿cuál es el peso del libro con el que te sentirías más cómodo/a?", bg="beige",font=("Courier", 10), wraplength=600, justify="left").grid(row = 8, column = 0, padx=10, pady=10)

options7 = ["-","Ligero", "Intermedio", "Pesado"]
var7 = tk.StringVar()
myCombo7 = ttk.Combobox(pref, values=options7, state="readonly",textvariable=var7)
myCombo7.current(0)
myCombo7.grid(row = 8, column = 1, padx=10)

#Pregunta 8:
Label8 = tk.Label(pref, text = "¿En qué idioma buscas leer?", bg="beige",font=("Courier", 10)).grid(row = 9, column = 0, padx=10, pady=10, sticky="w")

options8 = ["-","Castellano", "Inglés", "Catalán"]
var8 = tk.StringVar()
myCombo8 = ttk.Combobox(pref, values=options8, state="readonly",textvariable=var8)
myCombo8.current(0)
myCombo8.grid(row = 9, column = 1, padx=10)

#Pregunta 9:
Label9 = tk.Label(pref, text = "¿Prefieres una obra mundialmente conocida?", bg="beige",font=("Courier", 10)).grid(row =10, column = 0, padx=10, pady=10, sticky="w")

options9 = ["-","Si", "No"]
var9 = tk.StringVar()
myCombo9 = ttk.Combobox(pref, values=options9, state="readonly",textvariable=var9)
myCombo9.current(0)
myCombo9.grid(row = 10, column = 1, padx=10)

user_prefs_dic = {'contiene':var1, 'formato': var6, 'idioma': var8, 'largura_libro': var5,
                   'clasificacion_edad':var2, 'compone_saga':var4, 'famoso':var9, 'peso':var7,
                   'tipo_narrador':var3}

#########################
# Ventana recomendacion #
#########################

recom = tk.Frame(ventana, width=800, height=600, bg="beige")
titulo = tk.Label(recom, text="Te recomendamos los siguientes libros!!!", font=("Courier", 20), bg="beige")
titulo.grid(column = 0, row = 0, columnspan=3, pady=20)
punt = tk.Label(recom, text="Puntúa que te han parecido nuestras recomendaciones del 1 al 5", font=("Courier", 10), bg="beige")
punt.grid(column = 0, row = 2, columnspan=3)          

boton_salir = tk.Button(recom, text="Salir", command= salir)
boton_salir.grid(column= 1, row = 3, pady = 80)




# Iniciar el bucle principal de la aplicación
cbr = CBR(cases_db, users_db, books_db)
ventana.mainloop()

# --------------------------------- Prova sistema complet ------------------------------
# def main():
#     cbr = CBR(cases_db, users_db, books_db) #Iniciem el sistema
#     run = True
#     while run:
#         new_case = cbr.inici_usuari() #Realitzem les preguntes inicials al usuari
#         sim_cases = cbr.retrieve(new_case, 30) #Fem retrieve dels casos més similars, segon element es quants llibres tornem al retrieve
#         best_cases = cbr.reuse(sim_cases, new_case) #Fem reuse per adaptar la solució amb els casos similars i els llibres
#         new_cases = cbr.revise(best_cases, new_case) #Preguntem el feedback a l'usuari
#         cbr.retain(new_cases) #Guardem els casos al sistema i a la base de dades
#         s = input("Si deseas salir escribe 'exit': ").lower()
#         if s=='exit':
#             run = False
#     cbr.save_databases()

# main()




