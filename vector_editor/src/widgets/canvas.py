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

        # Для перетаскивания
        self.drag_start_pos = None
        self.drag_item = None

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

    def change_selected_items_color(self, color):
        """Изменяет цвет всех выделенных фигур"""
        selected_items = self.scene.selectedItems()

        if not selected_items:
            print("Нет выделенных фигур для изменения цвета")
            return

        print(f"Меняем цвет у {len(selected_items)} выделенных фигур на {color}")

        changed_count = 0

        for item in selected_items:
            # Проверяем, является ли элемент нашей фигурой
            if hasattr(item, 'type_name'):
                try:
                    # Проверяем, есть ли у элемента метод set_active_color
                    if hasattr(item, 'set_active_color'):
                        item.set_active_color(color)
                        changed_count += 1
                        print(f"✓ Изменен цвет фигуры типа: {item.type_name}")
                    else:
                        print(f"У фигуры типа {item.type_name} нет метода set_active_color")
                except Exception as e:
                    print(f"Ошибка при изменении цвета фигуры: {e}")
            # Также обрабатываем группы
            elif isinstance(item, Group):
                try:
                    item.set_active_color(color)
                    changed_count += 1
                    print(f"✓ Изменен цвет группы (всех элементов внутри)")
                except Exception as e:
                    print(f"Ошибка при изменении цвета группы: {e}")

        print(f"✓ Изменен цвет у {changed_count} фигур")

        # Обновляем цвет для инструментов рисования
        self.current_color = color
        for tool_key in ["line", "rect", "ellipse"]:
            if tool_key in self.tools:
                self.tools[tool_key].color = color

    # --- ПЕРЕОПРЕДЕЛЕНИЕ СОБЫТИЙ ---

    def mousePressEvent(self, event):
        if self.active_tool == self.tools["select"]:
            shift_pressed = event.modifiers() & Qt.ShiftModifier

            # Получаем элемент под курсором
            pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(pos, self.transform())

            if event.button() == Qt.LeftButton:
                if item and hasattr(item, 'type_name'):
                    # Если нажат Shift
                    if shift_pressed:
                        # Меняем состояние выделения элемента
                        item.setSelected(not item.isSelected())
                        print(f"Shift+клик по {item.type_name}, новое состояние выделения: {item.isSelected()}")

                        # Если элемент стал выделенным, готовимся к перетаскиванию
                        if item.isSelected():
                            self.drag_item = item
                            self.drag_start_pos = event.pos()
                            self.is_dragging = True
                        else:
                            # Если сняли выделение
                            self.is_dragging = False
                    else:
                        # Если Shift не нажат
                        if not item.isSelected():
                            # Если элемент не выделен, очищаем все выделения и выделяем его
                            self.scene.clearSelection()
                            item.setSelected(True)

                        # Готовимся к перетаскиванию
                        self.drag_item = item
                        self.drag_start_pos = event.pos()
                        self.is_dragging = True
                else:
                    # Клик по пустому месту
                    if not shift_pressed:
                        self.scene.clearSelection()

                    self.is_selecting = True
                    self.is_dragging = False
                    self.selection_start_pos = event.pos()
                    self.rubber_band.setGeometry(QRect(self.selection_start_pos, event.pos()).normalized())
                    self.rubber_band.show()

            event.accept()
        else:
            # Для других инструментов передаем событие дальше
            self.active_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        if self.active_tool == self.tools["select"]:
            if self.is_selecting and self.rubber_band.isVisible():
                # Обновляем rubber band
                self.rubber_band.setGeometry(QRect(self.selection_start_pos, event.pos()).normalized())

            elif self.is_dragging and self.drag_start_pos and self.drag_item:
                # Перетаскиваем ВСЕ выделенные элементы
                selected_items = self.scene.selectedItems()

                if selected_items:
                    # Вычисляем дельту перемещения
                    current_pos = event.pos()
                    delta = current_pos - self.drag_start_pos

                    # Преобразуем дельту в координаты сцены
                    start_scene_pos = self.mapToScene(self.drag_start_pos)
                    current_scene_pos = self.mapToScene(current_pos)
                    scene_delta = current_scene_pos - start_scene_pos

                    # Перемещаем все выделенные элементы
                    for item in selected_items:
                        if hasattr(item, 'type_name'):
                            # Получаем текущую позицию
                            current_item_pos = item.pos()

                            # Если это первый шаг перетаскивания, запоминаем начальную позицию
                            if not hasattr(item, '_drag_initial_pos'):
                                item._drag_initial_pos = current_item_pos

                            # Вычисляем новую позицию
                            new_pos = item._drag_initial_pos + scene_delta

                            # Устанавливаем новую позицию
                            item.setPos(new_pos)

                    print(f"Перетаскивание {len(selected_items)} элементов, delta: {scene_delta}")

            elif not self.is_dragging and not self.is_selecting:
                # Просто движение курсора - меняем курсор
                pos = self.mapToScene(event.pos())
                item = self.scene.itemAt(pos, self.transform())

                if item and hasattr(item, 'type_name'):
                    self.setCursor(Qt.OpenHandCursor)
                else:
                    self.setCursor(Qt.ArrowCursor)

            event.accept()
        else:
            event.accept()

        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        if self.active_tool == self.tools["select"]:
            if event.button() == Qt.LeftButton:
                if self.is_selecting:
                    # Завершаем выделение рамкой
                    self.is_selecting = False
                    self.rubber_band.hide()

                    rect = self.mapToScene(self.rubber_band.geometry()).boundingRect()
                    items_in_rect = self.scene.items(rect)

                    shift_pressed = event.modifiers() & Qt.ShiftModifier

                    if not shift_pressed:
                        # Если Shift не нажат, очищаем выделение перед добавлением новых
                        self.scene.clearSelection()

                    for item in items_in_rect:
                        if hasattr(item, 'type_name'):
                            item.setSelected(True)

                if self.is_dragging:
                    # Завершаем перетаскивание
                    self.is_dragging = False

                    # Очищаем временные данные перетаскивания
                    selected_items = self.scene.selectedItems()
                    for item in selected_items:
                        if hasattr(item, '_drag_initial_pos'):
                            del item._drag_initial_pos

                    self.drag_item = None
                    self.drag_start_pos = None

                    # Возвращаем нормальный курсор
                    pos = self.mapToScene(event.pos())
                    item = self.scene.itemAt(pos, self.transform())
                    if item and hasattr(item, 'type_name'):
                        self.setCursor(Qt.OpenHandCursor)
                    else:
                        self.setCursor(Qt.ArrowCursor)

                    print("Перетаскивание завершено")

            event.accept()
        else:
            event.accept()

        self.active_tool.mouse_release(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if not self.is_dragging and not self.is_selecting:
            self.setCursor(Qt.ArrowCursor)

    def group_selection(self):
        """Создает группу из выделенных элементов - ИСПРАВЛЕННАЯ версия"""
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

            # ИЩЕМ МИНИМАЛЬНЫЕ КООРДИНАТЫ для центра группы
            min_x = float('inf')
            min_y = float('inf')

            for item in items_to_group:
                item_scene_pos = item.scenePos()
                min_x = min(min_x, item_scene_pos.x())
                min_y = min(min_y, item_scene_pos.y())

            # СОЗДАЕМ ГРУППУ В РАСЧЕТНОЙ ТОЧКЕ
            group = Group(min_x, min_y)  # Передаем координаты группы
            self.scene.addItem(group)

            # ПЕРЕМЕЩАЕМ ЭЛЕМЕНТЫ В ГРУППУ
            for item in items_to_group:
                # Получаем позицию элемента в сцене
                item_scene_pos = item.scenePos()

                # Снимаем выделение
                item.setSelected(False)

                # Вычисляем локальные координаты относительно группы
                local_x = item_scene_pos.x() - min_x
                local_y = item_scene_pos.y() - min_y

                # Удаляем элемент со сцены
                self.scene.removeItem(item)

                # Устанавливаем локальную позицию
                item.setPos(local_x, local_y)

                # Добавляем в группу
                group.addToGroup(item)

            # Устанавливаем позицию группы на сцене
            group.setPos(min_x, min_y)

            # Выделяем группу
            group.setSelected(True)
            print(f"✓ Создана группа с {len(items_to_group)} элементами в позиции ({min_x}, {min_y})")

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