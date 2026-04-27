def calcular_calificacion(row):

    categoria = str(row['Categoria'])  
    peso_kilos_netos = row['Peso_kilos_netos']
    var_fob_dolar = row['Valor_FOB_USD']

    rangos_calificaciones = {
        'Chocolates': {
            'peso': {(0, 890): 0, (891, float('inf')): 1},
            'fob': {(0, 2499): 0, (2500, float('inf')): 1}
        },
        'Cacao en polvo': {
            'peso': {(0, 2821): 0, (2822, float('inf')): 1},
            'fob': {(0, 6344): 0, (6345, float('inf')): 1}
        },
        'Cacao crudo': {
            'peso': {(0, 24999): 0, (25000, float('inf')): 1},
            'fob': {(0, 66999): 0, (67000, float('inf')): 1}
        },
        'Manteca de cacao': {
            'peso': {(0, 11999): 0, (12000, float('inf')): 1},
            'fob': {(0, 44999): 0, (45000, float('inf')): 1}
        },
        'pasta de cacao': {
            'peso': {(0, 7999): 0, (8000, float('inf')): 1},
            'fob': {(0, 31999): 0, (32000, float('inf')): 1}
        },
        'Cacao tostado': {
            'peso': {(0, 599): 0, (600, float('inf')): 1},
            'fob': {(0, 3099): 0, (3100, float('inf')): 1}
        },
        'otras preparaciones': {
            'peso': {(0, 949): 0, (950, float('inf')): 1},
            'fob': {(0, 3899): 0, (3900, float('inf')): 1}
        },
        'Cascara de cacao': {
            'peso': {(0, 12599): 0, (12600, float('inf')): 1},
            'fob': {(0, 6599): 0, (6600, float('inf')): 1}
        }
    }

    if categoria in rangos_calificaciones:

        calificacion_peso = None
        calificacion_fob = None

        for rango, calificacion in rangos_calificaciones[categoria]['peso'].items():
            if rango[0] <= peso_kilos_netos <= rango[1]:
                calificacion_peso = calificacion
                break

        for rango, calificacion in rangos_calificaciones[categoria]['fob'].items():
            if rango[0] <= var_fob_dolar <= rango[1]:
                calificacion_fob = calificacion
                break

        if calificacion_peso is None or calificacion_fob is None:
            return 0

        promedio = (calificacion_peso + calificacion_fob) / 2

        return 1 if promedio >= 0.5 else 0

    return 0
