my_list = [1, 2, 3, 4, 5]

# for element in my_list: # como se recorre una lista normalmente
#     print(element)

# a continuacion se ve como funciona un ciclo for por dentro
# convierte la list a tipo iter y luego ejecuta next varias veces hasta que salga el error porque no hay
# mas elemento y ahi se detiene

my_iter = iter(my_list)

# print(type(my_iter)) # muestra el tipo de dato que es my_iter

# Extraer los elementos

print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))