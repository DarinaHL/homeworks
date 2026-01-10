# vector_editor/src/logic/tools.py
from abc import ABC, abstractmethod
from PySide6.QtCore import Qt, QPointF
from src.logic.factory import ShapeFactory
from PySide6.QtWidgets import QGraphicsView


class Tool(ABC):
    """Абстрактный базовый класс для всех инструментов"""

    def __init__(self, canvas_view):
        self.view = canvas_view  # Ссылка на View
        self.scene = canvas_view.scene  # Ссылка на Сцену

    @abstractmethod
    def mouse_press(self, event):
        """Обработка нажатия кнопки мыши"""
        pass

    @abstractmethod
    def mouse_move(self, event):
        """Обработка движения мыши"""
        pass

    @abstractmethod
    def mouse_release(self, event):
        """Обработка отпускания кнопки мыши"""
        pass


class CreationTool(Tool):
    """Инструмент для создания фигур с предпросмотром"""

    def __init__(self, canvas_view, shape_type, color="black", stroke_width=2):
        super().__init__(canvas_view)
        self.shape_type = shape_type
        self.color = color
        self.stroke_width = stroke_width
        self.current_shape = None  # Временная фигура для предпросмотра
        self.start_pos = None
        self.is_drawing = False

    def mouse_press(self, event):
        """Начало рисования"""
        if event.button() == Qt.LeftButton:
            self.is_drawing = True
            self.start_pos = self.view.mapToScene(event.pos())

            # Создаем фигуру нулевого размера для предпросмотра
            self.current_shape = ShapeFactory.create_shape(
                self.shape_type,
                self.start_pos,
                self.start_pos,  # Начало и конец совпадают
                color=self.color,
                stroke_width=self.stroke_width
            )
            self.scene.addItem(self.current_shape)

    def mouse_move(self, event):
        """Обновление предпросмотра фигуры при движении мыши"""
        if self.is_drawing and self.current_shape:
            end_pos = self.view.mapToScene(event.pos())

            # ЭФФЕКТИВНЫЙ ВАРИАНТ: обновляем геометрию существующей фигуры
            if hasattr(self.current_shape, 'update_geometry'):
                self.current_shape.update_geometry(self.start_pos, end_pos)
            else:
                # Запасной вариант: удаляем и создаем заново
                self.scene.removeItem(self.current_shape)
                self.current_shape = ShapeFactory.create_shape(
                    self.shape_type,
                    self.start_pos,
                    end_pos,
                    color=self.color,
                    stroke_width=self.stroke_width
                )
                self.scene.addItem(self.current_shape)

    def mouse_release(self, event):
        """Завершение рисования - фигура фиксируется"""
        if event.button() == Qt.LeftButton and self.is_drawing:
            # Фигура уже на сцене - просто сбрасываем ссылки
            self.current_shape = None
            self.is_drawing = False


class SelectionTool(Tool):
    """Инструмент для выделения и перемещения фигур"""

    def __init__(self, canvas_view):
        super().__init__(canvas_view)
        self.drag_start_pos = None
        self.is_dragging = False

    def mouse_press(self, event):
        """Обработка нажатия мыши - делегируем основному холсту"""
        # Пустая реализация - вся логика теперь в EditorCanvas
        pass

    def mouse_move(self, event):
        """Обработка движения мыши - делегируем основному холсту"""
        # Пустая реализация - вся логика теперь в EditorCanvas
        pass

    def mouse_release(self, event):
        """Обработка отпускания мыши - делегируем основному холсту"""
        # Пустая реализация - вся логика теперь в EditorCanvas
        pass