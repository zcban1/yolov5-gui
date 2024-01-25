import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, BooleanVar, ttk
import subprocess
import os

class YOLOTrainingGUI:
    def __init__(self, master):
        self.master = master
        master.title("YOLOv5 Training GUI")

        self.data_file_path = tk.StringVar()
        self.weights_file_path = tk.StringVar()
        self.img_size = tk.StringVar()
        self.batch_size = tk.StringVar()
        self.epochs = tk.StringVar()
        self.selected_workers = tk.StringVar()
        self.cache_ram_var = tk.BooleanVar()
        self.cache_disk_var = tk.BooleanVar()
        self.selected_model = tk.StringVar()
        self.no_val_var = tk.BooleanVar()

        # Set default values
        self.data_file_path.set("data.yaml")
        self.weights_file_path.set(None)
        self.batch_size.set("44")
        self.epochs.set("100")
        self.workers_values = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.selected_workers.set(self.workers_values[-1])  # Set the last value as default
        self.cache_ram_var.set(False)
        self.cache_disk_var.set(False)
        self.models = ["yolov5s.yaml", "yolov5n.yaml", "yolov5m.yaml", "yolov5l.yaml", "yolov5x.yaml"]
        self.selected_model.set(self.models[0])  # Set the first model as default
        self.no_val_var.set(False)
        self.img_size.set("640")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Configuration file data.yaml:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.data_file_path, width=50).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.master, text="Browse", command=self.browse_data_file).grid(row=0, column=2, pady=5)

        tk.Label(self.master, text="Initial weights file (empty for training from scratch):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.weights_file_path, width=50).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.master, text="Browse", command=self.browse_weights_file).grid(row=1, column=2, pady=5)

        tk.Label(self.master, text="Batch Size (default: -1):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.batch_size, width=10).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Epochs (default: 300):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.epochs, width=10).grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Image Size (default: 640):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self.master, textvariable=self.img_size, width=10).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Workers (default: 8):").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        tk.OptionMenu(self.master, self.selected_workers, *self.workers_values).grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Cache Option:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        tk.Checkbutton(self.master, text="Cache RAM", variable=self.cache_ram_var).grid(row=6, column=1, padx=10, pady=5)
        tk.Checkbutton(self.master, text="Cache Disk", variable=self.cache_disk_var).grid(row=6, column=2, padx=10, pady=5)

        tk.Label(self.master, text="No Validation Set (default: False):").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        tk.Checkbutton(self.master, text="No Validation", variable=self.no_val_var.set).grid(row=7, column=1, padx=10, pady=5)

        tk.Label(self.master, text="YOLO Model:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        tk.OptionMenu(self.master, self.selected_model, *self.models).grid(row=8, column=1, padx=10, pady=5)

        tk.Button(self.master, text="Start Training", command=self.start_training).grid(row=9, column=0, columnspan=3, pady=10)


    def browse_data_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml")])
        if file_path:
            self.data_file_path.set(file_path)

    def browse_weights_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Weight files", "*.pt")])
        if file_path:
            #self.weights_file_path.set(file_path)
            filename = os.path.basename(file_path)
            self.weights_file_path.set(filename)

    def start_training(self):
        # Ottieni il percorso assoluto del file export.py
        current_directory = os.path.dirname(os.path.abspath(__file__))
        #export_py_path = os.path.join(current_directory, "export.py")
        train_py_path = os.path.join(current_directory, "YOLOv5", "train.py")

        data_path = self.data_file_path.get()
        weights_path = self.weights_file_path.get()
        batch_size = self.batch_size.get()
        epochs = self.epochs.get()
        workers = self.selected_workers.get()
        cache_option = ""
        no_val_option = ""

        # Add the --cache option if at least one of the checkboxes is checked
        if self.cache_ram_var.get():
            cache_option = "--cache ram"
        elif self.cache_disk_var.get():
            cache_option = "--cache disk"

        # Check if a weights file is selected
        if weights_path is not None:
            weights_option = "--weights {weights_path}"
        else:
            weights_option = ""

        if self.no_val_var.get():
            no_val_option = "--noval "

        
        command = f"python {train_py_path} --img {self.img_size.get()} --data {data_path} {weights_option}  --cfg {self.selected_model.get()} --batch-size {batch_size} --epoch {epochs} --workers {workers} {cache_option}{no_val_option} "
        messagebox.showinfo("Comando", f"Comando: {command}")

        
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            tk.messagebox.showerror("Error", f"An error occurred during training:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YOLOTrainingGUI(root)
    root.mainloop()
