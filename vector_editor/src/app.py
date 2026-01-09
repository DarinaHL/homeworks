
# vector_editor/src/app.py
from PySide6.QtGui import QCloseEvent, QAction
from PySide6.QtWidgets import QMainWindow, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
from src.widgets.canvas import EditorCanvas

from PySide6.QtWidgets import QColorDialog
from PySide6.QtGui import QColor

class VectorEditorWindow(QMainWindow):
    def __init__(self):
        # Обязательный вызов конструктора родителя!
        # Без этого Qt-объект не будет создан в памяти C++
        super().__init__()

        self.setWindowTitle("Vector Editor")
        self.resize(800, 600)  # Начальный размер

        # Хороший тон: выносить настройку UI в отдельный метод
        self._init_ui()
        self._setup_layout()

    def _init_ui(self):
        # 1. Создаем строку состояния
        self.statusBar().showMessage("Готов к работе")

        # 2. Создаем Меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")  # Амперсанд позволяет открывать меню через Alt+F

        # 3. Создаем Action (Действие)
        # Важно: Action не имеет визуального представления сам по себе,
        # он привязывается к меню или тулбару.
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Close the application")
        # connect - связываем сигнал с методом close() окна
        exit_action.triggered.connect(self.close)

        # Добавляем Action в меню
        file_menu.addAction(exit_action)

        # 4. Создаем Тулбар
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.addAction(exit_action)  # Тот же самый экшен!

    def _setup_layout(self):
        # 1. Создаем главный контейнер
        container = QWidget()
        self.setCentralWidget(container)

        # 2. Основной лейаут (Горизонтальный: Слева панель, Справа холст)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы от краев окна

        # --- Левая панель (Палитра инструментов) ---
        tools_panel = QFrame()
        tools_panel.setFixedWidth(120)  # Фиксируем ширину
        tools_panel.setStyleSheet("background-color: #f0f0f0;")  # Временный цвет для наглядности

        # Внутри панели кнопки идут вертикально
        tools_layout = QVBoxLayout(tools_panel)

        # Создаем кнопки инструментов
        self.btn_select = QPushButton("Select")  # Новая кнопка
        self.btn_line = QPushButton("Line")
        self.btn_rect = QPushButton("Rect")
        self.btn_ellipse = QPushButton("Ellipse")
        self.btn_color = QPushButton("Выбор цвета")

        # Делаем кнопки "залипающими" (Checkable) - как RadioButtons
        self.btn_select.setCheckable(True)  # ДОБАВИТЬ
        self.btn_line.setCheckable(True)
        self.btn_rect.setCheckable(True)
        self.btn_ellipse.setCheckable(True)

        # По умолчанию активен инструмент Select
        self.btn_line.setChecked(True)
        self.current_tool = "select"

        # Добавляем кнопки на панель
        tools_layout.addWidget(self.btn_select)  # ДОБАВИТЬ первой
        tools_layout.addWidget(self.btn_line)
        tools_layout.addWidget(self.btn_rect)
        tools_layout.addWidget(self.btn_ellipse)
        tools_layout.addWidget(self.btn_color)

        self.color_preview = QFrame()
        self.color_preview.setFixedHeight(30)
        self.color_preview.setStyleSheet("background-color: black; border: 1px solid #888;")
        tools_layout.addWidget(self.color_preview)

        tools_layout.addStretch()  # Пружина, которая прижмет кнопки наверх



        # Создаем холст
        self.canvas = EditorCanvas()

        # СВЯЗЫВАЕМ СИГНАЛЫ КНОПОК С МЕТОДАМИ
        self.btn_select.clicked.connect(lambda: self.on_change_tool("select"))
        self.btn_line.clicked.connect(lambda: self.on_change_tool("line"))
        self.btn_rect.clicked.connect(lambda: self.on_change_tool("rect"))
        self.btn_ellipse.clicked.connect(lambda: self.on_change_tool("ellipse"))

        self.btn_color.clicked.connect(self.on_change_color)

        # 3. Собираем всё вместе
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)
        # canvas займет всё свободное место

    def on_change_tool(self, tool_name):
        self.current_tool = tool_name
        print(f"Выбран инструмент: {tool_name}")

        # Визуальная логика "Радио-кнопок"
        # Если выбрали один инструмент, отжимаем все остальные
        self.btn_select.setChecked(tool_name == "select")  # ДОБАВИТЬ
        self.btn_line.setChecked(tool_name == "line")
        self.btn_rect.setChecked(tool_name == "rect")
        self.btn_ellipse.setChecked(tool_name == "ellipse")

        # Передаем информацию в холст (он тоже должен знать, чем мы рисуем)
        self.canvas.set_tool(tool_name)

    #ДОБАВИЛА
    def on_change_color(self):
        # Открываем диалог выбора цвета
        color = QColorDialog.getColor()

        # Если пользователь выбрал цвет (не нажал Cancel)
        if color.isValid():
            # Получаем имя цвета в формате "#RRGGBB"
            color_name = color.name()
            print(f"Выбран цвет: {color_name}")

            # Обновляем визуализатор цвета
            self.color_preview.setStyleSheet(f"background-color: {color_name}; border: 1px solid #888;")

            # Обновляем текст на кнопке (опционально)
            self.btn_color.setText(f"Цвет: {color_name}")

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
            event.accept()  # Говорим Qt: "Закрывай"
        else:
            print("Отмена закрытия")
            event.ignore()  # Говорим Qt: "Игнорируй крестик"