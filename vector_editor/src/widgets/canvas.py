from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QPointF


class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)

        # Текущий инструмент (будет обновляться из Window)
        self.active_tool = "line"

    def set_tool(self, tool_name):
        self.active_tool = tool_name

    # --- ПЕРЕОПРЕДЕЛЕНИЕ СОБЫТИЙ ---

    def mousePressEvent(self, event):
        # 1. Получаем координаты клика в системе СЦЕНЫ
        scene_pos = self.mapToScene(event.pos())
        x, y = scene_pos.x(), scene_pos.y()

        print(f"Клик на сцене: {x:.1f}, {y:.1f} | Инструмент: {self.active_tool}")

        # 2. Простейшая реакция (Прототип рисования)
        if event.button() == Qt.LeftButton:
            if self.active_tool == "line":
                # Рисуем точку или маленькую линию для теста
                self.scene.addLine(x, y, x + 10, y + 10)
            elif self.active_tool == "rect":
                self.scene.addRect(x, y, 50, 50)

        # 3. Важно! Вызываем родительский метод,
        # чтобы работали стандартные функции (например, выделение объектов)
        super().mousePressEvent(event)
