import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import pdfplumber
import markdown
from googletrans import Translator

# Function to select the input folder
def select_input_folder():
    folder = filedialog.askdirectory(title="Select Input Folder")
    if folder:
        input_var.set(folder)

# Function to select the output folder
def select_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_var.set(folder)

# Function to convert PDFs to translated Markdown
def convert_pdf_to_translated_markdown():
    input_folder = input_var.get()
    output_folder = output_var.get()
    rename_format = rename_var.get()
    target_language = language_var.get()

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Please select both input and output folders.")
        return

    # List only PDF files in the input folder
    pdfs = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]

    if not pdfs:
        messagebox.showwarning("Warning", "No PDF files found in the input folder.")
        return

    progress_bar["maximum"] = len(pdfs)
    progress_bar["value"] = 0

    translator = Translator()

    try:
        for index, file in enumerate(pdfs):
            pdf_path = os.path.join(input_folder, file)
            md_filename = rename_format.format(index=index + 1, name=os.path.splitext(file)[0])
            md_path = os.path.join(output_folder, f"{md_filename}.md")

            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:  # Check if text was extracted
                        text += extracted + "\n"

            if text.strip():
                # Translate text if target language is set
                if target_language:
                    text = translator.translate(text, dest=target_language).text

                # Convert text to Markdown and save
                markdown_text = markdown.markdown(text)
                with open(md_path, "w", encoding="utf-8") as md_file:
                    md_file.write(markdown_text)
            else:
                messagebox.showwarning("Warning", f"Could not extract text from PDF: {file}")

            # Update progress bar
            progress_bar["value"] = index + 1
            percentage_var.set(f"{int((index + 1) / len(pdfs) * 100)}%")
            window.update_idletasks()

        messagebox.showinfo("Success", "Conversion and translation completed successfully!")
    except Exception as e:
        # Capture unexpected errors
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Main window
window = tk.Tk()
window.title("PDF to Translated Markdown Converter")

# Variables to store folder paths and options
input_var = tk.StringVar()
output_var = tk.StringVar()
rename_var = tk.StringVar(value="{name}_translated")  # Default rename pattern
language_var = tk.StringVar(value="pt")  # Default target language (Portuguese)
percentage_var = tk.StringVar(value="0%")

# Labels and input fields
tk.Label(window, text="Input Folder Path:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Entry(window, textvariable=input_var, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(window, text="Select", command=select_input_folder).grid(row=0, column=2, padx=5, pady=5)

tk.Label(window, text="Output Folder Path:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
tk.Entry(window, textvariable=output_var, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(window, text="Select", command=select_output_folder).grid(row=1, column=2, padx=5, pady=5)

tk.Label(window, text="Rename Format (e.g., {name}_translated):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
tk.Entry(window, textvariable=rename_var, width=50).grid(row=2, column=1, padx=5, pady=5)

tk.Label(window, text="Target Language (e.g., 'en' or 'pt')").grid(row=3, column=0, sticky="w", padx=5, pady=5)
tk.Entry(window, textvariable=language_var, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

# Convert button
tk.Button(window, text="Convert", command=convert_pdf_to_translated_markdown).grid(row=4, column=1, pady=10)

# Progress bar
progress_bar = ttk.Progressbar(window, length=400, mode="determinate")
progress_bar.grid(row=5, column=1, pady=10)

# Label to show percentage
tk.Label(window, textvariable=percentage_var).grid(row=6, column=1, pady=5)

# Exit button
tk.Button(window, text="Exit", command=window.quit).grid(row=7, column=1, pady=10)

# Main application loop
window.mainloop()
