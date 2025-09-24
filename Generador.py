import random
generador = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
longitud = int(input("Introduce la longitud de la contraseña: "))
contraseña = ""
for i in range(longitud):
    contraseña += random.choice(generador)
print("Tu contraseña generada es: ",contraseña)
