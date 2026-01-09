# test_abstract.py
from src.logic.shapes import Shape, Rectangle


def test_abstract_class():
    print("Тест 1: Попытка создать экземпляр абстрактного класса Shape...")
    try:
        s = Shape()
        print("ОШИБКА: Не должно быть возможности создать Shape напрямую!")
    except TypeError as e:
        print(f"✓ Правильно! Получили ошибку: {e}")

    print("\nТест 2: Создание конкретного класса Rectangle...")
    try:
        rect = Rectangle(10, 10, 100, 50, "blue", 3)  # Добавили толщину линии 3
        print(f"✓ Успешно! Создан прямоугольник типа: {rect.type_name}")
        print(f"  Данные для сохранения: {rect.to_dict()}")
        # Проверяем новую структуру
        if "props" in rect.to_dict():
            print("✓ Структура данных с ключом 'props' - правильно!")
        else:
            print("✗ Ошибка: ожидался ключ 'props'")
    except Exception as e:
        print(f"✗ Ошибка: {e}")


if __name__ == "__main__":
    test_abstract_class()