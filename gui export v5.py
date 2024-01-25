import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, BooleanVar, ttk
import subprocess
import os



class YOLOv5ExporterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("YOLOv5 Model Exporter")



        # Variabili per i parametri con valori predefiniti
        self.weights_file = StringVar()
        self.img_size_options = [str(size) for size in range(320, 1344, 32)]  # Opzioni per la dimensione dell'immagine
        self.img_size = StringVar(value=self.img_size_options[0])  # Valore predefinito: 320
        self.device_options = ["0", "cpu"]  # Opzioni disponibili per il dispositivo
        self.device = StringVar(value=self.device_options[0])  # Valore predefinito: 0
        self.include_options = ["onnx", "openvino", "engine", "coreml", "saved_model", "pb", "tflite", "edgetpu", "tfjs", "paddle", "torchscript"]
        self.include_option = StringVar(value="engine")  # Valore predefinito: engine
        self.half_option = BooleanVar()

        # Etichette e Entry per i parametri
        self.create_parameter_entry("Percorso del file weights (.pt):", self.weights_file)
        # Pulsante Sfoglia
        self.browse_button = tk.Button(master, text="Sfoglia", command=self.browse_weights_file)
        self.browse_button.pack(pady=10)

        self.create_parameter_entry_with_combobox("Dimensione dell'immagine:", self.img_size, self.img_size_options)
        self.create_parameter_entry_with_combobox("Dispositivo:", self.device, self.device_options)

        # Combobox per l'opzione include
        self.include_label = tk.Label(self.master, text="Opzione include:")
        self.include_label.pack(pady=5)
        self.include_combobox = ttk.Combobox(self.master, values=self.include_options, textvariable=self.include_option)
        self.include_combobox.set("engine")  # Imposta il valore predefinito
        self.include_combobox.pack(pady=5)

        # Checkbutton per l'opzione half
        self.half_checkbutton = tk.Checkbutton(master, text="check it for FP16", variable=self.half_option)
        self.half_checkbutton.pack(pady=10)



        # Pulsante Esporta
        self.export_button = tk.Button(master, text="Esporta Modello", command=self.export_model)
        self.export_button.pack(pady=20)

    def create_parameter_entry(self, label_text, variable):
        label = tk.Label(self.master, text=label_text)
        label.pack(pady=5)
        entry = tk.Entry(self.master, textvariable=variable)
        entry.pack(pady=5)

    def create_parameter_entry_with_combobox(self, label_text, variable, options):
        label = tk.Label(self.master, text=label_text)
        label.pack(pady=5)
        combobox = ttk.Combobox(self.master, values=options, textvariable=variable)
        combobox.pack(pady=5)

    def browse_weights_file(self):
        file_selected = filedialog.askopenfilename(filetypes=[("Weights files", "*.pt")])
        if file_selected:
            self.weights_file.set(file_selected)
            ### Estrai solo il nome del file con estensione
            #filename = os.path.basename(file_selected)
            #self.weights_file.set(filename)

    def export_model(self):
        # Ottieni il percorso assoluto del file export.py
        current_directory = os.path.dirname(os.path.abspath(__file__))
        #export_py_path = os.path.join(current_directory, "export.py")
        export_py_path = os.path.join(current_directory, "YOLOv5", "export.py")
        try:
            # Costruisci il comando base con i parametri selezionati o valori predefiniti
            command = f"python {export_py_path} --weights {self.weights_file.get()} --include {self.include_option.get()} --imgsz {self.img_size.get()} --device {self.device.get()} "

            # Aggiungi l'opzione --half se half_option è True
            if self.half_option.get():
                command += " --half"

            # Esegui il comando
            messagebox.showinfo("Comando", f"Comando: {command}")
            # Commenta la linea sottostante e rimuovi il commento dalla successiva per eseguire il comando
            subprocess.run(command, shell=True, check=True)
            tk.messagebox.showinfo("Successo", "Modello esportato con successo!")

        except subprocess.CalledProcessError as e:
            tk.messagebox.showerror("Errore", f"Errore durante l'esportazione del modello:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = YOLOv5ExporterGUI(root)
    root.mainloop()

