# vector_editor/src/widgets/canvas.py
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
        
        # Добавляем сохранение начальной точки
        self.start_pos = None
        self.current_shape = None  # Для режима предпросмотра (опционально)

    def set_tool(self, tool_name):
        self.active_tool = tool_name

    # --- ПЕРЕОПРЕДЕЛЕНИЕ СОБЫТИЙ ---
    def mousePressEvent(self, event):
        # Сохраняем начальную точку для рисования
        if event.button() == Qt.LeftButton:
            self.start_pos = self.mapToScene(event.pos())
            
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Создаем фигуру только если была начальная точка и это левая кнопка
        if event.button() == Qt.LeftButton and self.start_pos:
            end_pos = self.mapToScene(event.pos())

            # 1. Используем Фабрику для создания фигуры
            try:
                new_shape = ShapeFactory.create_shape(
                    self.active_tool,
                    self.start_pos,
                    end_pos
                )
                # 2. Добавляем объект на сцену
                self.scene.addItem(new_shape)
                
            except ValueError as e:
                print(f"Ошибка создания фигуры: {e}")
            
            # Сбрасываем начальную точку
            self.start_pos = None

        super().mouseReleaseEvent(event)