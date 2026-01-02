import tkinter as tk
from tkinter import ttk, messagebox
from itertools import permutations

# Логика солвера
class Solver:
    def __init__(self, func, part_table):
        '''
        :param func - evalable str with variables x, y, z, w and logic elements "==", "not", "()", "<=", "and", "or":
        example: "(x <= y) and (y or z) or (not w == x)"
        :param part_table: matrix 3 by 4. with lists of ints and Nones, like this:
        [
        [0, 1, None, None, 0],
        [None, 0, 0, 0, 0],
        [0, None, 1, None, 0]
        ]
        '''
        func = func.replace('∨', ' or ').replace('≡', '==').replace('¬', ' not ').replace('∧', ' and ').replace('→',
                                                                                                                '<=')
        self.func = func
        self.part_table = [i for i in part_table]
        self.table = []
        self.table_needed = []

    def create_whole_table(self):
        if self.table:
            return self.table
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    for w in range(2):
                        self.table.append([x, y, z, w, int(eval(self.func))])
        return self.table

    def solve(self):
        indexes = [0, 1, 2, 3]
        if not self.table:
            self.create_whole_table()
        for tble in permutations(self.table, r=3):
            for index in permutations(indexes):
                flag = False
                for i in range(3):
                    for j in range(4):
                        if tble[i][index[j]] != self.part_table[i][j] and self.part_table[i][j] is not None:
                            flag = True
                            break
                    if flag or tble[i][-1] != self.part_table[i][-1]:
                        break
                else:
                    m = [i for i in index]
                    m.append(-1)
                    return index, [[j[i] for i in m] for j in tble]
        return -1

    def new_value(self, func, part_table):
        func = func.replace('∨', ' or ').replace('≡', '==').replace('¬', ' not ').replace('∧', ' and ').replace('→',
                                                                                                                '<=')
        self.func = func
        self.part_table = [i for i in part_table]
        self.table = []
        self.table_needed = []


# Интерфейс на tkinter

class SolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ЕГЭ Информатика №2 Solver")
        self.root.geometry("900x520")

        # Панель ввода
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top_frame, text="Функция (Python синтаксис):", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        self.func_entry = tk.Entry(top_frame, font=("Courier", 12))
        self.func_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.func_entry.insert(0, "(x or y) and not (y == z) and not w")

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Полная таблица истинности
        left_frame = tk.LabelFrame(main_frame, text="Полная таблица истинности", padx=5, pady=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        columns = ("x", "y", "z", "w", "F")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=40, anchor="center")

        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Фрагмент таблицы истинности
        right_frame = tk.LabelFrame(main_frame, text="Фрагмент таблицы (ввод)", padx=5, pady=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.header_labels = []
        headers = ["?", "?", "?", "?", "F"]

        # Заголовки
        for idx, text in enumerate(headers):
            lbl = tk.Label(right_frame, text=text, font=("Arial", 11, "bold"))
            lbl.grid(row=0, column=idx, padx=5, pady=5)
            if idx < 4:
                self.header_labels.append(lbl)

        self.entries = []
        for r in range(3):
            row_entries = []
            for c in range(5):
                entry = tk.Entry(right_frame, width=5, justify="center", font=("Arial", 12))
                entry.grid(row=r + 1, column=c, padx=3, pady=3)
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Нижняя панель
        bottom_frame = tk.Frame(root, pady=15)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        solve_btn = tk.Button(bottom_frame, text="РЕШИТЬ", bg="#4CAF50", fg="white",
                              font=("Arial", 12, "bold"), command=self.run_solver)
        solve_btn.pack(side=tk.LEFT, padx=20)

        tk.Label(bottom_frame, text="Ответ:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.result_var = tk.StringVar()
        result_entry = tk.Entry(bottom_frame, textvariable=self.result_var,
                                font=("Arial", 14, "bold"), fg="blue", state="readonly", width=10)
        result_entry.pack(side=tk.LEFT, padx=10)

    def get_partial_table_data(self):
        """Считывает данные из правой таблицы. Пустые клетки -> None"""
        data = []
        try:
            for row in self.entries:
                row_data = []
                for entry in row:
                    val = entry.get().strip()
                    if val == "":
                        row_data.append(None)
                    elif val in ["0", "1"]:
                        row_data.append(int(val))
                    else:
                        raise ValueError("Вводите только 0 или 1")
                data.append(row_data)
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return None
        return data

    def run_solver(self):
        # Сброс заголовков на "?" перед новым решением
        for lbl in self.header_labels:
            lbl.config(text="?", fg="black")

        func_str = self.func_entry.get()
        part_table = self.get_partial_table_data()

        if part_table is None:
            return

        try:
            solver = Solver(func_str, part_table)

            # Заполняем полную таблицу истинности
            full_table = solver.create_whole_table()
            self.populate_left_table(full_table)

            # Решаем
            result = solver.solve()

            if result == -1:
                self.result_var.set("Нет реш.")
                messagebox.showwarning("Результат", "Решение не найдено. Проверьте функцию или таблицу.")
            else:
                indices, filled_rows = result

                vars_map = ['x', 'y', 'z', 'w']
                answer_str = "".join([vars_map[i] for i in indices])
                self.result_var.set(answer_str)

                # Дозаполняем правую таблицу
                self.update_right_table(filled_rows)

                # Обновляем заголовки
                for i, var_idx in enumerate(indices):
                    letter = vars_map[var_idx]
                    self.header_labels[i].config(text=letter, fg="blue")

        except Exception as e:
            messagebox.showerror("Ошибка выполнения", f"Произошла ошибка:\n{e}\nПроверьте синтаксис функции.")

    def populate_left_table(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            self.tree.insert("", tk.END, values=row)

    def update_right_table(self, filled_rows):
        for r, row_data in enumerate(filled_rows):
            for c, val in enumerate(row_data):
                entry = self.entries[r][c]
                current_val = entry.get()
                if current_val == "":
                    entry.insert(0, str(val))
                    entry.config(fg="red")
                else:
                    entry.config(fg="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = SolverApp(root)
    root.mainloop()