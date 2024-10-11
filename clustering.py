import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans

# Intentar cargar el CSV con diferentes codificaciones
try:
    df = pd.read_csv('productos_extraccion.csv', encoding='utf-8', sep=',')
except Exception as e:
    print("Error cargando el CSV con 'utf-8':", e)
    df = pd.read_csv('productos_extraccion.csv', encoding='latin1', sep=',')

# Limpiar los nombres de las columnas (eliminar espacios y caracteres extraños)
df.columns = df.columns.str.strip()  # Solo eliminar espacios en los nombres

# Inspeccionar las columnas y los datos
print("Columnas en el DataFrame:", df.columns.tolist())
print(df.head())

# Preprocesar los datos: seleccionar características para el clustering
# Usaremos 'Precio Normal' y convertiremos 'Tallas' y 'Categoría' a formato numérico
features = df[['Precio Normal', 'Tallas', 'Categoría']]

# Codificar las características categóricas
encoder = OneHotEncoder(sparse_output=False)  # Usar sparse_output en lugar de sparse
categorical_features = encoder.fit_transform(features[['Tallas', 'Categoría']])

# Crear un DataFrame a partir de las características codificadas
encoded_df = pd.DataFrame(categorical_features, columns=encoder.get_feature_names_out(['Tallas', 'Categoría']))

# Unir las características codificadas con 'Precio Normal'
final_features = pd.concat([df[['Precio Normal']].reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

# Aplicar el algoritmo KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(final_features)

# Predecir los clusters
df['Cluster'] = kmeans.labels_

# Visualizar los resultados en un gráfico de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(df['Precio Normal'], np.arange(len(df)), c=df['Cluster'], cmap='viridis', alpha=0.5)
plt.title('Clustering de Productos por Precio')
plt.xlabel('Precio')
plt.ylabel('Índice de Producto')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.show()

# Mostrar el DataFrame con los clusters asignados
print(df[['Categoría', 'Tallas', 'Precio Normal', 'Cluster']].head())

