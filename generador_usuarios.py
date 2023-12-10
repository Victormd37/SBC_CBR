import pandas as pd
import random

genero = ['hombre', 'mujer', 'prefiero_no_decirlo']
edad = ['joven', 'adulto']
clase_social = ['baja', 'media', 'alta']
trabajo = ['nada', 'estudiante', 'trabajador', 'jubilado']
horas_lectura = ['pocas', 'normal', 'muchas']
musica = ['pop', 'techno', 'reggeatón','clasica','rap','heavy_metal']
tarde_libre = ['bar', 'playa', 'montaña', 'sofa']
vacaciones = ['moderno', 'clasico', 'aventura']

atributos = ['usuario', 'genero','edad', 'clase_social', 'trabajo', 'horas_lectura_a_la_semana', 'musica', 'tarde_libre', 'vacaciones']

def genero_usuario(genero):
    pesos =  [0.45,0.45,0.1]
    g = random.choices(genero, weights=pesos, k=1)[0]  
    return g

def trabajo_usuario(trabajo, e):
    if e == 'joven':
        pesos =  [0.1,0.7,0.2,0]
        tr = random.choices(trabajo, weights=pesos, k=1)[0] 
    else:
        pesos =  [0.1,0.05,0.65,0.2]
        tr = random.choices(trabajo, weights=pesos, k=1)[0] 
    return tr


def horas_lectura_usuario(horas_lectura,g,e,tr):
    if g == 'hombre':
        if e == 'joven':
            if tr == 'nada':
                pesos =  [0.2,0.3,0.5]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'estudiante':
                pesos =  [0.2,0.5,0.3]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            else:
                pesos =  [0.3,0.5,0.2]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
        else: 
            if tr == 'nada':
                pesos =  [0.1,0.4,0.5]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'estudiante':
                pesos =  [0.1,0.5,0.4]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'trabajador':
                pesos =  [0.2,0.6,0.2]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            else:
                pesos =  [0.1,0.3,0.6]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
    elif g == 'mujer':
        if e == 'joven':
            if tr == 'nada':
                pesos =  [0.1,0.3,0.6]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'estudiante':
                pesos =  [0.1,0.6,0.3]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            else:
                pesos =  [0.25,0.6,0.15]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
        else: 
            if tr == 'nada':
                pesos =  [0.05,0.25,0.7]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'estudiante':
                pesos =  [0.1,0.6,0.3]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'trabajador':
                pesos =  [0.15,0.7,0.15]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            else:
                pesos =  [0.1,0.3,0.6]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
    else:
        if e == 'joven':
            if tr == 'nada':
                pesos =  [0.1,0.3,0.6]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'estudiante':
                pesos =  [0.1,0.6,0.3]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            else:
                pesos =  [0.25,0.6,0.15]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
        else: 
            if tr == 'nada':
                pesos =  [0.05,0.25,0.7]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'estudiante':
                pesos =  [0.1,0.6,0.3]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            elif tr == 'trabajador':
                pesos =  [0.15,0.7,0.15]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0] 
            else:
                pesos =  [0.1,0.3,0.6]
                h_l = random.choices(horas_lectura, weights=pesos, k=1)[0]    
    return h_l 


def musica_usuario(musica, g,e):
    if g == 'hombre':
        if e == 'joven':
            pesos =  [0.1,0.2,0.3,0.05,0.25,0.1]
            m = random.choices(musica, weights=pesos, k=1)[0] 
        else:
            pesos =  [0.2,0.1,0.1,0.25,0.1,0.25]
            m = random.choices(musica, weights=pesos, k=1)[0] 
    elif g == 'mujer':
        if e == 'joven':
            pesos =  [0.4,0.15,0.3,0.05,0.05,0.05]
            m = random.choices(musica, weights=pesos, k=1)[0] 
        else:
            pesos =  [0.35,0.15,0.5,0.35,0.05,0.05]
            m = random.choices(musica, weights=pesos, k=1)[0] 
    else:
        if e == 'joven':
            pesos =  [0.2,0.25,0.25,0.05,0.15,0.1]
            m = random.choices(musica, weights=pesos, k=1)[0] 
        else:
            pesos = [0.2,0.25,0.25,0.05,0.15,0.1]
            m = random.choices(musica, weights=pesos, k=1)[0] 

    return m


df = pd.DataFrame(columns=atributos)

datos_usuario = {}
for atr in atributos:
    datos_usuario[atr] = None
for n in range(100):
    lista = []
    g = genero_usuario(genero)
    e = random.choices(edad)[0]
    c_s = random.choices(clase_social)[0]  
    tr = trabajo_usuario(trabajo,e)
    h_l = horas_lectura_usuario(horas_lectura,g,e,tr)
    m = musica_usuario(musica,g,e)
    t_l = random.choices(tarde_libre)[0] 
    v = random.choices(vacaciones)[0] 
    lista.extend([n,g,e,c_s,tr,h_l,m,v ])

    for i in range(len(lista)):
        datos_usuario[atributos[i]] = lista[i]
    df = pd.concat([df, pd.DataFrame([datos_usuario])], ignore_index=True)

df.to_csv("C:/Users/dancv/Desktop/cuatri5/SBC/Práctica2/SBC_CBR/df_usuarios.csv", index=False)
