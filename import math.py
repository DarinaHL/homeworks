import math

class Shape:
    def __init__(self):
        pass

    @property
    def area(self):
        return self.get_area() #raise NotImplementedError
    
    @property
    def perimeter(self):
        return self.get_perimeter() #raise NotImplementedError
    
    def diagonal(self):
        if hasattr(self, 'get_diagonal'):
            return self.get_diagonal()
        raise NotImplementedError("Диагональ не определена для этой фигуры")


class InvalidShapeError(ValueError):
    pass


class Rectangle(Shape):
    def __init__(self, length, width):
        if length <= 0 or width <= 0:
            raise InvalidShapeError("Числа должны быть больше нуля.")
        self.length = length
        self.width = width

    def get_area(self):
        return self.length * self.width

    def get_perimeter(self):
        return 2 * (self.length + self.width)
    
    def get_diagonal(self):
        return (self.length ** 2 + self.width ** 2) ** 0.5
        


class Circle(Shape):
    def __init__(self, radius):
        if radius <= 0:
            raise InvalidShapeError("Радиус должен быть больше нуля.")
        self.radius = radius
    
    def get_area(self):
        return math.pi * (self.radius ** 2)
    
    def get_perimeter(self):
        return 2 * math.pi * self.radius
    

class Triangle(Shape):
    def __init__(self, A, B, C):
        if A <= 0 or B <= 0 or C <= 0:
            raise InvalidShapeError("Стороны треугольника должны быть больше нуля.")
        if A + B <= C or A + C <= B or B + C <= A:
            raise InvalidShapeError("Сумма любых двух сторон должна быть больше третьей стороны.")
        self.A = A
        self.B = B
        self.C = C
        self.P = (A + B + C) / 2

    def get_area(self):
        return (self.P * (self.P-self.A) * (self.P-self.B) * (self.P-self.C)) ** 0.5
    
    def get_perimeter(self):
        return self.A + self.B + self.C


if __name__ == "__main__":
    try:
        s = Rectangle(5, 3)
        print(s.area, s.perimeter, s.diagonal())
        s = Circle(3)
        print(f'{s.area:.2f}, {s.perimeter:.2f}')
        s = Triangle(3, 4, 5)
        print(s.area, s.perimeter)
    except InvalidShapeError as error:
        print(f"Ошибка: {error}")

