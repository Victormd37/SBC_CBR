import pandas as pd
import numpy as np
import random


usuarios = pd.read_csv('C:/Users/dancv/Desktop/cuatri5/SBC/Usuarios.csv')
libros = pd.read_csv('C:/Users/dancv/Desktop/cuatri5/SBC/my_data_books_new.csv')
#autores = pd.read_csv('my_data_autors_new.csv')

def obtener_categorias(dataset, categoria = str):
    lista = []
    for i in dataset[categoria]:
        lista_categoria = eval(i)
        for c in lista_categoria:
            if c not in lista:
                lista.append(c) 
    return lista

def seleccionar_atributos_casos(atributos_casos,dataset):
    lista_final = []
    for atr in atributos_casos[1:]:
        if dataset[atr][0].startswith('['):
            lista_atributos = obtener_categorias(libros, atr)
        else:
            lista_atributos= list(np.unique(dataset[atr]))
        lista_final.append(lista_atributos)
    return lista_final

def genero(num_usuario,instancias_usuarios,lista_atributos_casos):
    opciones = lista_atributos_casos
    # comprobamos primero su género
    if instancias_usuarios[num_usuario][0] == 'Mujer':
        # comprobamos la edad
        if instancias_usuarios[num_usuario][1] == 'Joven':
            pesos = [0.15,0.1,0.25,0.05,0.05,0.1,0.1,0.05,0.15]
            g = random.choices(opciones, weights=pesos, k=1)[0]  
        else:
            pesos = [0.1,0.05,0.15,0.05,0.1,0.25,0.15,0.05,0.1]  
            g = random.choices(opciones, weights=pesos, k=1)[0]
    elif instancias_usuarios[num_usuario] == 'Hombre':
        if instancias_usuarios[num_usuario][1] == 'Joven':
            pesos = [0.05,0.05,0.05,0.15,0.1,0.1,0.1,0.15,0.25]  
            g = random.choices(opciones, weights=pesos, k=1)[0]
        else:
            pesos =  [0.1,0.05,0.05,0.05,0.1,0.1,0.15,0.25,0.15]
            
            g = random.choices(opciones, weights=pesos, k=1)[0]
    else:
        pesos = [1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9]  
        g = random.choices(opciones, weights=pesos, k=1)[0]
    return g

def formato(num_usuario,instancias_usuarios,lista_atributos_casos):
    opciones = lista_atributos_casos
    # comprobamos la clase social
    if instancias_usuarios[num_usuario][2] == 'Alta':
        pesos =  [0.45,0.45,0.1]
        f = random.choices(opciones, weights=pesos, k=1)[0]  
    elif instancias_usuarios[num_usuario][2] == 'Normal':
        pesos =  [0.65,0.25,0.1]
        f = random.choices(opciones, weights=pesos, k=1)[0]  
    else:
        pesos =  [0.9,0.07,0.03]
        f = random.choices(opciones, weights=pesos, k=1)[0]
    return f

def idioma(num_usuario, instancias_usuarios, lista_atributos_casos):
    opciones = lista_atributos_casos
    # comprobamos clase social
    if instancias_usuarios[num_usuario][4] == 'Muchas':
        pesos =  [0.15,0.5,0.35]
        i = random.choices(opciones, weights=pesos, k=1)[0]  
    elif instancias_usuarios[num_usuario][2] == 'Normal':
        pesos =  [0.1,0.2,0.7]
        i = random.choices(opciones, weights=pesos, k=1)[0]  
    else:
        pesos =  [0.1,0.05,0.85]
        i = random.choices(opciones, weights=pesos, k=1)[0]
    return i

def largura_libro(num_usuario, instancias_usuarios, lista_atributos_casos):
    opciones = lista_atributos_casos
    # comprobamos clase social
    if instancias_usuarios[num_usuario][2] == 'Alta':
        pesos =  [0.2,0.4,0.4]
        l = random.choices(opciones, weights=pesos, k=1)[0]  
    elif instancias_usuarios[num_usuario][2] == 'Normal':
        pesos =  [0.3,0.2,0.5]
        l = random.choices(opciones, weights=pesos, k=1)[0]  
    else:
        pesos =  [0.4,0.2,0.4]
        l = random.choices(opciones, weights=pesos, k=1)[0]
    return l

def clasificacion_edad(num_usuario, instancias_usuarios, lista_atributos_casos):
    opciones = lista_atributos_casos
    # comprobamos edad
    if instancias_usuarios[num_usuario][1] == 'Joven':
        pesos =  [0.1,0.35,0.55]
        ce = random.choices(opciones, weights=pesos, k=1)[0]  
    else:
        pesos =  [0.55,0.1,0.35]
        ce = random.choices(opciones, weights=pesos, k=1)[0]
    return ce

def peso(num_usuario, instancias_usuarios, lista_atributos_casos):
    opciones = lista_atributos_casos
    if instancias_usuarios[num_usuario][1] == 'Sofa':
        pesos =  [1/3,1/3,1/3]
        p = random.choices(opciones, weights=pesos, k=1)[0]  
    else:
        pesos =  [0.3,0.5,0.2]
        p = random.choices(opciones, weights=pesos, k=1)[0]
    return p

def generar_casos(atributos_casos,num_usuarios,instancias_usuarios,lista_atributos_casos):
    df = pd.DataFrame(columns=atributos_casos)
    # creamos diccionario para ir guardando las cositas
    datos_usuario = {}
    for atr in atributos_casos:
        datos_usuario[atr] = None
    # generamos los atributos
    for n in range(num_usuarios):
        casos_usuario = random.randint(1,50)
        for c in range(casos_usuario):
            lista_aux = []
            #obtenemos género, formato, idioma, largura_libro,clasifiacion_edad, compone_saga, famoso, peso, tipo de narrador
            lista_aux.extend([n, genero(n,instancias_usuarios,lista_atributos_casos[0]),formato(n,instancias_usuarios,lista_atributos_casos[1]), idioma(n,instancias_usuarios,lista_atributos_casos[2]),largura_libro(n,instancias_usuarios,lista_atributos_casos[3]),clasificacion_edad(n,instancias_usuarios,lista_atributos_casos[4]),random.choices(lista_atributos_casos[5])[0],random.choices(lista_atributos_casos[6])[0],peso(n,instancias_usuarios,lista_atributos_casos[7]),random.choices(lista_atributos_casos[8])[0]])  
            for i in range(len(lista_aux)):
                datos_usuario[atributos_casos[i]] = lista_aux[i]
            df = pd.concat([df, pd.DataFrame([datos_usuario])], ignore_index=True)
            
    return df

def asignar_libro(libros,df,num_caso):
    libro = False
    lista_libros = [l for l in libros['titulo']]
    while not libro:
        for col in df.columns[1:]:
            nueva_lista_libros = []
            # miramos cada libro
            for libro in range(len(lista_libros)):
                # añadimos contador por si ya no se cumple una restricción, dejar de iterar
                if libros[col][libro].startswith('['):
                    if df[col][num_caso] in eval(libros[col][libro]):
                        nueva_lista_libros.append(lista_libros[libro])
                else:
                    if df[col][num_caso] in libros[col][libro]:
                        nueva_lista_libros.append(lista_libros[libro])      
            if len(lista_libros) - len(nueva_lista_libros) == len(lista_libros): # no nos hemos quedado con ningún libro
                libro = random.choices(lista_libros)[0]
            elif col == 'tipo_narrador': #llegamos a la última
                libro = random.choices(nueva_lista_libros)[0]
            else:
                lista_libros = nueva_lista_libros  
 
    libro_id = libros.loc[libros['titulo'] == libro, 'Unnamed: 0'].values[0] #devolvemos el índice
    return libro_id


def asignar_valoración(libros,df,num_caso):
    valoracion_libro = libros.loc[libros['Unnamed: 0'] == df['libro'][num_caso], 'valoracion'].values[0]
    valoracion_simulada = int(np.random.normal(loc=valoracion_libro, scale=0.5))  # Ajusta la desviación estándar según sea necesario
    valoracion_simulada = max(1, min(valoracion_simulada, 5))
    return valoracion_simulada

atributos_casos = ['Usuario','contiene', 'formato', 'idioma', 'tema', 'largura_libro', 'clasificacion_edad','compone_saga','famoso', 'peso', 'tipo_narrador']

lista_atributos_casos =  seleccionar_atributos_casos(atributos_casos, libros)   
#el tema lo quitamos de momento
lista_atributos_casos.remove(lista_atributos_casos[3])
atributos_casos.remove('tema')

atributos_usuarios = ['Genero', 'Edad', 'Clase social', 'Trabajo', 'Horas de lectura a la semana', 'Musica', 'Tarde libre', 'Vacaciones']

instancias_usuarios = dict()
for u in range(len(usuarios)):
    lista_atributos = []
    for atr in atributos_usuarios:
        lista_atributos.append(usuarios[atr][u])
    instancias_usuarios[u] = lista_atributos
    
df = generar_casos(atributos_casos,len(usuarios),instancias_usuarios,lista_atributos_casos)

lista_libros = []
for caso in range(len(df)):
    lista_libros.append(asignar_libro(libros,df,caso))
df['libro'] = lista_libros

lista_valoraciones= []
for caso in range(len(df)):
    lista_valoraciones.append(asignar_valoración(libros,df,caso))
df['valoración'] = lista_valoraciones


#df.to_csv("C:/Users/dancv/Desktop/cuatri5/SBC/df_casos.csv", index=False)



