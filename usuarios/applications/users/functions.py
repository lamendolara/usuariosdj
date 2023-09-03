# Funciones extra de la app users

import random
import string

#en este caso definimos que el codigo sea de 6 digitos compuestos de letras mayusculas y digitos.
def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) 
