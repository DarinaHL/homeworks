# vector_editor/src/app.py
from PySide6.QtGui import QCloseEvent, QAction
from PySide6.QtWidgets import QMainWindow, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
from src.widgets.canvas import EditorCanvas
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QColorDialog
from PySide6.QtGui import QColor


class VectorEditorWindow(QMainWindow):
    def __init__(self):
        # Обязательный вызов конструктора родителя!
        super().__init__()

        self.setWindowTitle("Vector Editor")
        self.resize(1000, 700)  # Увеличим размер окна для удобства

        # Сначала создаем canvas
        self.canvas = EditorCanvas()
        self.canvas.set_tool("select")

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

        # 3. Создаем Action (Действие)
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Close the application")
        exit_action.triggered.connect(self.close)

        # Добавляем Action в меню
        file_menu.addAction(exit_action)

        # 4. Создаем Тулбар
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.addAction(exit_action)

        # Создаем меню Edit для группировки
        edit_menu = self.menuBar().addMenu("&Edit")

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

        # Добавить разделитель
        edit_menu.addSeparator()

        print("✓ Меню и тулбары созданы")

    def on_group_selection(self):
        """Обработчик для группировки"""
        print("Нажата Shift+G - группировка...")
        self.canvas.group_selection()

    def on_ungroup_selection(self):
        """Обработчик для разгруппировки"""
        print("Нажата Shift+U - разгруппировка...")
        self.canvas.ungroup_selection()


    def _setup_layout(self):
        # 1. Создаем главный контейнер
        container = QWidget()
        self.setCentralWidget(container)

        # 2. Основной лейаут (Горизонтальный: Слева панель, Справа холст)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(5, 5, 5, 5)  # Добавим небольшие отступы

        # --- Левая панель (Палитра инструментов) ---
        tools_panel = QFrame()
        tools_panel.setFixedWidth(150)  # Немного шире
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

        tip_text = QPushButton("1. Выделите фигуры\n2. Нажмите Ctrl+Shift+G")
        tip_text.setEnabled(False)
        tip_text.setStyleSheet("text-align: left; font-size: 10pt; background-color: #f8f8f8;")
        tools_layout.addWidget(tip_text)

        tools_layout.addStretch()  # Пружина, которая прижмет кнопки наверх

        # СВЯЗЫВАЕМ СИГНАЛЫ КНОПОК С МЕТОДАМИ
        self.btn_select.clicked.connect(lambda: self.on_change_tool("select"))
        self.btn_line.clicked.connect(lambda: self.on_change_tool("line"))
        self.btn_rect.clicked.connect(lambda: self.on_change_tool("rect"))
        self.btn_ellipse.clicked.connect(lambda: self.on_change_tool("ellipse"))

        self.btn_color.clicked.connect(self.on_change_color)

        # 3. Собираем всё вместе
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)

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
        self.canvas.set_tool(tool_name)

    def on_change_color(self):
        # Открываем диалог выбора цвета
        color = QColorDialog.getColor()

        # Если пользователь выбрал цвет (не нажал Cancel)
        if color.isValid():
            color_name = color.name()
            print(f"Выбран цвет: {color_name}")

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

            # Обновляем статусбар
            self.statusBar().showMessage(f"Текущий цвет: {color_name}")
        else:
            print("Выбор цвета отменен")

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