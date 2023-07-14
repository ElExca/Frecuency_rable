def statistical_calculator(arr_sorted):
    media = sum(arr_sorted) / len(arr_sorted)

    desviacion = 0
    for elemento in arr_sorted:
        desviacion += abs(elemento - media)
    desviacion_media = round(desviacion / len(arr_sorted), 2)

    varianza_resultado = 0
    for elemento in arr_sorted:
        valor = pow(abs(elemento - media),2)
        varianza_resultado = varianza_resultado + valor
    varianza = round(varianza_resultado/len(arr_sorted),2)

    desviacion_estandar = (varianza ** .5)
    print(f'La desviacion estandar {round(desviacion_estandar, 2)}')

    return desviacion_media, media,varianza, desviacion_estandar
