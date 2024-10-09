import pandas as pd
import matplotlib.pyplot as plt

# Cargar el CSV
df = pd.read_csv('productos_1.csv', encoding='latin1', sep=';')

# Gráfica 1: Comparación de precios entre productos con descuento y sin descuento
df['Tiene Descuento'] = df['precio_descuento'].notna()

# Configurar subplots para las gráficas
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# Gráfica 1: Promedio de precios con y sin descuento
df.groupby('Tiene Descuento')['precio_normal'].mean().plot(kind='bar', ax=axs[0], color=['blue', 'orange'])
axs[0].set_title('Promedio de Precios: Con y Sin Descuento')
axs[0].set_ylabel('Precio Promedio')
axs[0].set_xticklabels(['Sin Descuento', 'Con Descuento'], rotation=0)

# Gráfica 2: Distribución por rango de precios
df['Rango de Precios'] = pd.cut(df['precio_normal'], bins=[0, 50000, 100000, 150000, 200000, 300000],
                                      labels=['0-50k', '50k-100k', '100k-150k', '150k-200k', '200k+'])
df['Rango de Precios'].value_counts().sort_index().plot(kind='bar', ax=axs[1], color='green')
axs[1].set_title('Distribución por Rango de Precios')
axs[1].set_ylabel('Cantidad de Productos')

# Gráfica 3: Cantidad de productos por categoría
df['categoria'].value_counts().plot(kind='bar', ax=axs[2], color='purple')
axs[2].set_title('Cantidad de Productos por Categoría')
axs[2].set_ylabel('Cantidad')

# Mostrar las gráficas
plt.tight_layout()
plt.show()

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