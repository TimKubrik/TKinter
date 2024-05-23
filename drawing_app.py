import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        # Установка титула окна
        self.root.title("Рисовалка с сохранением в PNG")

        # Создание изображения с белым фоном
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создание холста с белым фоном
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        # Добавление холста
        self.canvas.pack()

        # Установка интерфейса
        self.setup_ui()

        # Переменные для хранения координат мыши
        self.last_x, self.last_y = None, None

        # Переменные для хранения цвета пера
        self.pen_color = 'black'

        # Привязка событий к холсту вызывает методы paint, reset,pick_color
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)  # Привязка события правой кнопки мыши

    def setup_ui(self):
        # Создается рамка для кнопок и шкалы размера кисти
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)
        # Создание кнопок
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)
        # Создается щкала размера кисти и ориентацией по горизонтали
        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)
        # Добавление размеров кисти в список
        self.sizes = [1, 2, 5, 10]
        self.current_size = tk.StringVar()
        self.current_size.set(str(self.sizes[0]))  # Установка начального размера кисти

        # Создание выпадающего списка с размерами кисти
        self.size_menu = tk.OptionMenu(self.root, self.current_size, *map(str, self.sizes),
                                       command=self.update_brush_size)
        self.size_menu.pack(side=tk.LEFT)

    def update_brush_size(self, value):
        # Обновление текущего размера кисти при выборе значения из списка
        self.brush_size_scale.set(int(value))

    def paint(self, event):
        # Рисует линию на холсте и на изображении
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())
        # Координаты начала и конца линии
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        # сбрасывает координаты начала и конца линии
        self.last_x, self.last_y = None, None

    # удаляет все элементы на холсте с помощью метода delete, а затем создает новое изображение с белым фоном
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    # открывает диалоговое окно для выбора цвета и сохраняет выбранный цвет в переменной pen_color.
    def choose_color(self):
        self.previous_color = self.pen_color  # Сохранение предыдущего цвета
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def use_eraser(self):
        # Устанавливает цвет пера в цвет фона ("white") для использования в качестве ластика
        self.previous_color = self.pen_color  # Сохранение предыдущего цвета
        self.pen_color = "white"

    def pick_color(self, event):
        # Получение цвета пикселя под курсором мыши и установка его как текущего цвета пера
        x, y = event.x, event.y
        self.pen_color = self.image.getpixel((x, y))
        self.previous_color = self.pen_color

    # Открывает диалоговое окно для выбора файла и сохраняет изображение в выбранный файл в формате PNG
    # Если файл не имеет расширения .png, то оно добавляется автоматически.
    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
