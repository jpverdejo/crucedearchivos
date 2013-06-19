from datetime import datetime


class Validator:
    # Para efectos del programa un booleano sera un 1 o un 0, cualquier otro valor es invalido
    def isBoolean(self, value):
        if len(str(value)) == 1 and (str(value) == "1" or str(value) == "0"):
            return True

        return False

    def isInt(self, value):
        try:
            int(value)
            return int(value) > 0
        except ValueError:
            return False

    def isEmpty(self, value):
        return len(str(value)) == 0

    def validRUT(self, value):
        rut = value.split("-")

        if not self.isInt(rut[0]):
            return False

        # Dado que isInt solo respodne verdadero si el entero es mayor a 0 (de hecho deberia ser isNatural o algo asi)
        # tambien debemos revisar aparte si el DV es 0
        if not (self.isInt(rut[1]) or rut[1].upper() == "K" or rut[1] == "0"):
            return False

        if len(rut) != 2:
            return False

        return (self.digito_verificador(rut[0]) == rut[1].upper())

    # Codigo sacado de http://es.wikipedia.org/wiki/Rol_%C3%9Anico_Tributario
    def digito_verificador(self, rut):
        value = 11 - sum([int(a)*int(b) for a, b in zip(str(rut).zfill(8), '32765432')]) % 11
        return {10: 'K', 11: '0'}.get(value, str(value))

    def isValidDate(self, date):
        try:
            datetime.strptime(date, '%Y%m%d')

            return True
        except:
            return False
