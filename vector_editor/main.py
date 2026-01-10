# vector_editor/main.py
import sys
from PySide6.QtWidgets import QApplication
from src.app import VectorEditorWindow


def main():
    app = QApplication(sys.argv)

    # Инициализация и настройка темы оформления (опционально)
    app.setStyle("Fusion")

    # Устанавливаем уникальное имя приложения для избежания конфликтов
    app.setApplicationName("Vector Editor")
    app.setOrganizationName("VectorEditor")
    app.setOrganizationDomain("vectoreditor.example.com")

    window = VectorEditorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()