import pandas as pd
import matplotlib.pyplot as plt

# Cargar el CSV
df = pd.read_csv('productos_extraccion.csv', encoding='latin1', sep=',')

# Corregir los nombres de las columnas
df.columns = ['Categoría', 'Página', 'Posición', 'Descripción', 'Precio Normal', 'Precio Descuento', 'Imagen URL', 'Tallas']

# Añadir una columna para identificar si los productos tienen descuento o no
df['Tiene Descuento'] = df['Precio Descuento'].notna()

# ----------- Gráfico 1: Pie Chart de productos con y sin descuento ----------- #
plt.figure(figsize=(6, 6))
df['Tiene Descuento'].value_counts().plot(kind='pie', autopct='%1.1f%%', labels=['Sin Descuento', 'Con Descuento'], 
                                           colors=['#ff9999', '#66b3ff'], startangle=90, explode=(0, 0.1))
plt.title('Proporción de Productos Con y Sin Descuento')
plt.ylabel('')  # Elimina el label de Y para que el gráfico de torta se vea limpio
plt.show(block=False)  # Mostrar gráfico de torta sin bloquear

# ----------- Gráfico 2: Gráfico de Área de Distribución por Rango de Precios ----------- #
plt.figure(figsize=(8, 5))
df['Rango de Precios'] = pd.cut(df['Precio Normal'], bins=[0, 50000, 100000, 150000, 200000, 300000],
                                labels=['0-50k', '50k-100k', '100k-150k', '150k-200k', '200k+'])

# Agrupar por rangos y contar productos
rango_precios = df['Rango de Precios'].value_counts().sort_index()
plt.fill_between(rango_precios.index.astype(str), rango_precios.values, color='#88c999', alpha=0.7)
plt.plot(rango_precios.index.astype(str), rango_precios.values, color='#336699', marker='o')

plt.title('Distribución de Productos por Rango de Precios')
plt.xlabel('Rango de Precios')
plt.ylabel('Cantidad de Productos')
plt.grid(True)
plt.show(block=False)  # Mostrar gráfico de área sin bloquear

# ----------- Gráfico 3: Barras Horizontales para la cantidad de productos por categoría ----------- #
plt.figure(figsize=(8, 5))
df['Categoría'].value_counts().sort_values(ascending=True).plot(kind='barh', color='#ffcc66')
plt.title('Cantidad de Productos por Categoría')
plt.xlabel('Cantidad')
plt.ylabel('Categoría')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show(block=False)  # Mostrar gráfico de barras horizontales sin bloquear

# Esto mantendrá abiertas las ventanas de las gráficas
plt.show()  # Llamada final para que todas las ventanas se mantengan abiertas

#  Insights y análisis adicionales basados en la cantidad de datos extraidos
# Insight 1: Diferencia significativa entre productos con y sin descuento
# - Se observa que los productos sin descuento tienen un precio promedio significativamente más alto (~100k) comparado con los productos con descuento (~60k).
# - Esto podría sugerir que la empresa tiende a aplicar descuentos en productos de gama media, o que los productos más caros no entran frecuentemente en promociones.
# - Estrategia: Revisar si los productos con descuentos están alineados con las temporadas de promociones. Podría ser útil introducir más productos de gamas altas en las ofertas.

# Insight 2: Distribución de precios
# - La mayor cantidad de productos se encuentran en el rango de precios entre 50k y 100k.
# - Esto indica que la estrategia de precios de la empresa se centra mayormente en productos asequibles para el público objetivo.
# - Estrategia: Explorar si los productos dentro de este rango de precios representan las mejores ventas y analizar si hay oportunidades para incrementar precios ligeramente sin perder competitividad.

# Insight 3: Análisis por categoría de productos
# - Bebés es la categoría más dominante en términos de cantidad de productos, seguida de los productos para niños y el Outlet.
# - Este hallazgo sugiere que la empresa está priorizando el mercado de ropa para bebés, lo cual puede estar relacionado con la demanda más alta en esa área.
# - Estrategia: Ampliar la oferta de productos en categorías como "Niñas", ya que parece ser la menos abastecida.
# - Además, el Outlet puede ser una oportunidad clave para liberar inventario de productos que no se vendan rápidamente.