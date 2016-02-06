class Complexes(object):
    def __init__(self, items = []):
        self._complexes = items

    def __str__(self):
        line = ""
        for r, i in self._complexes:
            line = line + "(" + str(r) + ", " + str(i) + ")"
        return line

    def addition(self, real, imag):
        temp = []
        for r, i in self._complexes:
            r = r + real
            i = i + imag
            temp.append((r, i))

        self._complexes = temp

    def multiply(self, real, imag):
        temp = []
        for r, i in self._complexes:
            temp_real = r * real - i * imag
            temp_imag = r * imag + i * real

            temp.append((temp_real, temp_imag))
        self._complexes = temp
