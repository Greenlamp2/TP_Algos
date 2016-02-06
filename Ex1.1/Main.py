class Complexe(object):

    def __init__(self, real=0, imag=0):
        self._real = real
        self._imag = imag

    def copy(self):
        return Complexe(self._real, self._imag)

    def __str__(self):
        return "(" + str(self._real) + ", " + str(self._imag) + ")"

    def set_real(self, real):
        self._real = real

    def get_real(self):
        return self._real

    def get_imag(self):
        return self._imag

    def set_imag(self, imag):
        self._imag = imag

    def add(self, complexe):
        self._real = self._real + complexe.get_real()
        self._imag = self._imag + complexe.get_imag()

    def multiply(self, complexe):
        #(a+bi) * (c+di) = ac + adi + cdi + bidi²
        temp_real = self._real * complexe.get_real() - self._imag * complexe.get_imag()
        temp_imag = self._real * complexe.get_imag() + self._imag * complexe.get_real()

        self._real = temp_real
        self._imag = temp_imag



if __name__ == "__main__":
    c1 = Complexe(1, 2)
    print("Complexe 1:")
    print(c1)

    c2 = Complexe()
    print("Complexe 2:")
    print(c2)

    print("addition")
    c2.add(c1)
    print(c1)

    print("multiplication")
    c1.multiply(c2)
    print(c1)

    print("copie")
    c3 = c1.copy()
    print(c3)