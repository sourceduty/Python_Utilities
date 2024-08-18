import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
from PIL import Image, ImageTk, ImageFilter, ImageOps
import random

class PixelArtConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art Converter")

        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.pixelate_button = tk.Button(self.button_frame, text="Convert to Pixel Art", command=self.convert_to_pixel_art)
        self.pixelate_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.button_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.pixelation_level = tk.IntVar(value=32)
        self.pixelation_dropdown = ttk.Combobox(self.button_frame, textvariable=self.pixelation_level, values=[8, 16, 32, 64, 128])
        self.pixelation_dropdown.pack(side=tk.LEFT, padx=5)

        self.camouflage_var = tk.BooleanVar()
        self.delete_pixels_var = tk.BooleanVar()
        self.colorize_var = tk.BooleanVar()

        self.camouflage_check = tk.Checkbutton(self.button_frame, text="Camouflage", variable=self.camouflage_var)
        self.camouflage_check.pack(side=tk.LEFT, padx=5)

        self.delete_pixels_check = tk.Checkbutton(self.button_frame, text="Delete Pixels", variable=self.delete_pixels_var)
        self.delete_pixels_check.pack(side=tk.LEFT, padx=5)

        self.colorize_check = tk.Checkbutton(self.button_frame, text="Colorize", variable=self.colorize_var)
        self.colorize_check.pack(side=tk.LEFT, padx=5)

        self.color_picker_button = tk.Button(self.button_frame, text="Choose Colors", command=self.choose_colors)
        self.color_picker_button.pack(side=tk.LEFT, padx=5)

        self.image = None
        self.original_image = None
        self.pixelated_image = None
        self.color1 = "blue"
        self.color2 = "yellow"

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.image = self.original_image.copy()
            self.display_image(self.image)

    def display_image(self, image):
        resized_image = image.copy()
        resized_image.thumbnail((500, 500), Image.Resampling.LANCZOS)
        self.canvas.image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas.image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def convert_to_pixel_art(self):
        if self.original_image:
            colors = self.pixelation_level.get()
            self.pixelated_image = self.original_image.quantize(colors=colors, method=Image.Quantize.MAXCOVERAGE)

            if self.camouflage_var.get():
                self.pixelated_image = self.camouflage_pixels(self.pixelated_image)

            if self.delete_pixels_var.get():
                self.pixelated_image = self.delete_pixels(self.pixelated_image)

            if self.colorize_var.get():
                self.pixelated_image = self.colorize_image(self.pixelated_image)

            self.display_image(self.pixelated_image)

    def camouflage_pixels(self, image):
        return image.convert("RGB").filter(ImageFilter.GaussianBlur(radius=2))

    def delete_pixels(self, image):
        image = image.convert("RGBA")
        pixels = image.load()
        width, height = image.size
        for x in range(width):
            for y in range(height):
                if random.random() < 0.5:
                    pixels[x, y] = (0, 0, 0, 0)  # Make pixel transparent
        return image

    def colorize_image(self, image):
        return ImageOps.colorize(image.convert("L"), black=self.color1, white=self.color2)

    def choose_colors(self):
        self.color1 = colorchooser.askcolor(title="Choose Color 1")[1]
        self.color2 = colorchooser.askcolor(title="Choose Color 2")[1]

    def save_image(self):
        if self.pixelated_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.pixelated_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtConverter(root)
    root.mainloop()
