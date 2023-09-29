import pdfplumber
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # Importar ttk para Progressbar

def compare_pdfs(pdf_file1, pdf_file2):
    with pdfplumber.open(pdf_file1) as pdf1, pdfplumber.open(pdf_file2) as pdf2:
        num_pages1 = len(pdf1.pages)
        num_pages2 = len(pdf2.pages)

        if num_pages1 != num_pages2:
            return False  # Diferente número de páginas

        for page_num in range(num_pages1):
            page1 = pdf1.pages[page_num]
            page2 = pdf2.pages[page_num]

            text1 = page1.extract_text()
            text2 = page2.extract_text()

            if text1 != text2:
                return False  # Diferencias de texto en la página

    return True

def browse_pdf1():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf1_entry.delete(0, tk.END)
    pdf1_entry.insert(0, file_path)

def browse_pdf2():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf2_entry.delete(0, tk.END)
    pdf2_entry.insert(0, file_path)

def compare_button_click():
    pdf_file1 = pdf1_entry.get()
    pdf_file2 = pdf2_entry.get()

    # Deshabilitar los elementos de entrada durante la comparación
    pdf1_entry.config(state="disabled")
    pdf2_entry.config(state="disabled")
    pdf1_browse_button.config(state="disabled")
    pdf2_browse_button.config(state="disabled")
    compare_button.config(state="disabled")

    # Configurar el texto "Comparando..."
    result_label.config(text="Comparing....")

    # Iniciar la barra de progreso desde cero
    progress_bar.stop()
    progress_bar.config(mode="indeterminate")
    progress_bar.start()

    # Realizar la comparación en un hilo para evitar bloquear la interfaz gráfica
    import threading
    comparison_thread = threading.Thread(target=perform_comparison, args=(pdf_file1, pdf_file2))
    comparison_thread.start()

def perform_comparison(pdf_file1, pdf_file2):
    if compare_pdfs(pdf_file1, pdf_file2):
        result_label.config(text="PDF documents are exactly the same.")
    else:
        result_label.config(text="PDF documents are different.")

    # Habilitar nuevamente los elementos de entrada
    pdf1_entry.config(state="normal")
    pdf2_entry.config(state="normal")
    pdf1_browse_button.config(state="normal")
    pdf2_browse_button.config(state="normal")
    compare_button.config(state="normal")

    # Detener la barra de progreso y restablecerla a modo determinado (normal)
    progress_bar.stop()
    progress_bar.config(mode="determinate")

# Crear la ventana principal
root = tk.Tk()
root.title("PDF Comparison")
root.geometry("400x300")  # Tamaño de la ventana

# Crear un Frame que ocupará todo el espacio disponible y lo centrará
frame = tk.Frame(root)
frame.pack(expand=True, fill="both", padx=20, pady=20)

# Crear y configurar elementos de la UI dentro del Frame
pdf1_label = tk.Label(frame, text="PDF 1:")
pdf1_label.pack()

pdf1_entry = tk.Entry(frame)
pdf1_entry.pack()

pdf1_browse_button = tk.Button(frame, text="Search PDF 1", command=browse_pdf1)
pdf1_browse_button.pack()

pdf2_label = tk.Label(frame, text="PDF 2:")
pdf2_label.pack()

pdf2_entry = tk.Entry(frame)
pdf2_entry.pack()

pdf2_browse_button = tk.Button(frame, text="Search PDF 2", command=browse_pdf2)
pdf2_browse_button.pack()

compare_button = tk.Button(frame, text="Start Comparison", command=compare_button_click)
compare_button.pack()

# Agregar una Progressbar (animación de carga circular)
progress_bar = ttk.Progressbar(frame, mode="determinate")
progress_bar.pack()

result_label = tk.Label(frame, text="")
result_label.pack()

root.mainloop()
