# vector_editor/src/app.py
from PySide6.QtGui import QCloseEvent, QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
from src.widgets.canvas import EditorCanvas
from src.widgets.properties import PropertiesPanel  # ИМПОРТИРУЕМ НОВЫЙ КЛАСС
from PySide6.QtWidgets import QColorDialog
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QUndoView  # QUndoView остаётся в QtWidgets


class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vector Editor")
        self.resize(1200, 700)  # Увеличиваем окно для панели свойств

        # Сначала создаем canvas
        self.canvas = EditorCanvas()
        self.canvas.set_tool("select")

        # Текущий выбранный цвет
        self.current_color = "black"

        # Затем настраиваем UI
        self._init_ui()
        self._setup_layout()

        print("✓ Окно редактора инициализировано")

    def _init_ui(self):
        # 1. Создаем строку состояния
        self.statusBar().showMessage("Готов к работе")

        # 2. Создаем Меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        # Добавляем меню Edit
        edit_menu = menubar.addMenu("&Edit")

        # 3. Создаем Action (Действие)
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Close the application")
        exit_action.triggered.connect(self.close)

        # Добавляем Action в меню
        file_menu.addAction(exit_action)

        # Действие для Undo
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setStatusTip("Отменить последнее действие")
        undo_action.triggered.connect(self.on_undo)
        edit_menu.addAction(undo_action)

        # Действие для Redo
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.setStatusTip("Повторить отмененное действие")
        redo_action.triggered.connect(self.on_redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        # Действие для Delete
        delete_action = QAction("&Delete", self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.setStatusTip("Удалить выделенные объекты")
        delete_action.triggered.connect(self.on_delete)
        edit_menu.addAction(delete_action)

        # Action для группировки - ИЗМЕНИТЬ на Shift+G
        group_action = QAction("&Group", self)
        group_action.setShortcut(QKeySequence("Shift+G"))
        group_action.triggered.connect(self.on_group_selection)
        group_action.setStatusTip("Group selected items")
        edit_menu.addAction(group_action)

        # Action для разгруппировки - ИЗМЕНИТЬ на Shift+U
        ungroup_action = QAction("&Ungroup", self)
        ungroup_action.setShortcut(QKeySequence("Shift+U"))
        ungroup_action.triggered.connect(self.on_ungroup_selection)
        ungroup_action.setStatusTip("Ungroup selected items")
        edit_menu.addAction(ungroup_action)

        # Действие для показа истории команд (Wow-эффект)
        history_action = QAction("&Show History", self)
        history_action.setShortcut("Ctrl+H")
        history_action.setStatusTip("Показать историю команд")
        history_action.triggered.connect(self.on_show_history)
        edit_menu.addAction(history_action)

        # 4. Создаем Тулбар
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.addAction(exit_action)
        toolbar.addSeparator()
        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)
        toolbar.addSeparator()
        toolbar.addAction(delete_action)

        print("✓ Меню и тулбары созданы")

    def on_undo(self):
        """Обработчик для Undo"""
        if self.canvas.undo_stack.canUndo():
            self.canvas.undo_stack.undo()
            print("Выполнено Undo")

    def on_redo(self):
        """Обработчик для Redo"""
        if self.canvas.undo_stack.canRedo():
            self.canvas.undo_stack.redo()
            print("Выполнено Redo")

    def on_delete(self):
        """Обработчик для Delete"""
        print("Нажата Delete - удаление выделенных элементов")
        self.canvas.delete_selected()

    def on_group_selection(self):
        """Обработчик для группировки"""
        print("Нажата Shift+G - группировка...")
        self.canvas.group_selection()

    def on_ungroup_selection(self):
        """Обработчик для разгруппировки"""
        print("Нажата Shift+U - разгруппировка...")
        self.canvas.ungroup_selection()

    def on_show_history(self):
        """Показывает окно с историей команд (Wow-эффект)"""
        self.history_window = QUndoView(self.canvas.undo_stack)
        self.history_window.setWindowTitle("История команд")
        self.history_window.resize(300, 400)
        self.history_window.show()

    def _setup_layout(self):
        # 1. Создаем главный контейнер
        container = QWidget()
        self.setCentralWidget(container)

        # 2. Основной лейаут (Горизонтальный: Слева панель инструментов, Справа холст и панель свойств)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # --- Левая панель (Палитра инструментов) ---
        tools_panel = QFrame()
        tools_panel.setFixedWidth(150)
        tools_panel.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-right: 1px solid #cccccc;
            }
            QPushButton {
                padding: 8px;
                margin: 2px;
                text-align: left;
            }
            QPushButton:checked {
                background-color: #d0e0ff;
                border: 1px solid #a0c0ff;
            }
        """)

        # Внутри панели кнопки идут вертикально
        tools_layout = QVBoxLayout(tools_panel)
        tools_layout.setSpacing(5)

        # Заголовок панели
        tools_title = QPushButton("Инструменты")
        tools_title.setEnabled(False)
        tools_title.setStyleSheet("font-weight: bold; background-color: #e0e0e0;")
        tools_layout.addWidget(tools_title)

        # Создаем кнопки инструментов
        self.btn_select = QPushButton("Выделение (Select)")
        self.btn_line = QPushButton("Линия (Line)")
        self.btn_rect = QPushButton("Прямоугольник (Rect)")
        self.btn_ellipse = QPushButton("Эллипс (Ellipse)")
        self.btn_color = QPushButton("Выбор цвета")

        # Делаем кнопки "залипающими" (Checkable) - как RadioButtons
        self.btn_select.setCheckable(True)
        self.btn_line.setCheckable(True)
        self.btn_rect.setCheckable(True)
        self.btn_ellipse.setCheckable(True)

        # По умолчанию активен инструмент Select
        self.btn_select.setChecked(True)
        self.current_tool = "select"

        # Добавляем кнопки на панель
        tools_layout.addWidget(self.btn_select)
        tools_layout.addWidget(self.btn_line)
        tools_layout.addWidget(self.btn_rect)
        tools_layout.addWidget(self.btn_ellipse)
        tools_layout.addWidget(self.btn_color)

        self.color_preview = QFrame()
        self.color_preview.setFixedHeight(40)
        self.color_preview.setStyleSheet("""
            QFrame {
                background-color: black; 
                border: 2px solid #888888;
                border-radius: 4px;
            }
        """)
        tools_layout.addWidget(self.color_preview)

        # Добавим подсказку про группировку
        group_tip = QPushButton("Подсказка:")
        group_tip.setEnabled(False)
        group_tip.setStyleSheet("text-align: left; font-style: italic; background-color: #f0f0f0;")
        tools_layout.addWidget(group_tip)

        tip_text = QPushButton("1. Выделите фигуры\n2. Нажмите Shift+G")
        tip_text.setEnabled(False)
        tip_text.setStyleSheet("text-align: left; font-size: 10pt; background-color: #f8f8f8;")
        tools_layout.addWidget(tip_text)

        # Добавим подсказку про изменение цвета
        color_tip = QPushButton("Изменить цвет:")
        color_tip.setEnabled(False)
        color_tip.setStyleSheet("text-align: left; font-style: italic; background-color: #f0f0f0;")
        tools_layout.addWidget(color_tip)

        color_tip_text = QPushButton("1. Выделите фигуры\n2. Нажмите кнопку\n'Выбор цвета'")
        color_tip_text.setEnabled(False)
        color_tip_text.setStyleSheet("text-align: left; font-size: 10pt; background-color: #f8f8f8;")
        tools_layout.addWidget(color_tip_text)

        # Добавим подсказку про Undo/Redo
        undo_tip = QPushButton("Горячие клавиши:")
        undo_tip.setEnabled(False)
        undo_tip.setStyleSheet("text-align: left; font-style: italic; background-color: #f0f0f0;")
        tools_layout.addWidget(undo_tip)

        undo_tip_text = QPushButton("Ctrl+Z - Отменить\nCtrl+Y - Повторить\nDel - Удалить")
        undo_tip_text.setEnabled(False)
        undo_tip_text.setStyleSheet("text-align: left; font-size: 10pt; background-color: #f8f8f8;")
        tools_layout.addWidget(undo_tip_text)

        tools_layout.addStretch()  # Пружина, которая прижмет кнопки наверх

        # СВЯЗЫВАЕМ СИГНАЛЫ КНОПОК С МЕТОДАМИ
        self.btn_select.clicked.connect(lambda: self.on_change_tool("select"))
        self.btn_line.clicked.connect(lambda: self.on_change_tool("line"))
        self.btn_rect.clicked.connect(lambda: self.on_change_tool("rect"))
        self.btn_ellipse.clicked.connect(lambda: self.on_change_tool("ellipse"))

        self.btn_color.clicked.connect(self.on_change_color)

        # --- Создаем панель свойств ---
        self.props_panel = PropertiesPanel(self.canvas.scene, self.canvas.undo_stack)  # Передаем undo_stack
        # Подключаем сигналы от панели свойств
        self.props_panel.color_changed.connect(self.on_props_color_changed)
        self.props_panel.stroke_width_changed.connect(self.on_props_stroke_width_changed)

        # 3. Собираем всё вместе
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self.props_panel)  # Добавляем панель свойств справа

        print("✓ Интерфейс настроен")

    def on_change_tool(self, tool_name):
        self.current_tool = tool_name
        print(f"Выбран инструмент: {tool_name}")

        # Визуальная логика "Радио-кнопок"
        self.btn_select.setChecked(tool_name == "select")
        self.btn_line.setChecked(tool_name == "line")
        self.btn_rect.setChecked(tool_name == "rect")
        self.btn_ellipse.setChecked(tool_name == "ellipse")

        # Передаем информацию в холст
        self.canvas.set_tool(tool_name, color=self.current_color)

    def on_change_color(self):
        # Открываем диалог выбора цвета
        color = QColorDialog.getColor()

        # Если пользователь выбрал цвет (не нажал Cancel)
        if color.isValid():
            color_name = color.name()
            print(f"Выбран цвет: {color_name}")

            # Сохраняем текущий цвет
            self.current_color = color_name

            # Обновляем визуализатор цвета
            self.color_preview.setStyleSheet(f"""
                QFrame {{
                    background-color: {color_name}; 
                    border: 2px solid #888888;
                    border-radius: 4px;
                }}
            """)

            # Обновляем текст на кнопке
            self.btn_color.setText(f"Цвет: {color_name[1:].upper()}")

            # Передаем выбранный цвет в холст
            self.canvas.set_tool(self.current_tool, color=color_name)

            # Изменяем цвет ВСЕХ выделенных фигур
            self.canvas.change_selected_items_color(color_name)

            # Обновляем статусбар
            self.statusBar().showMessage(f"Текущий цвет: {color_name} (применен к выделенным фигурам)")

    def on_props_color_changed(self, color_name):
        """Обработчик изменения цвета из панели свойств"""
        print(f"Цвет изменен из панели свойств: {color_name}")
        self.current_color = color_name

        # Обновляем визуализатор цвета
        self.color_preview.setStyleSheet(f"""
            QFrame {{
                background-color: {color_name}; 
                border: 2px solid #888888;
                border-radius: 4px;
            }}
        """)

        # Обновляем текст на кнопке
        self.btn_color.setText(f"Цвет: {color_name[1:].upper()}")

    def on_props_stroke_width_changed(self, width):
        """Обработчик изменения толщины линии из панели свойств"""
        print(f"Толщина линии изменена из панели свойств: {width}")

    def closeEvent(self, event: QCloseEvent):
        # Перехватываем событие закрытия
        print("Попытка закрыть окно...")
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            print("Window Closed: Разрешаем закрытие")
            event.accept()
        else:
            print("Отмена закрытия")
            event.ignore()