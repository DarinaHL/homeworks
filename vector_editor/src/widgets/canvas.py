# vector_editor/src/widgets/canvas.py
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QRubberBand, QGraphicsItemGroup
from PySide6.QtCore import Qt, QPointF, QRect
from PySide6.QtGui import QCursor, QMouseEvent
from src.logic.tools import CreationTool, SelectionTool
from src.logic.shapes import Group


class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)

        # Включаем отслеживание движения мыши (для смены курсора)
        self.setMouseTracking(True)

        # Изначально отключаем режим выделения рамкой
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        # Текущие настройки рисования
        self.current_color = "black"
        self.stroke_width = 2

        # Инициализация инструментов
        self.tools = {}
        self._init_tools()

        # Текущий активный инструмент
        self.active_tool = self.tools["select"]

        # Инициализируем rubber band для выделения
        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.selection_start_pos = QPointF()

        # Флаг для отслеживания перетаскивания
        self.is_dragging = False

        # Флаг для отслеживания выделения рамкой
        self.is_selecting = False

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

            # Включаем/выключаем режим выделения рамкой
            if tool_name == "select":
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
                self.setCursor(Qt.ArrowCursor)
                print(f"Выбран инструмент: {tool_name}")
            else:
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
                self.setCursor(Qt.CrossCursor)
                print(f"Выбран инструмент: {tool_name} (крестик)")
        else:
            print(f"Ошибка: неизвестный инструмент '{tool_name}'")

    # --- ПЕРЕОПРЕДЕЛЕНИЕ СОБЫТИЙ ---

    def mousePressEvent(self, event):
        if self.active_tool == self.tools["select"]:
            super().mousePressEvent(event)
        else:
            event.accept()

        if self.active_tool == self.tools["select"]:
            if event.button() == Qt.LeftButton:
                pos = self.mapToScene(event.pos())
                item = self.scene.itemAt(pos, self.transform())

                if item and hasattr(item, 'type_name'):
                    self.is_dragging = True
                    self.setCursor(Qt.ClosedHandCursor)
                else:
                    self.is_selecting = True
                    self.selection_start_pos = event.pos()
                    self.rubber_band.setGeometry(QRect(self.selection_start_pos, event.pos()).normalized())
                    self.rubber_band.show()

        self.active_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        if self.active_tool == self.tools["select"]:
            super().mouseMoveEvent(event)

            if self.is_selecting and self.rubber_band.isVisible():
                self.rubber_band.setGeometry(QRect(self.selection_start_pos, event.pos()).normalized())

            if not self.is_dragging and not self.is_selecting:
                pos = self.mapToScene(event.pos())
                item = self.scene.itemAt(pos, self.transform())

                if item and hasattr(item, 'type_name'):
                    self.setCursor(Qt.OpenHandCursor)
                else:
                    self.setCursor(Qt.ArrowCursor)
        else:
            event.accept()

        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        if self.active_tool == self.tools["select"]:
            super().mouseReleaseEvent(event)

            if event.button() == Qt.LeftButton:
                if self.is_selecting:
                    self.is_selecting = False
                    self.rubber_band.hide()

                    rect = self.mapToScene(self.rubber_band.geometry()).boundingRect()
                    items_in_rect = self.scene.items(rect)

                    for item in items_in_rect:
                        if hasattr(item, 'type_name'):
                            item.setSelected(True)

                if self.is_dragging:
                    self.is_dragging = False

                    pos = self.mapToScene(event.pos())
                    item = self.scene.itemAt(pos, self.transform())
                    if item and hasattr(item, 'type_name'):
                        self.setCursor(Qt.OpenHandCursor)
                    else:
                        self.setCursor(Qt.ArrowCursor)
        else:
            event.accept()

        self.active_tool.mouse_release(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if not self.is_dragging and not self.is_selecting:
            self.setCursor(Qt.ArrowCursor)

    def group_selection(self):
        """Создает группу из выделенных элементов - ПРАВИЛЬНАЯ версия"""
        selected_items = self.scene.selectedItems()

        print(f"Попытка создать группу из {len(selected_items)} элементов")

        if len(selected_items) < 2:
            print("Недостаточно элементов для группировки (нужно минимум 2)")
            return

        try:
            # Фильтруем только наши фигуры
            items_to_group = []
            for item in selected_items:
                if hasattr(item, 'type_name'):
                    # Проверяем, что элемент не находится в другой группе
                    if not self._is_item_in_group(item):
                        print(f"Будет добавлен элемент типа: {item.type_name}")
                        items_to_group.append(item)
                    else:
                        print(f"Элемент {item.type_name} уже находится в группе, пропускаем")

            if len(items_to_group) < 2:
                print("Недостаточно фигур для группировки")
                return

            # Создаем новую группу
            group = Group()
            self.scene.addItem(group)

            # Собираем информацию о позициях элементов
            for item in items_to_group:
                # Сохраняем позицию элемента в сцене
                item_scene_pos = item.scenePos()

                # Снимаем выделение
                item.setSelected(False)

                # Добавляем в группу (это автоматически установит правильную позицию)
                group.addToGroup(item)

                # Устанавливаем позицию элемента относительно группы
                item.setPos(item_scene_pos - group.scenePos())

            # Выделяем группу
            group.setSelected(True)
            print(f"✓ Создана группа с {len(items_to_group)} элементами")

        except Exception as e:
            print(f"Ошибка при создании группы: {e}")
            import traceback
            traceback.print_exc()
            self.scene.clearSelection()

    def _is_item_in_group(self, item):
        """Проверяет, находится ли элемент в какой-либо группе"""
        parent = item.parentItem()
        while parent:
            if isinstance(parent, QGraphicsItemGroup):
                return True
            parent = parent.parentItem()
        return False

    def ungroup_selection(self):
        """Разбивает выделенные группы на отдельные элементы"""
        selected_items = self.scene.selectedItems()

        print(f"Попытка разгруппировать {len(selected_items)} элементов")

        groups_to_ungroup = []
        for item in selected_items:
            if hasattr(item, 'type_name') and item.type_name == "group":
                groups_to_ungroup.append(item)

        if not groups_to_ungroup:
            print("Нет групп для разгруппировки")
            return

        for group in groups_to_ungroup:
            try:
                if not isinstance(group, Group):
                    print(f"Пропускаем элемент: не является группой Group")
                    continue

                print(f"Разгруппировка группы с {len(group.childItems())} детьми")

                # Получаем позицию группы в сцене
                group_scene_pos = group.scenePos()

                # Получаем всех детей
                children = list(group.childItems())

                # Для каждого ребенка
                for child in children:
                    # Сохраняем позицию ребенка относительно группы
                    child_relative_pos = child.pos()

                    # Вычисляем позицию в сцене
                    child_scene_pos = group_scene_pos + child_relative_pos

                    # Удаляем из группы
                    group.removeFromGroup(child)

                    # Устанавливаем позицию в сцене
                    child.setPos(child_scene_pos)

                    # Выделяем
                    child.setSelected(True)

                # Удаляем пустую группу со сцены
                self.scene.removeItem(group)

                print(f"✓ Группа расформирована, возвращено {len(children)} элементов")

            except Exception as e:
                print(f"Ошибка при разгруппировке: {e}")
                import traceback
                traceback.print_exc()