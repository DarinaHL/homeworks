from src.logic.shapes import Rectangle, Line, Ellipse
from src.logic.shapes import Group

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str, start_point, end_point, color="black", stroke_width=2):  # Добавили stroke_width
        """
        Универсальный метод создания фигур.
        Принимает начальную и конечную точку (от мыши).
        """
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()

        # Вычисляем ширину и высоту для прямоугольных фигур
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)

        if shape_type == "rect":
            return Rectangle(x, y, w, h, color, stroke_width)  # Добавили stroke_width
        elif shape_type == "ellipse":
            return Ellipse(x, y, w, h, color, stroke_width)  # Добавили stroke_width
        elif shape_type == "line":
            return Line(x1, y1, x2, y2, color, stroke_width)  # Добавили stroke_width
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")

    @staticmethod
    def create_from_dict(data: dict):
        """
        Альтернативный метод создания фигур из словаря (для загрузки из файла)
        Теперь ожидает структуру с ключом "props"
        """
        shape_type = data.get("type")
        props = data.get("props", {})  # ЗАМЕНИЛИ "coords" на "props"
        pos = data.get("pos", [0, 0])  # Добавить поддержку позиции
        color = props.get("color", "black")
        stroke_width = props.get("stroke_width", 2)  # Добавили толщину линии

        if shape_type == "rect":
            x = props.get("x", 0)
            y = props.get("y", 0)
            w = props.get("w", 100)
            h = props.get("h", 100)
            rect = Rectangle(x, y, w, h, color, stroke_width)
            rect.setPos(pos[0], pos[1])  # Устанавливаем позицию
            return rect

        elif shape_type == "ellipse":
            x = props.get("x", 0)
            y = props.get("y", 0)
            w = props.get("w", 100)
            h = props.get("h", 100)
            ellipse = Ellipse(x, y, w, h, color, stroke_width)
            ellipse.setPos(pos[0], pos[1])
            return ellipse

        elif shape_type == "line":
            x1 = props.get("x1", 0)
            y1 = props.get("y1", 0)
            x2 = props.get("x2", 100)
            y2 = props.get("y2", 100)
            line = Line(x1, y1, x2, y2, color, stroke_width)
            line.setPos(pos[0], pos[1])
            return line

        raise ValueError(f"Cannot create shape from data: {data}")

    @staticmethod
    def _create_group(data: dict):
        """Рекурсивно создает группу из словаря"""
        # Получаем позицию группы
        pos = data.get("pos", [0, 0])
        x, y = pos

        # Создаем группу
        group = Group(x, y)

        # Рекурсивно создаем детей
        children_data = data.get("children", [])
        for child_data in children_data:
            child = ShapeFactory.from_dict(child_data)
            group.addToGroup(child)

        return group


    @staticmethod
    def from_dict(data: dict):
        """
        Восстанавливает объект из словаря с поддержкой рекурсии для групп
        """
        shape_type = data.get("type")

        if shape_type == "group":
            return ShapeFactory._create_group(data)
        else:
            # Используем существующий метод для примитивов
            return ShapeFactory.create_from_dict(data)