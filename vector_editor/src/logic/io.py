from abc import ABC, abstractmethod
import json
import os
from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtCore import QRectF


class SaveStrategy(ABC):
    @abstractmethod
    def save(self, filename: str, scene, items: list):
        """
        :param filename: Путь к файлу
        :param scene: Объект сцены (нужен для рендеринга картинки)
        :param items: Список фигур (нужен для JSON)
        """
        pass


class JsonSaveStrategy(SaveStrategy):
    def save(self, filename, scene, items):
        data = {
            "version": "1.0",
            "canvas_width": scene.width(),
            "canvas_height": scene.height(),
            "shapes": []
        }

        # Собираем данные со всех фигур
        # Используем to_dict(), который мы писали в Модуле 2 и 4
        for item in items:
            # Проверяем, есть ли у предмета метод сериализации
            if hasattr(item, "to_dict"):
                data["shapes"].append(item.to_dict())

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)


class ImageSaveStrategy(SaveStrategy):
    def __init__(self, fmt="PNG"):
        self.fmt = fmt  # PNG, JPG, BMP

    def save(self, filename, scene, items):
        # 1. Создаем пустую картинку размера сцены
        # Format_ARGB32 поддерживает прозрачность
        rect = scene.sceneRect()
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format.Format_ARGB32)
        image.fill(QColor(0, 0, 0, 0))  # Заливаем прозрачным

        # 2. Создаем Художника (Painter), который рисует на картинке
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 3. Просим сцену нарисовать себя на художнике
        # render(painter, target_rect, source_rect)
        scene.render(painter, QRectF(image.rect()), rect)

        # 4. Завершаем рисование и сохраняем файл
        painter.end()
        image.save(filename, self.fmt)


class FileManager:
    """
    Класс отвечает ТОЛЬКО за чтение и запись данных на диск.
    Он не знает про QGraphicsScene. Он работает с Python-словарями.
    """

    @staticmethod
    def save_project(filename: str, data: dict):
        """
        :param filename: Полный путь к файлу
        :param data: Готовый словарь с данными проекта
        """
        try:
            # ensure_ascii=False позволяет сохранять кириллицу нормально
            # indent=4 делает файл читаемым (pretty print)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except OSError as e:
            # Пробрасываем ошибку выше, чтобы UI показал Alert
            raise IOError(f"Не удалось записать файл: {e}")

    @staticmethod
    def load_project(filename: str) -> dict:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл не найден: {filename}")

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Файл поврежден или имеет неверный формат")
        except OSError as e:
            raise IOError(f"Ошибка чтения файла: {e}")