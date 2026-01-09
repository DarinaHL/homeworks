from src.logic.shapes import Rectangle, Line, Ellipse


class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str, start_point, end_point, color="black"):
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
            return Rectangle(x, y, w, h, color)
        elif shape_type == "ellipse":
            return Ellipse(x, y, w, h, color)
        elif shape_type == "line":
            return Line(x1, y1, x2, y2, color)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")

    @staticmethod
    def create_from_dict(data: dict):
        """
        Альтернативный метод создания фигур из словаря (для загрузки из файла)
        """
        shape_type = data.get("type")
        coords = data.get("coords", [])
        color = data.get("color", "black")

        if shape_type == "rect":
            if len(coords) >= 4:
                return Rectangle(*coords[:4], color)
        elif shape_type == "ellipse":
            if len(coords) >= 4:
                return Ellipse(*coords[:4], color)
        elif shape_type == "line":
            if len(coords) >= 4:
                return Line(*coords[:4], color)

        raise ValueError(f"Cannot create shape from data: {data}")