# vector_editor/src/logic/commands.py
from PySide6.QtGui import QUndoCommand
from PySide6.QtCore import QPointF


class AddShapeCommand(QUndoCommand):
    """Команда добавления фигуры на сцену"""

    def __init__(self, scene, item):
        super().__init__()
        self.scene = scene
        self.item = item

        # Определяем тип фигуры для отображения в истории
        shape_type = "Unknown"
        if hasattr(item, 'type_name'):
            shape_type = item.type_name
            if shape_type == "rect":
                shape_type = "Прямоугольник"
            elif shape_type == "line":
                shape_type = "Линия"
            elif shape_type == "ellipse":
                shape_type = "Эллипс"
            elif shape_type == "group":
                shape_type = "Группа"

        self.setText(f"Добавить {shape_type}")

    def redo(self):
        """Выполнение команды (добавление фигуры)"""
        # Проверяем, не добавлена ли фигура уже на сцену
        if self.item.scene() is None:
            self.scene.addItem(self.item)

    def undo(self):
        """Отмена команды (удаление фигуры)"""
        # Проверяем, что фигура на сцене
        if self.item.scene() is not None:
            self.scene.removeItem(self.item)


class MoveCommand(QUndoCommand):
    """Команда перемещения фигуры"""

    def __init__(self, item, old_pos, new_pos):
        super().__init__()
        self.item = item
        self.old_pos = old_pos
        self.new_pos = new_pos
        self.setText(f"Переместить {self._get_item_name()}")

    def _get_item_name(self):
        """Получаем имя объекта для отображения в истории"""
        if hasattr(self.item, 'type_name'):
            type_name = self.item.type_name
            if type_name == "rect":
                return "прямоугольник"
            elif type_name == "line":
                return "линию"
            elif type_name == "ellipse":
                return "эллипс"
            elif type_name == "group":
                return "группу"
        return "объект"

    def redo(self):
        """Выполнение команды (перемещение в новую позицию)"""
        self.item.setPos(self.new_pos)

    def undo(self):
        """Отмена команды (возврат в старую позицию)"""
        self.item.setPos(self.old_pos)


class MoveMultipleCommand(QUndoCommand):
    """Команда перемещения нескольких фигур одновременно"""

    def __init__(self, items, old_positions, new_positions):
        super().__init__()
        self.items = items
        self.old_positions = old_positions
        self.new_positions = new_positions

        if len(items) == 1:
            self.setText(f"Переместить {self._get_item_name(items[0])}")
        else:
            self.setText(f"Переместить {len(items)} объектов")

    def _get_item_name(self, item):
        """Получаем имя объекта для отображения в истории"""
        if hasattr(item, 'type_name'):
            type_name = item.type_name
            if type_name == "rect":
                return "прямоугольник"
            elif type_name == "line":
                return "линию"
            elif type_name == "ellipse":
                return "эллипс"
            elif type_name == "group":
                return "группу"
        return "объект"

    def redo(self):
        """Выполнение команды (перемещение всех объектов)"""
        for i, item in enumerate(self.items):
            if i < len(self.new_positions):
                item.setPos(self.new_positions[i])

    def undo(self):
        """Отмена команды (возврат всех объектов в старые позиции)"""
        for i, item in enumerate(self.items):
            if i < len(self.old_positions):
                item.setPos(self.old_positions[i])


class DeleteCommand(QUndoCommand):
    """Команда удаления фигуры"""

    def __init__(self, scene, item):
        super().__init__()
        self.scene = scene
        self.item = item
        self.setText(f"Удалить {self._get_item_name()}")

    def _get_item_name(self):
        """Получаем имя объекта для отображения в истории"""
        if hasattr(self.item, 'type_name'):
            type_name = self.item.type_name
            if type_name == "rect":
                return "прямоугольник"
            elif type_name == "line":
                return "линию"
            elif type_name == "ellipse":
                return "эллипс"
            elif type_name == "group":
                return "группу"
        return "объект"

    def redo(self):
        """Выполнение команды (удаление фигуры)"""
        if self.item.scene() is not None:
            self.scene.removeItem(self.item)

    def undo(self):
        """Отмена команды (восстановление фигуры)"""
        if self.item.scene() is None:
            self.scene.addItem(self.item)


class DeleteMultipleCommand(QUndoCommand):
    """Команда удаления нескольких фигур"""

    def __init__(self, scene, items):
        super().__init__()
        self.scene = scene
        self.items = items

        if len(items) == 1:
            self.setText(f"Удалить {self._get_item_name(items[0])}")
        else:
            self.setText(f"Удалить {len(items)} объектов")

    def _get_item_name(self, item):
        """Получаем имя объекта для отображения в истории"""
        if hasattr(item, 'type_name'):
            type_name = item.type_name
            if type_name == "rect":
                return "прямоугольник"
            elif type_name == "line":
                return "линию"
            elif type_name == "ellipse":
                return "эллипс"
            elif type_name == "group":
                return "группу"
        return "объект"

    def redo(self):
        """Выполнение команды (удаление всех объектов)"""
        for item in self.items:
            if item.scene() is not None:
                self.scene.removeItem(item)

    def undo(self):
        """Отмена команды (восстановление всех объектов)"""
        for item in self.items:
            if item.scene() is None:
                self.scene.addItem(item)


class ChangeColorCommand(QUndoCommand):
    """Команда изменения цвета фигуры"""

    def __init__(self, item, new_color, old_color=None):
        super().__init__()
        self.item = item
        self.new_color = new_color

        # Если старая позиция не передана, получаем ее из объекта
        if old_color is None and hasattr(item, 'pen'):
            self.old_color = item.pen().color().name()
        else:
            self.old_color = old_color

        self.setText(f"Изменить цвет {self._get_item_name()}")

    def _get_item_name(self):
        """Получаем имя объекта для отображения в истории"""
        if hasattr(self.item, 'type_name'):
            type_name = self.item.type_name
            if type_name == "rect":
                return "прямоугольника"
            elif type_name == "line":
                return "линии"
            elif type_name == "ellipse":
                return "эллипса"
            elif type_name == "group":
                return "группы"
        return "объекта"

    def redo(self):
        """Выполнение команды (изменение цвета)"""
        if hasattr(self.item, "set_active_color"):
            self.item.set_active_color(self.new_color)

    def undo(self):
        """Отмена команды (возврат старого цвета)"""
        if hasattr(self.item, "set_active_color"):
            self.item.set_active_color(self.old_color)


class ChangeColorMultipleCommand(QUndoCommand):
    """Команда изменения цвета нескольких фигур"""

    def __init__(self, items, new_color, old_colors=None):
        super().__init__()
        self.items = items
        self.new_color = new_color

        # Сохраняем старые цвета
        self.old_colors = []
        if old_colors is None:
            for item in items:
                if hasattr(item, 'pen'):
                    self.old_colors.append(item.pen().color().name())
                else:
                    self.old_colors.append("#000000")
        else:
            self.old_colors = old_colors

        if len(items) == 1:
            self.setText(f"Изменить цвет {self._get_item_name(items[0])}")
        else:
            self.setText(f"Изменить цвет {len(items)} объектов")

    def _get_item_name(self, item):
        """Получаем имя объекта для отображения в истории"""
        if hasattr(item, 'type_name'):
            type_name = item.type_name
            if type_name == "rect":
                return "прямоугольника"
            elif type_name == "line":
                return "линии"
            elif type_name == "ellipse":
                return "эллипса"
            elif type_name == "group":
                return "группы"
        return "объекта"

    def redo(self):
        """Выполнение команды (изменение цвета всех объектов)"""
        for item in self.items:
            if hasattr(item, "set_active_color"):
                item.set_active_color(self.new_color)

    def undo(self):
        """Отмена команды (возврат старых цветов)"""
        for i, item in enumerate(self.items):
            if hasattr(item, "set_active_color") and i < len(self.old_colors):
                item.set_active_color(self.old_colors[i])


class ChangeWidthCommand(QUndoCommand):
    """Команда изменения толщины линии"""

    def __init__(self, item, new_width, old_width=None):
        super().__init__()
        self.item = item
        self.new_width = new_width

        # Если старая толщина не передана, получаем ее из объекта
        if old_width is None and hasattr(item, 'pen'):
            self.old_width = item.pen().width()
        else:
            self.old_width = old_width

        self.setText(f"Изменить толщину {self._get_item_name()}")

    def _get_item_name(self):
        """Получаем имя объекта для отображения в истории"""
        if hasattr(self.item, 'type_name'):
            type_name = self.item.type_name
            if type_name == "rect":
                return "прямоугольника"
            elif type_name == "line":
                return "линии"
            elif type_name == "ellipse":
                return "эллипса"
            elif type_name == "group":
                return "группы"
        return "объекта"

    def redo(self):
        """Выполнение команды (изменение толщины)"""
        if hasattr(self.item, "set_stroke_width"):
            self.item.set_stroke_width(self.new_width)
        elif hasattr(self.item, "pen"):
            pen = self.item.pen()
            pen.setWidth(self.new_width)
            self.item.setPen(pen)

    def undo(self):
        """Отмена команды (возврат старой толщины)"""
        if hasattr(self.item, "set_stroke_width"):
            self.item.set_stroke_width(self.old_width)
        elif hasattr(self.item, "pen"):
            pen = self.item.pen()
            pen.setWidth(self.old_width)
            self.item.setPen(pen)


class ChangeWidthMultipleCommand(QUndoCommand):
    """Команда изменения толщины нескольких фигур"""

    def __init__(self, items, new_width, old_widths=None):
        super().__init__()
        self.items = items
        self.new_width = new_width

        # Сохраняем старые толщины
        self.old_widths = []
        if old_widths is None:
            for item in items:
                if hasattr(item, 'pen'):
                    self.old_widths.append(item.pen().width())
                else:
                    self.old_widths.append(2)
        else:
            self.old_widths = old_widths

        if len(items) == 1:
            self.setText(f"Изменить толщину {self._get_item_name(items[0])}")
        else:
            self.setText(f"Изменить толщину {len(items)} объектов")

    def _get_item_name(self, item):
        """Получаем имя объекта для отображения в истории"""
        if hasattr(item, 'type_name'):
            type_name = item.type_name
            if type_name == "rect":
                return "прямоугольника"
            elif type_name == "line":
                return "линии"
            elif type_name == "ellipse":
                return "эллипса"
            elif type_name == "group":
                return "группы"
        return "объекта"

    def redo(self):
        """Выполнение команды (изменение толщины всех объектов)"""
        for item in self.items:
            if hasattr(item, "set_stroke_width"):
                item.set_stroke_width(self.new_width)
            elif hasattr(item, "pen"):
                pen = item.pen()
                pen.setWidth(self.new_width)
                item.setPen(pen)

    def undo(self):
        """Отмена команды (возврат старых толщин)"""
        for i, item in enumerate(self.items):
            if i < len(self.old_widths):
                if hasattr(item, "set_stroke_width"):
                    item.set_stroke_width(self.old_widths[i])
                elif hasattr(item, "pen"):
                    pen = item.pen()
                    pen.setWidth(self.old_widths[i])
                    item.setPen(pen)



class GroupCommand(QUndoCommand):
    """Команда группировки фигур"""

    def __init__(self, canvas, items):
        super().__init__()
        self.canvas = canvas
        self.items = items
        self.group = None
        self.setText(f"Сгруппировать {len(items)} объектов")

    def redo(self):
        """Создание группы"""
        if not self.group:
            # Создаем новую группу
            self.group = Group(0, 0)
            self.canvas.scene.addItem(self.group)

            # Добавляем все элементы в группу
            for item in self.items:
                item.setSelected(False)
                item_pos = item.scenePos()
                item.setPos(item_pos)
                self.group.addToGroup(item)

        self.group.setSelected(True)

    def undo(self):
        """Разгруппировка"""
        if self.group:
            children = list(self.group.childItems())
            for child in children:
                self.group.removeFromGroup(child)
                child.setPos(child.scenePos())
                child.setSelected(True)
            self.canvas.scene.removeItem(self.group)


class UngroupCommand(QUndoCommand):
    """Команда разгруппировки"""

    def __init__(self, canvas, group):
        super().__init__()
        self.canvas = canvas
        self.group = group
        self.children = []
        self.setText("Разгруппировать")

    def redo(self):
        """Разгруппировка"""
        if not self.children:
            self.children = list(self.group.childItems())

        for child in self.children:
            self.group.removeFromGroup(child)
            child.setPos(child.scenePos())
            child.setSelected(True)
        self.canvas.scene.removeItem(self.group)

    def undo(self):
        """Восстановление группы"""
        self.canvas.scene.addItem(self.group)
        for child in self.children:
            child.setSelected(False)
            child.setPos(child.pos())
            self.group.addToGroup(child)
        self.group.setSelected(True)