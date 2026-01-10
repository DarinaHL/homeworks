from abc import ABC, abstractmethod, ABCMeta
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtGui import QPainterPath
from PySide6.QtWidgets import QGraphicsItemGroup

class MetaShape(type(QGraphicsPathItem), ABCMeta): pass


class Shape(QGraphicsPathItem, ABC, metaclass=MetaShape):
    def __init__(self, color="black", stroke_width=2):  # Добавили параметр stroke_width
        super().__init__()
        # Настраиваем внешний вид с учетом толщины линии
        pen = QPen(QColor(color))
        pen.setWidth(stroke_width)  # Теперь используем переданный параметр
        self.setPen(pen)

        # Сохраняем цвет для доступа
        self._color = color
        self._stroke_width = stroke_width

        # Флаги Qt
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)

    # Добавить метод для изменения цвета
    def set_active_color(self, color: str):
        """Устанавливает цвет фигуры"""
        self._color = color
        pen = self.pen()
        pen.setColor(QColor(color))
        self.setPen(pen)

    def set_stroke_width(self, width: int):
        """Устанавливает толщину линии фигуры"""
        self._stroke_width = width
        pen = self.pen()
        pen.setWidth(width)
        self.setPen(pen)

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
        # Исправленная структура для совместимости с factory.py
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],  # Используем pos() вместо self.x, self.y
            "props": {
                "x": self.x, "y": self.y,
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

    def set_active_color(self, color: str):
        super().set_active_color(color)
        self._color = color

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
            "pos": [self.pos().x(), self.pos().y()],  # Используем pos()
            "props": {
                "x1": self.x1, "y1": self.y1,
                "x2": self.x2, "y2": self.y2,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

    def set_active_color(self, color: str):
        super().set_active_color(color)
        self._color = color

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
            "pos": [self.pos().x(), self.pos().y()],  # Используем pos()
            "props": {
                "x": self.x, "y": self.y,
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

    def set_active_color(self, color: str):
        super().set_active_color(color)
        self._color = color

    def update_geometry(self, start_point, end_point):
        """Обновить геометрию эллипса по двум точкам"""
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()

        self.x = min(x1, x2)
        self.y = min(y1, y2)
        self.w = abs(x2 - x1)
        self.h = abs(y2 - y1)

        self._create_geometry()


class Group(QGraphicsItemGroup):
    """Класс для группировки фигур с использованием паттерна Composite"""

    def __init__(self, x=0, y=0):
        # Инициализация Qt-части
        QGraphicsItemGroup.__init__(self)

        # Сохраняем базовые свойства
        self._color = "black"
        self._stroke_width = 2

        # Устанавливаем позицию группы
        self.setPos(x, y)

        # Настраиваем флаги для группы
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)

        # ВАЖНО: Группа перехватывает события своих детей
        self.setHandlesChildEvents(True)

        # Убедимся, что группа может быть выделена
        self.setSelected(True)

    @property
    def type_name(self) -> str:
        return "group"

    def _create_geometry(self):
        """Для группы этот метод не нужен, так как геометрия определяется детьми"""
        pass

    def update_geometry(self, start_point, end_point):
        """Для группы этот метод не нужен"""
        pass

    def set_active_color(self, color: str):
        """
        Рекурсивно меняет цвет всех детей.
        Паттерн Composite: группа делегирует операцию детям.
        """
        for child in self.childItems():
            if isinstance(child, Shape):
                child.set_active_color(color)

    def to_dict(self) -> dict:
        """
        Рекурсивная сериализация группы.
        Сохраняет позицию группы и словари всех детей.
        """
        children_data = []
        for child in self.childItems():
            if hasattr(child, 'to_dict'):
                children_data.append(child.to_dict())

        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "children": children_data
        }

    def destroy_group(self, scene):
        """Разрушает группу, возвращая детей на сцену"""
        children = list(self.childItems())

        # Удаляем группу из сцены
        scene.removeItem(self)

        # Возвращаем детей на сцену
        for child in children:
            child.setParentItem(None)
            scene.addItem(child)
            child.setSelected(True)

    def set_stroke_width(self, width: int):
        """
        Рекурсивно меняет толщину линий всех детей.
        Паттерн Composite: группа делегирует операцию детям.
        """
        for child in self.childItems():
            if isinstance(child, Shape):
                child.set_stroke_width(width)