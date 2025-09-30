import tkinter as tk

class DynamicColorChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("HEX Color Changer")
        self.root.geometry("300x260")
        self.current_color = "#1CB594"
        self.create_widgets()
    
    def create_widgets(self):
        self.color_display = tk.Label(self.root, text="Colour", 
                                     bg=self.current_color, fg="#02021A",
                                     font=("Arial italics", 11), width=20, height=5, anchor="nw")
        self.color_display.pack(pady=20, padx=20)
        hex_frame = tk.Frame(self.root)
        hex_frame.pack(pady=10)
        tk.Label(hex_frame, text="HEX code:").pack(side="left")
        self.hex_entry = tk.Entry(hex_frame, width=10)
        self.hex_entry.insert(0, self.current_color)
        self.hex_entry.pack(side="left", padx=5)
        self.hex_entry.bind("<KeyRelease>", self.update_color)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        colors = [("#AD1313", "Red"), ("#18AF70", "Green"), 
                 ("#5091E6", "Blue"), ("#FFF08E", "Yellow")]
        for hex_color, name in colors:
            btn = tk.Button(button_frame, text=name, bg=hex_color,
                           command=lambda h=hex_color: self.set_color(h))
            btn.pack(side="left", padx=5)
    
    def update_color(self, event=None):
        hex_code = self.hex_entry.get()
        if len(hex_code) == 7 and hex_code.startswith("#"):
            try:
                self.color_display.config(bg=hex_code)
                self.current_color = hex_code
            except:
                pass
    
    def set_color(self, hex_color):
        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, hex_color)
        self.update_color()


class Draw(DynamicColorChanger):
    def __init__(self, root):
        super().__init__(root)
        self.root.title("Place for Drawing")
        self.root.geometry("600x600")
        self.current_color = "#1CB594"
        
        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.line_start = None
        self.line_end = None

        #self.canvas.bind("<Button-1>", self.make_point)
        self.canvas.bind("<Button-3>", self.make_line)
    
    def make_point(self, event):
        x, y = event.x, event.y
        radius = 5
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                               fill=self.current_color, outline=self.current_color)
    
    def make_line(self, event):
        x, y = event.x, event.y
        if self.line_start is None:
            self.line_start = (x, y)
        else:
            self.line_end = (x, y)
            self.canvas.create_line(self.line_start[0], self.line_start[1],
                                   self.line_end[0], self.line_end[1],
                                   fill=self.current_color, width=2)
            
            self.line_start = None
            self.line_end = None

class DrawFigures(Draw):
    def __init__(self, root):
        super().__init__(root)
        self.root.title("Drawing with Keyboard")
        
        self.figure_mode = False
        self.last_point = None
        self.cursor_visible = False
        self.cursor_id = None
        
        self.root.bind("<Double-Button-1>", self.toggle_figure_mode)
        self.root.bind("<KeyPress-Up>", self.move_up)
        self.root.bind("<KeyPress-Down>", self.move_down)
        self.root.bind("<KeyPress-Left>", self.move_left)
        self.root.bind("<KeyPress-Right>", self.move_right)
        
        self.instruction = self.canvas.create_text(300, 20, 
                                                  text="2 раза ЛКМ - начало рисования фигур, 1 раз ЛКМ - точка, ПКМ - линии", 
                                                  font=("Arial", 12))
    
    def toggle_figure_mode(self, event):
        if not self.figure_mode:
            self.figure_mode = True
            self.last_point = (event.x, event.y) 
            self.show_cursor(self.last_point[0], self.last_point[1])
            self.canvas.itemconfig(self.instruction, 
                                  text="2 раза ЛКМ - стоп рисования фигур")
        else:
            self.figure_mode = False
            self.hide_cursor()
            self.last_point = None
            self.canvas.itemconfig(self.instruction, 
                                  text="2 раза ЛКМ - начало рисования фигур, 1 раз ЛКМ - точка, ПКМ - линии")
    
    def show_cursor(self, x, y):
        if self.cursor_id:
            self.canvas.delete(self.cursor_id)
        
        radius = 3
        self.cursor_id = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                                                fill="red", outline="red")
        self.cursor_visible = True
    
    def hide_cursor(self):
        if self.cursor_id:
            self.canvas.delete(self.cursor_id)
            self.cursor_id = None
        self.cursor_visible = False
    
    def move_and_draw(self, dx, dy):
        if not self.figure_mode or not self.last_point:
            return
        
        x, y = self.last_point
        new_x, new_y = x + dx, y + dy
        
        if 0 <= new_x <= 600 and 0 <= new_y <= 600:
            self.canvas.create_line(x, y, new_x, new_y, 
                                   fill=self.current_color, width=5)
            
            self.last_point = (new_x, new_y)
            self.show_cursor(new_x, new_y)
    
    def move_up(self, event):
        self.move_and_draw(0, -5)
    
    def move_down(self, event):
        self.move_and_draw(0, 5)
    
    def move_left(self, event):
        self.move_and_draw(-5, 0)
    
    def move_right(self, event):
        self.move_and_draw(5, 0)
    
    def make_point(self, event):
        if not self.figure_mode:
            super().make_point(event)
    
    def make_line(self, event):
        if not self.figure_mode:
            super().make_line(event)


if __name__ == "__main__":
    root2 = tk.Tk()
    app2 = DrawFigures(root2)
    root2.mainloop()