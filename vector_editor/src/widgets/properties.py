# vector_editor/src/widgets/properties.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QSpinBox, QPushButton, QDoubleSpinBox, QHBoxLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QColorDialog
from PySide6.QtGui import QColor
from src.logic.shapes import Shape, Group
from src.logic.commands import ChangeColorMultipleCommand, ChangeWidthMultipleCommand


class PropertiesPanel(QWidget):
    """Панель свойств для редактирования параметров фигур"""

    # Сигнал для изменения цвета (для связи с главным окном)
    color_changed = Signal(str)
    stroke_width_changed = Signal(int)
    position_changed = Signal(float, float)

    def __init__(self, scene, undo_stack=None):  # Добавили параметр undo_stack
        super().__init__()
        self.scene = scene
        self.undo_stack = undo_stack  # Сохраняем ссылку на стек отмены

        # Настройка UI
        self._init_ui()

        # Подписка на сигнал изменения выделения (Паттерн Observer)
        self.scene.selectionChanged.connect(self.on_selection_changed)

    def _init_ui(self):
        # Ограничиваем ширину панели
        self.setFixedWidth(200)
        self.setStyleSheet("""
            PropertiesPanel {
                background-color: #f0f0f0;
                border-left: 1px solid #ccc;
            }
            QLabel {
                font-weight: bold;
                margin-top: 5px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Заголовок
        title = QLabel("Свойства")
        title.setStyleSheet("font-weight: bold; font-size: 14px; background-color: #e0e0e0; padding: 5px;")
        layout.addWidget(title)

        # Метка типа объекта
        self.lbl_type = QLabel("Тип: ---")
        self.lbl_type.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.lbl_type)

        # Разделитель
        layout.addWidget(QLabel("─────"))

        # 1. Геометрия (X, Y)
        layout.addWidget(QLabel("Позиция:"))

        geo_layout = QHBoxLayout()
        self.spin_x = QDoubleSpinBox()
        self.spin_x.setRange(-10000, 10000)
        self.spin_x.setPrefix("X: ")
        self.spin_x.setDecimals(0)
        self.spin_x.valueChanged.connect(self.on_position_changed)

        self.spin_y = QDoubleSpinBox()
        self.spin_y.setRange(-10000, 10000)
        self.spin_y.setPrefix("Y: ")
        self.spin_y.setDecimals(0)
        self.spin_y.valueChanged.connect(self.on_position_changed)

        geo_layout.addWidget(self.spin_x)
        geo_layout.addWidget(self.spin_y)
        layout.addLayout(geo_layout)

        # 2. Толщина линии
        layout.addWidget(QLabel("Толщина линии:"))
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 50)
        self.spin_width.setSuffix(" px")
        self.spin_width.valueChanged.connect(self.on_width_changed)
        layout.addWidget(self.spin_width)

        # 3. Цвет линии
        layout.addWidget(QLabel("Цвет линии:"))
        self.btn_color = QPushButton()
        self.btn_color.setFixedHeight(30)
        self.btn_color.setStyleSheet("""
            QPushButton {
                border: 2px solid #888888;
                border-radius: 4px;
            }
            QPushButton:hover {
                border: 2px solid #666666;
            }
        """)
        self.btn_color.clicked.connect(self.on_color_clicked)
        layout.addWidget(self.btn_color)

        # Информация о выделении
        self.lbl_selection_info = QLabel("Выделено: 0")
        self.lbl_selection_info.setStyleSheet("color: #666; font-size: 10pt;")
        layout.addWidget(self.lbl_selection_info)

        # Добавляем пружину
        layout.addStretch()

        # Исходное состояние: панель выключена
        self.setEnabled(False)

    # --- MODEL -> VIEW (Чтение данных) ---
    def on_selection_changed(self):
        """Вызывается при изменении выделения на сцене"""
        selected_items = self.scene.selectedItems()

        # Обновляем информацию о выделении
        self.lbl_selection_info.setText(f"Выделено: {len(selected_items)}")

        # Сценарий 1: Ничего не выделено
        if not selected_items:
            self.setEnabled(False)
            self.lbl_type.setText("Тип: ---")
            self.btn_color.setStyleSheet("background-color: transparent; border: 2px solid #888888;")
            return

        # Сценарий 2: Что-то выделено
        self.setEnabled(True)

        # Берем первый элемент для отображения свойств
        item = selected_items[0]

        # Определяем тип объекта
        if hasattr(item, 'type_name'):
            type_name = item.type_name
            if type_name == "rect":
                display_name = "Прямоугольник"
            elif type_name == "line":
                display_name = "Линия"
            elif type_name == "ellipse":
                display_name = "Эллипс"
            elif type_name == "group":
                display_name = "Группа"
            else:
                display_name = type_name.capitalize()

            if len(selected_items) > 1:
                display_name += f" (+{len(selected_items) - 1})"

            self.lbl_type.setText(f"Тип: {display_name}")
        else:
            self.lbl_type.setText(f"Тип: {type(item).__name__}")

        # Получаем свойства первого объекта
        current_width = 2
        current_color = "#000000"

        if hasattr(item, "pen"):
            current_width = item.pen().width()
            current_color = item.pen().color().name()

        # Получаем позицию
        pos = item.pos()
        current_x = pos.x()
        current_y = pos.y()

        # Обновляем UI, блокируя сигналы, чтобы избежать циклических вызовов
        self.spin_width.blockSignals(True)
        self.spin_x.blockSignals(True)
        self.spin_y.blockSignals(True)

        self.spin_width.setValue(current_width)
        self.spin_x.setValue(current_x)
        self.spin_y.setValue(current_y)

        self.btn_color.setStyleSheet(f"""
            background-color: {current_color};
            border: 2px solid #888888;
            border-radius: 4px;
        """)

        self.spin_width.blockSignals(False)
        self.spin_x.blockSignals(False)
        self.spin_y.blockSignals(False)

    # --- VIEW -> MODEL (Изменение данных) ---
    def on_width_changed(self, value):
        """Изменение толщины линии с поддержкой отмены"""
        selected_items = self.scene.selectedItems()

        if not selected_items or not self.undo_stack:
            return

        # Фильтруем только наши фигуры
        items_to_change = []
        old_widths = []
        for item in selected_items:
            if hasattr(item, 'type_name'):
                items_to_change.append(item)
                old_widths.append(item.pen().width() if hasattr(item, 'pen') else 2)

        if items_to_change:
            # Создаем команду изменения толщины
            command = ChangeWidthMultipleCommand(items_to_change, value, old_widths)
            self.undo_stack.push(command)

        self.scene.update()
        self.stroke_width_changed.emit(value)

    def on_color_clicked(self):
        """Открытие диалога выбора цвета с поддержкой отмены"""
        # Получаем текущий цвет кнопки
        current_style = self.btn_color.styleSheet()
        current_color = "#000000"

        # Пытаемся извлечь цвет из стиля (грубый способ)
        import re
        match = re.search(r'background-color:\s*([^;]+)', current_style)
        if match:
            current_color = match.group(1).strip()

        # Открываем диалог
        color = QColorDialog.getColor(QColor(current_color), self, "Выберите цвет линии")

        if color.isValid():
            hex_color = color.name()

            # Обновляем кнопку
            self.btn_color.setStyleSheet(f"""
                background-color: {hex_color};
                border: 2px solid #888888;
                border-radius: 4px;
            """)

            # Применяем цвет к выделенным объектам с поддержкой отмены
            selected_items = self.scene.selectedItems()

            if not selected_items or not self.undo_stack:
                return

            # Фильтруем только наши фигуры
            items_to_change = []
            old_colors = []
            for item in selected_items:
                if hasattr(item, 'type_name'):
                    items_to_change.append(item)
                    if hasattr(item, 'pen'):
                        old_colors.append(item.pen().color().name())
                    else:
                        old_colors.append("#000000")

            if items_to_change:
                # Создаем команду изменения цвета
                command = ChangeColorMultipleCommand(items_to_change, hex_color, old_colors)
                self.undo_stack.push(command)

            self.scene.update()
            self.color_changed.emit(hex_color)

    def on_position_changed(self, value):
        """Изменение позиции объекта"""
        selected_items = self.scene.selectedItems()

        new_x = self.spin_x.value()
        new_y = self.spin_y.value()

        for item in selected_items:
            item.setPos(new_x, new_y)

        self.scene.update()
        self.position_changed.emit(new_x, new_y)