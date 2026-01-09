from abc import ABC, abstractmethod, ABCMeta
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtGui import QPainterPath

class MetaShape(type(QGraphicsPathItem), ABCMeta): pass

class Shape(QGraphicsPathItem, ABC, metaclass=MetaShape):
    def __init__(self, color="black", stroke_width=2):
        super().__init__()
        # Настраиваем внешний вид
        pen = QPen(QColor(color))
        pen.setWidth(stroke_width)
        self.setPen(pen)

        # Флаги Qt: разрешаем выделять и перетаскивать фигуру мышкой
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)

    @property
    @abstractmethod
    def type_name(self) -> str:
        """Возвращает строковый идентификатор типа фигуры ('rect', 'line')"""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Сериализация данных фигуры для сохранения в JSON"""
        pass


class Rectangle(Shape):
    def __init__(self, x, y, w, h, color="black"):
        super().__init__(color)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Формируем геометрию
        self._update_path()

    @property
    def type_name(self) -> str:
        return "rect"

    def _update_path(self):
        path = QPainterPath()
        path.addRect(self.x, self.y, self.w, self.h)
        self.setPath(path)  # Метод QGraphicsPathItem

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "coords": [self.x, self.y, self.w, self.h],
            "color": self.pen().color().name()
        }


# Добавим в shapes.py полные реализации Line и Ellipse

class Line(Shape):
    def __init__(self, x1, y1, x2, y2, color="black"):
        super().__init__(color)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self._update_path()

    @property
    def type_name(self) -> str:
        return "line"

    def _update_path(self):
        path = QPainterPath()
        path.moveTo(self.x1, self.y1)
        path.lineTo(self.x2, self.y2)
        self.setPath(path)

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "coords": [self.x1, self.y1, self.x2, self.y2],
            "color": self.pen().color().name()
        }


class Ellipse(Shape):
    def __init__(self, x, y, w, h, color="black"):
        super().__init__(color)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self._update_path()

    @property
    def type_name(self) -> str:
        return "ellipse"

    def _update_path(self):
        path = QPainterPath()
        path.addEllipse(self.x, self.y, self.w, self.h)
        self.setPath(path)

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "coords": [self.x, self.y, self.w, self.h],
            "color": self.pen().color().name()
        }