import pandas as pd
from convertir_tipos import convertir_tipos
from preprocesamiento import *
from analisis_univariado import analisis_univariado
from feature_selection import feature_selection
from dummy_creation import dummy_creation
#import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, f1_score, confusion_matrix, recall_score
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, confusion_matrix
from pathlib import Path
from sklearn.metrics import precision_score
import joblib




def calcular_calificacion(row):
    
    categoria = str(row['Categoria'])  
    peso_kilos_netos = row['Peso_kilos_netos']
    var_fob_dolar = row['Valor_FOB_USD']

    # Diccionario con los rangos y sus correspondientes calificaciones para cada categoría
    rangos_calificaciones = {
        'Chocolates': {
            'peso': {
                (0, 890): 0,
    
                (891 , float('inf')): 1
            },
            'fob': {
                (0, 2499): 0,
                
                (2500 , float('inf')): 1
            }
        },
        'Cacao en polvo': {
             'fob': {
                (0, 6344): 0,
                
                (6345 , float('inf')): 1
            },
            'peso': {
                (0, 2821): 0,
               
                (2822 , float('inf')): 1
            }
        },
        'Cacao crudo': {
             'peso': {
                (0, 24999): 0,
               
                (25000 , float('inf')): 1
            },
            'fob': {
                (0, 66999): 0,
                
                (67000 , float('inf')): 1
            }
        },
        'Manteca de cacao': {
             'peso': {
                (0, 11999): 0,
               
                (12000, float('inf')): 1
            },
            'fob': {
                (0, 44999): 0,
              
                (45000 , float('inf')): 1
            }
        },
        'pasta de cacao': {
            'peso': {
                (0, 7999): 0,
                
                (8000 , float('inf')): 1
            },
            'fob': {
                (0, 31999): 0,
                
                (32000 , float('inf')): 1
            }
        },
        'Cacao tostado': {
            'peso': {
                (0, 599): 0,
                
                (600 , float('inf')): 1
            },
            'fob': {
                (0, 3099): 0,
               
                (3100  , float('inf')): 1
            }
        },
        'otras preparaciones': {
             'peso': {
                (0, 949): 0,
               
                (950 , float('inf')): 1
            },
            'fob': {
                (0, 3899 ): 0,
                
                (3900  , float('inf')): 1
            }
        },
        'Cascara de cacao': {
             'peso': {
                (0, 12599): 0,
                
                (12600 , float('inf')): 1
            },
            'fob': {
                (0, 6599 ): 0,
               
                (6600 , float('inf')): 1
            }
        }
    }

    # Verificamos si la categoría está en los rangos predefinidos
    if categoria in rangos_calificaciones:
        calificacion_peso = None
        calificacion_fob = None
        
        # Verificamos el peso
        for rango, calificacion in rangos_calificaciones[categoria]['peso'].items():
            if rango[0] <= peso_kilos_netos <= rango[1]:
                calificacion_peso = calificacion
                break

        # Verificamos el valor FOB
        for rango, calificacion in rangos_calificaciones[categoria]['fob'].items():
            if rango[0] <= var_fob_dolar <= rango[1]:
                calificacion_fob = calificacion
                break

        # Si no se encontró una calificación para el peso o el valor FOB, retornamos None
        if calificacion_peso is None or calificacion_fob is None:
            return None
        
        # Calculamos el promedio de las calificaciones
        calificacion_promedio = (calificacion_peso + calificacion_fob) / 2
        
        # Determinamos si la venta es confiable o no
        if calificacion_promedio >=0.5:
            
            return 1
            
        else:
           
            return 0
        

    else:
        # Si la categoría no está en los rangos predefinidos, retornamos None
        return 0

# Escalador MinMax
scaler = MinMaxScaler()
# Cargar datos
BASE_DIR = Path(__file__).resolve().parent
ruta_archivo = BASE_DIR.parent / "in" / "cacao.xlsx"
ruta_archivo2 = BASE_DIR.parent / "in" / "input.xlsx"
datos = pd.read_excel(ruta_archivo)
datos2=pd.read_excel(ruta_archivo2)
# Preprocesamiento de datos
datos = convertir_tipos(datos)
datos = categorizar_trimestre(datos)
datos = categorizar_cosecha(datos)
datos = mapear_categoria(datos)
datos = llenar_na_continente_destino(datos)
datos = escalar_variables(datos)
datos = renombrar_columnas(datos)
datos = filtrar_paises(datos)
datos['venta_fiable'] = datos.apply(calcular_calificacion, axis=1)
datos['venta_fiable'] = datos['venta_fiable'].fillna(0)

datos[['Peso_kilos_netos']] = scaler.fit_transform(datos[['Peso_kilos_netos']])
datos[['Valor_FOB_USD']] = scaler.fit_transform(datos[['Valor_FOB_USD']])
datos = analisis_univariado(datos)
datos['venta_fiable'] = datos['venta_fiable'].fillna(0)
#preprocesamiento datos2
datos2 = convertir_tipos(datos2)
datos2 = categorizar_trimestre(datos2)
datos2 = categorizar_cosecha(datos2)
datos2 = mapear_categoria(datos2)
datos2 = llenar_na_continente_destino(datos2)
datos2= escalar_variables(datos2)
datos2 = renombrar_columnas(datos2)
datos2 = filtrar_paises(datos2)
datos2['venta_fiable'] = datos2.apply(calcular_calificacion, axis=1)
datos2['venta_fiable'] = datos2['venta_fiable'].fillna(0)

datos2[['Peso_kilos_netos']] = scaler.fit_transform(datos2[['Peso_kilos_netos']])
datos2[['Valor_FOB_USD']] = scaler.fit_transform(datos2[['Valor_FOB_USD']])
datos2 = analisis_univariado(datos2)
datos2['venta_fiable'] = datos2['venta_fiable'].fillna(0)



X = datos.drop(['venta_fiable'], axis=1)
y = datos['venta_fiable'].round().astype(int)
X_train, X_test, y_train, y_test , p_data= feature_selection(X,y)

#print("Se ejecuto anova y chicuadrado")

X_train = dummy_creation(X_train, list(p_data['Feature']))
X_test = dummy_creation(X_test, list(p_data['Feature']))

X_test = X_test.reindex(labels=X_train.columns, axis=1, fill_value=0)
y_test = y_test.reindex(axis=1, fill_value=0)


X_datos2 = datos2.drop(['venta_fiable'], axis=1)
y_datos2 = datos2['venta_fiable'].round().astype(int)

X_datos2 = dummy_creation(X_datos2, list(p_data['Feature']))
X_datos2 = X_datos2.reindex(columns=X_train.columns, fill_value=0)



#print(X_test)
#print(X_train)
#categorical_feat = list(datos.select_dtypes(include=['category','object']).columns)
#datos[categorical_feat] = datos[categorical_feat].applymap(str)
#print(datos[categorical_feat].nunique().reset_index().sort_values(by=0, ascending=False))
#print(y_train)
#print(y_test)
# Definir la función de tiempo de inicio
start_time = time.time()


# Crear y entrenar el modelo de Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')  
model.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
y_pred = model.predict(X_test)
y_pred2 =model.predict(X_datos2)

# Calcular métricas de evaluación
accuracy = accuracy_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='binary') 


# Calcular métricas de evaluación excel prueba

accuracy2 = accuracy_score(y_datos2, y_pred2)
mse2 = mean_squared_error(y_datos2, y_pred2)
cm2 = confusion_matrix(y_datos2, y_pred2)
precision2 = precision_score(y_datos2, y_pred2, average='binary')


# Mostrar resultados
print(f'Precisión del modelo: {accuracy}')
print(f'Precisión (Precision): {precision}')
print(f'Error Cuadrático Medio (MSE): {mse}')
print('Matriz de Confusión:')
print(cm)

# Mostrar resultados pruebas
print(f'Precisión del modelo prueba: {accuracy2}')
print(f'Precisión (Precision) prueba: {precision2}')
print(f'Error Cuadrático Medio (MSE) prueba: {mse2}')
print('Matriz de Confusión prueba: ')
print(cm2)

# Medir tiempo de ejecución
end_time = time.time()
execution_time = end_time - start_time
print(f'Tiempo de ejecución: {execution_time:.4f} segundos')
print(datos['venta_fiable'].value_counts())
print(datos['Categoria'].value_counts())
joblib.dump(model, "modelo.pkl")
# Guardar columnas finales del modelo
joblib.dump(X_train.columns.tolist(), "columnas_modelo.pkl")
joblib.dump(scaler, "scaler.pkl")