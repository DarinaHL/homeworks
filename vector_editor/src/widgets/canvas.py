# vector_editor/src/widgets/canvas.py
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QCursor
from src.logic.tools import CreationTool, SelectionTool


class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)

        # Включаем отслеживание движения мыши (для смены курсора)
        self.setMouseTracking(True)

        # Текущие настройки рисования
        self.current_color = "black"
        self.stroke_width = 2

        # Инициализация инструментов
        self.tools = {}
        self._init_tools()

        # Текущий активный инструмент
        self.active_tool = self.tools["select"]

    def _init_tools(self):
        """Инициализация всех доступных инструментов"""
        # Инструмент выделения
        self.tools["select"] = SelectionTool(self)

        # Инструменты создания фигур
        self.tools["line"] = CreationTool(self, "line", self.current_color, self.stroke_width)
        self.tools["rect"] = CreationTool(self, "rect", self.current_color, self.stroke_width)
        self.tools["ellipse"] = CreationTool(self, "ellipse", self.current_color, self.stroke_width)

    def set_tool(self, tool_name, color=None, stroke_width=None):
        """Установка активного инструмента"""
        # Обновляем настройки цвета и толщины
        if color:
            self.current_color = color
        if stroke_width:
            self.stroke_width = stroke_width

        # Обновляем настройки для всех инструментов создания
        for tool_key in ["line", "rect", "ellipse"]:
            if tool_key in self.tools:
                self.tools[tool_key].color = self.current_color
                self.tools[tool_key].stroke_width = self.stroke_width

        # Устанавливаем активный инструмент
        if tool_name in self.tools:
            self.active_tool = self.tools[tool_name]

            # Меняем курсор в зависимости от инструмента
            if tool_name == "select":
                self.setCursor(Qt.ArrowCursor)
                print(f"Выбран инструмент: {tool_name} (стрелка)")
            else:
                self.setCursor(Qt.CrossCursor)
                print(f"Выбран инструмент: {tool_name} (крестик)")
        else:
            print(f"Ошибка: неизвестный инструмент '{tool_name}'")

    # --- ПЕРЕОПРЕДЕЛЕНИЕ СОБЫТИЙ ---
    # Теперь просто делегируем события текущему инструменту

    def mousePressEvent(self, event):
        self.active_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.active_tool.mouse_release(event)

    # Дополнительно можно добавить метод для наведения курсора
    def mouseHoverEvent(self, event):
        # Эта опциональная функция может менять курсор при наведении на фигуру
        pass