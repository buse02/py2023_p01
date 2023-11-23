import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Variable to store extracted titles
titles = []

# Function to extract titles from PDF files in a specified directory
def extract_titles(directory):
    global titles
    titles = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(directory, file_name)
            print(f"Processing file: {file_path}")
            pdf_document = fitz.open(file_path)
            title = pdf_document.metadata.get("title", "").strip()
            print(f"Extracted title: {title}")
            titles.append((title, file_path))
            pdf_document.close()
    return titles

# Function to save titles to a new PDF file
def save_titles(title_list, output_filename):
    try:
        pdf_writer = fitz.open()
        for title, file_path in title_list:
            pdf_document = fitz.open(file_path)
            pdf_writer.insert_pdf(pdf_document)
            pdf_document.close()

        # Create a new PDF with improved readability
        with open(output_filename, "wb") as output_file:
            c = canvas.Canvas(output_file, pagesize=letter)
            c.setFont("Helvetica", 16)
            c.drawString(72, 750, "Extracted Titles")
            c.setFont("Helvetica", 12)

            for index, (title, _) in enumerate(title_list, start=1):
                y_position = 720 - (index * 14)
                c.drawString(72, y_position, f"{index}. {title}")

            c.save()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to update the Text widget with titles
def update_text_widget():
    global titles
    titles = extract_titles(directory_path)
    text_widget.delete(1.0, tk.END)  # Clear existing content
    text_widget.insert(tk.END, "Extracted Titles:\n\n")
    text_widget.insert(tk.END, "\n".join(title[0] for title in titles))

# Function to handle button clicks
def button_click(button):
    global directory_path
    if button == "extract":
        directory_path = os.path.join(os.getcwd(), "pdfFiles")
        print(f"Selected directory: {directory_path}")
        update_text_widget()
        result_label.config(text="Titles extracted successfully.")
    elif button == "save":
        directory_path = os.path.join(os.getcwd(), "pdfFiles")
        print(f"Selected directory: {directory_path}")
        save_titles(titles, "all_titles.pdf")
        result_label.config(text="Titles saved to all_titles.pdf.")
    elif button == "exit":
        root.destroy()

# Create the main GUI window
root = tk.Tk()
root.title("PDF Title Extractor")

# Create and place buttons in the GUI
extract_button = tk.Button(root, text="Extract Titles", command=lambda: button_click("extract"))
extract_button.pack(pady=10)

save_button = tk.Button(root, text="Save", command=lambda: button_click("save"))
save_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=lambda: button_click("exit"))
exit_button.pack(pady=10)

# Create a label to display results
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Create a Text widget to display extracted titles
text_widget = tk.Text(root, height=10, width=50)
text_widget.pack(pady=10)

# Run the GUI
root.mainloop()
