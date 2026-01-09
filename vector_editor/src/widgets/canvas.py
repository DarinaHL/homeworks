# vector_editor/src/widgets/canvas.py
'''from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QBrush
import math
from src.logic.factory import ShapeFactory
'''

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QBrush
import math
from src.logic.factory import ShapeFactory

class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)

        # Текущий инструмент (будет обновляться из Window)
        self.active_tool = "line"

        #ДОБАВИЛА
        self.current_color = "black"  # Текущий цвет
        self.stroke_width = 2  # Текущая толщина линии
        #.

        # Добавляем сохранение начальной точки
        self.start_pos = None
        self.current_shape = None  # Для режима предпросмотра (опционально)

        '''# --- ВРЕМЕННЫЙ ТЕСТ (удалить позже) ---
        # Добавляем тестовые фигуры для проверки
        from src.logic.shapes import Rectangle, Line, Ellipse
        rect = Rectangle(50, 50, 100, 100, "red", 3)
        line = Line(200, 50, 300, 150, "blue", 5)
        ellipse = Ellipse(50, 200, 150, 80, "green", 2)

        self.scene.addItem(rect)
        self.scene.addItem(line)
        self.scene.addItem(ellipse)
        # --- КОНЕЦ ТЕСТА ---'''

    '''def set_tool(self, tool_name):
        self.active_tool = tool_name'''

    def set_tool(self, tool_name, color=None, stroke_width=None):
        self.active_tool = tool_name
        if color:
            self.current_color = color
            print(f"Canvas: установлен цвет {color}")  # Для отладки
        if stroke_width:
            self.stroke_width = stroke_width

    # --- ПЕРЕОПРЕДЕЛЕНИЕ СОБЫТИЙ ---
    def mousePressEvent(self, event):
        # Проверяем, есть ли фигура под курсором мыши
        items = self.scene.items(self.mapToScene(event.pos()))
        # Если есть фигуры под курсором - это клик по существующей фигуре
        # Не начинаем рисование новой фигуры
        if items and event.button() == Qt.LeftButton:
            # Есть фигура под курсором - передаем событие родителю для выделения/перемещения
            super().mousePressEvent(event)
            return
        # Если фигур под курсором нет - начинаем рисование
        if event.button() == Qt.LeftButton:
            self.start_pos = self.mapToScene(event.pos())
            print(f"Начало рисования в точке: {self.start_pos}, цвет: {self.current_color}")

        super().mousePressEvent(event)
        '''# Сохраняем начальную точку для рисования
        if event.button() == Qt.LeftButton:
            self.start_pos = self.mapToScene(event.pos())
            print(f"Начало рисования в точке: {self.start_pos}, цвет: {self.current_color}")  # Для отладки

        super().mousePressEvent(event)'''

    def mouseReleaseEvent(self, event):
        # Создаем фигуру только если была начальная точка и это левая кнопка
        if event.button() == Qt.LeftButton and self.start_pos:
            end_pos = self.mapToScene(event.pos())

            # 1. Используем Фабрику для создания фигуры
            try:
                '''new_shape = ShapeFactory.create_shape(
                    self.active_tool,
                    self.start_pos,
                    end_pos
                )'''
                new_shape = ShapeFactory.create_shape(
                    self.active_tool,
                    self.start_pos,
                    end_pos,
                    color=self.current_color,  # Используем текущий цвет
                    stroke_width=self.stroke_width  # Используем текущую толщину
                )
                # 2. Добавляем объект на сцену
                self.scene.addItem(new_shape)
                print(f"Создана фигура: {new_shape.type_name}, цвет: {self.current_color}")

            except ValueError as e:
                print(f"Ошибка создания фигуры: {e}")

            # Сбрасываем начальную точку
            self.start_pos = None

        super().mouseReleaseEvent(event)