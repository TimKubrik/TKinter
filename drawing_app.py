import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox,simpledialog
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")
        self.pen_color = 'black'

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.color_preview = tk.Label(root, width=5, height=2, bg='black')
        self.color_preview.pack(side=tk.RIGHT)
        self.update_color_preview()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.update_color_preview()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)

        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        resize_button = tk.Button(control_frame, text="Resize", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        self.sizes = [1, 2, 5, 10]
        self.current_size = tk.StringVar()
        self.current_size.set(str(self.sizes[0]))

        self.size_menu = tk.OptionMenu(self.root, self.current_size, *map(str, self.sizes), command=self.update_brush_size)
        self.size_menu.pack(side=tk.LEFT)

    def update_brush_size(self, value):
        self.brush_size_scale.set(int(value))

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=self.brush_size_scale.get(), fill=self.pen_color, capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color, width=self.brush_size_scale.get())
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        self.previous_color = self.pen_color
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_color_preview()

    def use_eraser(self):
        self.previous_color = self.pen_color
        self.pen_color = "white"
        self.update_color_preview()

    def pick_color(self, event):
        x, y = event.x, event.y
        self.pen_color = self.image.getpixel((x, y))
        self.previous_color = self.pen_color
        self.update_color_preview()

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_color_preview(self):
        self.color_preview.config(bg=self.pen_color)

    def resize_canvas(self):
        new_width = simpledialog.askinteger("Изменение размера холста", "Введите новую ширину:")
        new_height = simpledialog.askinteger("Изменение размера холста", "Введите новую высоту:")
        if new_width and new_height:
            self.canvas.config(width=new_width, height=new_height)
            self.image = Image.new("RGB", (new_width, new_height), "white")
            self.draw = ImageDraw.Draw(self.image)


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()