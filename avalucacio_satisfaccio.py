

import matplotlib.pyplot as plt

# Avaluem satisfacció

media1 = 4.54

media2 = 4.38

media3 = 3.61

etiquetas = ['Primera', 'Segunda', 'Tercera']
valores = [media1, media2, media3]
# Ancho de las barras (puedes ajustar este valor según tus preferencias)
ancho_barras = 0.5

# Crear gráfico de barras con barras más anchas
plt.bar(etiquetas, valores, width=ancho_barras)

# Establecer etiquetas personalizadas en el eje x
plt.xticks(etiquetas)

# Añadir etiquetas y título
plt.xlabel('Medias recomendaciones')
plt.ylabel('Satisfacción media (1-5)')
plt.title('Análisis de Satisfacción de Usuarios')

for etiqueta, valor in zip(etiquetas, valores):
    plt.text(etiqueta, valor, f'{valor:.2f}', ha='center', va='bottom')

# Mostrar el gráfico
plt.show()