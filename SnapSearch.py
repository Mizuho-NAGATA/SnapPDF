# -------------------------------------------------------------
# PDF Keyword Search and CSV Output Program
# This program "Snap Search" was developed with the assistance of ChatGPT.
# Copyright (c) 2023 NAGATA Mizuho, Institute of Laser Engineering, Osaka University.
# Created on: 2023-09-15
# Last updated on: 2024-06-13
# -------------------------------------------------------------
import os
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime  # Import the datetime module

def search_pdf():
    # Display a dialog box to select a directory
    selected_directory = filedialog.askdirectory(title="Select the directory you want to search") # Set the title of the dialog box

    # Get the entered keywords
    search_keywords = keyword_entry.get().split()  # Split keywords by space

    # Get the state of the and search checkbox
    and_search = and_checkbox_var.get()

    # List to store search results
    search_results = []

    # Search for PDF files in the directory
    for root, _, files in os.walk(selected_directory):
        for filename in files:
            if filename.endswith('.pdf'):
                pdf_file_path = os.path.join(root, filename)

                # Open the PDF file
                pdf_reader = PdfReader(pdf_file_path)

                # Search each page
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()

                    # and search: Check if all keywords are included
                if and_search:
                    if all(keyword in page_text for keyword in search_keywords):
                        # Add keywords to search results
                        search_results.append((filename, pdf_file_path, search_keywords))
                        continue  # No need to check other pages
                # or search: Check if any one keyword is included
                else:
                    if any(keyword in page_text for keyword in search_keywords):
                        # Add keywords to search results
                        search_results.append((filename, pdf_file_path, search_keywords))


    # Get the current date and time
    current_datetime = datetime.now()

    # Format the current date and time
    date_time_str = current_datetime.strftime("%Y%m%d_%H%M%S")

    # Path to the search result CSV file (including the current time)
    csv_file_path = f'search_results_{date_time_str}.csv'

    # Write the search results to a CSV file
    with open(csv_file_path, 'w', newline='', encoding='shift-jis') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File name', 'Location', 'Keywords'])

        for filename, location, keywords in search_results:
            csv_writer.writerow([filename, location, ', '.join(keywords)])

    # Create a window to display search results
    result_window = tk.Toplevel(window)
    result_window.title('PDF Text Search Results')

    if not search_results:
        # Label when there are no search results
        result_label = tk.Label(result_window, text='No keywords were found')
        result_label.pack()
    else:
        # Display search results
        result_label = tk.Label(result_window, text='PDF files where keywords were found:')
        result_label.pack()

    # Display the file name, location, and keywords of the search results
    for filename, location, keywords in search_results:
        keyword_str = ', '.join(keywords)
        result_text = f'File name: {filename}, Location: {location}, Keywords: {keyword_str}'
        result_label = tk.Label(result_window, text=result_text, font=("Helvetica", 14))
        result_label.pack()

# Create a GUI window
window = tk.Tk()
window.title('PDF Text Search Snap Search')

# Change the size of the window
window.geometry("400x200")  # Width 400 pixels, height 200 pixels

# Keyword input field
keyword_label = tk.Label(window, text='Search keywords \n (separate with space):', font=("Helvetica", 14))
keyword_label.pack()
keyword_entry = tk.Entry(window, font=("Helvetica", 14))
keyword_entry.pack()

# and search checkbox (checked from the beginning)
and_checkbox_var = tk.BooleanVar(value=True)
and_checkbox = tk.Checkbutton(window, text='and search', font=("Helvetica", 14), variable=and_checkbox_var)
and_checkbox.pack()

# Directory selection and CSV output button
export_csv_button = tk.Button(window, text='Select directory \n Output search results to CSV', font=("Helvetica", 14), command=search_pdf)
export_csv_button.pack()

window.mainloop()
