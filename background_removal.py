import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Used for image loading and manipulation

class ImageProcessorApp:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    def __init__(self, root):
        self.root = root
        self.root.title("Foreground Extractor")
        self.root.geometry("1000x700")  # Set the size of the GUI window

        # Variables to store loaded images
        self.bg_image = None
        self.fg_image = None

        # Title label
        tk.Label(root, text="Foreground Extraction using Background Subtraction",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Buttons to load images and process them
        tk.Button(root, text="📂 Select Background Image", command=self.load_background).pack(pady=5)
        tk.Button(root, text="📂 Select Foreground Image", command=self.load_foreground).pack(pady=5)
        tk.Button(root, text="🚀 Process Images", command=self.process_images).pack(pady=10)

        # Frame to hold the displayed images
        self.image_frame = tk.Frame(root)
        self.image_frame.pack()

        # Dictionary to hold labels for the three output images
        self.labels = {
            "original": tk.Label(self.image_frame, text="Original", compound='top'),
            "mask": tk.Label(self.image_frame, text="Mask", compound='top'),
            "foreground": tk.Label(self.image_frame, text="Foreground", compound='top'),
        }

        # Pack the image display labels side-by-side
        for label in self.labels.values():
            label.pack(side='left', padx=10)

    # Load the background image from file
    def load_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.bg_image = Image.open(file_path).convert("RGB")  # Convert to RGB
            messagebox.showinfo("Background", "✅ Background image loaded.")

    # Load the foreground image from file
    def load_foreground(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.fg_image = Image.open(file_path).convert("RGB")  # Convert to RGB
            messagebox.showinfo("Foreground", "✅ Foreground image loaded.")

    # Process both images to extract foreground
    def process_images(self):
        if self.bg_image is None or self.fg_image is None:
            messagebox.showwarning("Missing Images", "⚠️ Please load both background and foreground images.")
            return

        # Resize background to match the foreground dimensions
        bg_resized = self.bg_image.resize(self.fg_image.size)

        # Convert both images to grayscale using luminance formula
        gray_bg = self.convert_to_grayscale(bg_resized)
        gray_fg = self.convert_to_grayscale(self.fg_image)

        # Create binary mask where the difference is greater than threshold
        mask = self.create_mask(gray_fg, gray_bg, threshold=30)

        # Use the mask to extract the foreground object from the original image
        foreground = self.apply_mask(self.fg_image, mask)

        # Display original, mask, and foreground output
        self.display_image(self.fg_image, self.labels["original"])
        self.display_image(mask.convert("RGB"), self.labels["mask"])
        self.display_image(foreground, self.labels["foreground"])

    # Convert a color image to grayscale using formula: 0.299*R + 0.587*G + 0.114*B
    def convert_to_grayscale(self, image):
        width, height = image.size
        gray_image = Image.new("L", (width, height))  # "L" mode is grayscale
        pixels = gray_image.load()

        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                pixels[x, y] = gray

        return gray_image

    # Create binary mask where the pixel difference between foreground and background is significant
    def create_mask(self, fg_gray, bg_gray, threshold):
        width, height = fg_gray.size
        mask = Image.new("L", (width, height))
        pixels_fg = fg_gray.load()
        pixels_bg = bg_gray.load()
        pixels_mask = mask.load()

        for x in range(width):
            for y in range(height):
                diff = abs(pixels_fg[x, y] - pixels_bg[x, y])
                pixels_mask[x, y] = 255 if diff > threshold else 0  # Binary mask

        return mask

    # Apply binary mask to original image: show pixel if mask is 255, else black
    def apply_mask(self, original_image, mask):
        width, height = original_image.size
        result = Image.new("RGB", (width, height))
        pixels_original = original_image.load()
        pixels_mask = mask.load()
        pixels_result = result.load()

        for x in range(width):
            for y in range(height):
                if pixels_mask[x, y] == 255:
                    pixels_result[x, y] = pixels_original[x, y]  # Keep pixel
                else:
                    pixels_result[x, y] = (0, 0, 0)  # Black out background

        return result

    # Display PIL image on the tkinter label
    def display_image(self, image, label_widget):
        image_resized = image.resize((300, 300))  # Resize for display
        img_tk = ImageTk.PhotoImage(image_resized)
        label_widget.configure(image=img_tk)
        label_widget.image = img_tk  # Reference to avoid image disappearing

# Create and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
