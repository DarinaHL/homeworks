from abc import ABC, abstractmethod, ABCMeta
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtGui import QPainterPath

class MetaShape(type(QGraphicsPathItem), ABCMeta): pass

# ЗАМЕНИТЬ текущий код классов фигур на этот:

class Shape(QGraphicsPathItem, ABC, metaclass=MetaShape):
    def __init__(self, color="black", stroke_width=2):  # Добавили параметр stroke_width
        super().__init__()
        # Настраиваем внешний вид с учетом толщины линии
        pen = QPen(QColor(color))
        pen.setWidth(stroke_width)  # Теперь используем переданный параметр
        self.setPen(pen)

        # Флаги Qt
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)

    @property
    @abstractmethod
    def type_name(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class Rectangle(Shape):
    def __init__(self, x, y, w, h, color="black", stroke_width=2):  # Добавили stroke_width
        # 1. Инициализация родителя с новым параметром
        super().__init__(color, stroke_width)

        # 2. Сохраняем "Бизнес-данные" (для сохранения в файл)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # 3. Создаем визуальное представление
        self._create_geometry()  # Изменили название с _update_path

    def _create_geometry(self):
        path = QPainterPath()
        path.addRect(self.x, self.y, self.w, self.h)
        self.setPath(path)

    @property
    def type_name(self) -> str:
        return "rect"

    def to_dict(self) -> dict:
        # Изменили структуру: теперь "props" вместо "coords"
        return {
            "type": self.type_name,
            "props": {  # ЗАМЕНИТЬ "coords" на "props"
                "x": self.x, "y": self.y,
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()  # Добавили толщину линии
            }
        }

    def update_geometry(self, start_point, end_point):
        """Обновить геометрию прямоугольника по двум точкам"""
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()

        self.x = min(x1, x2)
        self.y = min(y1, y2)
        self.w = abs(x2 - x1)
        self.h = abs(y2 - y1)

        self._create_geometry()  # Перерисовываем путь


class Line(Shape):
    def __init__(self, x1, y1, x2, y2, color="black", stroke_width=2):  # Добавили stroke_width
        super().__init__(color, stroke_width)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self._create_geometry()  # Изменили название

    def _create_geometry(self):
        path = QPainterPath()
        path.moveTo(self.x1, self.y1)
        path.lineTo(self.x2, self.y2)
        self.setPath(path)

    @property
    def type_name(self) -> str:
        return "line"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "props": {  # ЗАМЕНИТЬ "coords" на "props"
                "x1": self.x1, "y1": self.y1,
                "x2": self.x2, "y2": self.y2,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()  # Добавили толщину линии
            }
        }

    def update_geometry(self, start_point, end_point):
        """Обновить геометрию линии по двум точкам"""
        self.x1 = start_point.x()
        self.y1 = start_point.y()
        self.x2 = end_point.x()
        self.y2 = end_point.y()

        self._create_geometry()


class Ellipse(Shape):
    def __init__(self, x, y, w, h, color="black", stroke_width=2):  # Добавили stroke_width
        super().__init__(color, stroke_width)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._create_geometry()  # Изменили название

    def _create_geometry(self):
        path = QPainterPath()
        path.addEllipse(self.x, self.y, self.w, self.h)
        self.setPath(path)

    @property
    def type_name(self) -> str:
        return "ellipse"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "props": {  # ЗАМЕНИТЬ "coords" на "props"
                "x": self.x, "y": self.y,
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()  # Добавили толщину линии
            }
        }

    def update_geometry(self, start_point, end_point):
        """Обновить геометрию эллипса по двум точкам"""
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()

        self.x = min(x1, x2)
        self.y = min(y1, y2)
        self.w = abs(x2 - x1)
        self.h = abs(y2 - y1)

        self._create_geometry()