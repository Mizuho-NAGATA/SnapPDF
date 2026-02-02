# -------------------------------------------------------------
# GUI module for SnapPDF
# Copyright (c) 2023-2026 NAGATA Mizuho
# Institute of Laser Engineering, The University of Osaka
# -------------------------------------------------------------

import os
import threading
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional

from PIL import Image, ImageTk

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD

    HAS_DND = True
except ImportError:
    HAS_DND = False
    print("Warning: tkinterdnd2 not available. Drag-and-drop disabled.")

from .config import AppConfig
from .core import PDFGenerator
from .utils import format_error_message, resize_image_for_thumbnail


class SnapPDFApplication:
    """Main GUI application for SnapPDF"""

    def __init__(self, root):
        """
        Initialize the application.

        Args:
            root: Root Tkinter window
        """
        self.root = root
        self.root.title(AppConfig.WINDOW_TITLE)

        # Application state
        self.pdf_generator: Optional[PDFGenerator] = None
        self.current_layout = "standard"
        self.photo_images: List[ImageTk.PhotoImage] = []

        # Initialize with default layout
        self._update_pdf_generator()

        # Setup GUI
        self._setup_gui()

    def _setup_gui(self) -> None:
        """Setup the GUI layout"""
        # Main container
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title section
        self._create_title_section(main_frame)

        # Layout selection section
        self._create_layout_section(main_frame)

        # Input fields section
        self._create_input_section(main_frame)

        # Excel section
        self._create_excel_section(main_frame)

        # Image selection section
        self._create_image_selection_section(main_frame)

        # Image list section
        self._create_image_list_section(main_frame)

        # Image reordering section
        self._create_reorder_section(main_frame)

        # Thumbnail display section
        self._create_thumbnail_section(main_frame)

        # Export section
        self._create_export_section(main_frame)

    def _create_title_section(self, parent: tk.Widget) -> None:
        """Create title section"""
        title_frame = tk.Frame(parent)
        title_frame.pack(pady=10)

        title_label = tk.Label(
            title_frame,
            text="SnapPDF - Unified Image to PDF Converter",
            font=("BIZ-UDGothicR", 18, "bold"),
        )
        title_label.pack()

        version_label = tk.Label(
            title_frame, text="Version 2.0.0", font=("BIZ-UDGothicR", 10)
        )
        version_label.pack()

    def _create_layout_section(self, parent: tk.Widget) -> None:
        """Create layout selection section"""
        layout_frame = tk.LabelFrame(
            parent,
            text="Page Layout",
            font=AppConfig.DEFAULT_BUTTON_FONT,
            padx=10,
            pady=10,
        )
        layout_frame.pack(fill=tk.X, pady=10)

        # Layout selection label
        label = tk.Label(
            layout_frame, text="Select layout:", font=AppConfig.DEFAULT_BUTTON_FONT
        )
        label.pack(side=tk.LEFT, padx=5)

        # Layout dropdown
        self.layout_var = tk.StringVar(value=AppConfig.LAYOUTS["standard"].display_name)
        self.layout_combo = ttk.Combobox(
            layout_frame,
            textvariable=self.layout_var,
            values=AppConfig.get_layout_display_names(),
            state="readonly",
            font=("BIZ-UDGothicR", 12),
            width=30,
        )
        self.layout_combo.pack(side=tk.LEFT, padx=5)
        self.layout_combo.bind("<<ComboboxSelected>>", self._on_layout_changed)

        # Layout info label
        self.layout_info_label = tk.Label(
            layout_frame,
            text=AppConfig.LAYOUTS["standard"].description,
            font=("BIZ-UDGothicR", 10),
            fg="gray",
        )
        self.layout_info_label.pack(side=tk.LEFT, padx=10)

    def _create_input_section(self, parent: tk.Widget) -> None:
        """Create input fields section"""
        input_frame = tk.LabelFrame(
            parent,
            text="PDF Information",
            font=AppConfig.DEFAULT_BUTTON_FONT,
            padx=10,
            pady=10,
        )
        input_frame.pack(fill=tk.X, pady=10)

        # Title field
        title_field_frame = tk.Frame(input_frame)
        title_field_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            title_field_frame,
            text="Title:",
            width=10,
            font=AppConfig.DEFAULT_BUTTON_FONT,
            anchor="w",
        ).pack(side=tk.LEFT, padx=5)

        self.title_entry = tk.Entry(
            title_field_frame, font=AppConfig.DEFAULT_BUTTON_FONT
        )
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Remarks field
        remarks_field_frame = tk.Frame(input_frame)
        remarks_field_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            remarks_field_frame,
            text="Remarks:",
            width=10,
            font=AppConfig.DEFAULT_BUTTON_FONT,
            anchor="w",
        ).pack(side=tk.LEFT, padx=5)

        self.remarks_entry = tk.Entry(
            remarks_field_frame, font=AppConfig.DEFAULT_BUTTON_FONT
        )
        self.remarks_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def _create_excel_section(self, parent: tk.Widget) -> None:
        """Create Excel file selection section"""
        excel_frame = tk.LabelFrame(
            parent,
            text="Excel Data (Optional)",
            font=AppConfig.DEFAULT_BUTTON_FONT,
            padx=10,
            pady=10,
        )
        excel_frame.pack(fill=tk.X, pady=10)

        button_frame = tk.Frame(excel_frame)
        button_frame.pack(fill=tk.X)

        self.excel_button = tk.Button(
            button_frame,
            text="Select Excel File",
            command=self._select_excel_file,
            font=AppConfig.DEFAULT_BUTTON_FONT,
            bg="#90EE90",
        )
        self.excel_button.pack(side=tk.LEFT, padx=5)

        self.excel_clear_button = tk.Button(
            button_frame,
            text="Clear Excel Data",
            command=self._clear_excel_data,
            font=AppConfig.DEFAULT_BUTTON_FONT,
            state=tk.DISABLED,
        )
        self.excel_clear_button.pack(side=tk.LEFT, padx=5)

        self.excel_status_label = tk.Label(
            button_frame,
            text="No Excel data loaded",
            font=("BIZ-UDGothicR", 10),
            fg="gray",
        )
        self.excel_status_label.pack(side=tk.LEFT, padx=10)

    def _create_image_selection_section(self, parent: tk.Widget) -> None:
        """Create image selection section"""
        image_select_frame = tk.LabelFrame(
            parent,
            text="Image Selection",
            font=AppConfig.DEFAULT_BUTTON_FONT,
            padx=10,
            pady=10,
        )
        image_select_frame.pack(fill=tk.X, pady=10)

        button_frame = tk.Frame(image_select_frame)
        button_frame.pack(fill=tk.X)

        self.select_images_button = tk.Button(
            button_frame,
            text="Select Images",
            command=self._select_images,
            font=AppConfig.DEFAULT_BUTTON_FONT,
            bg="#87CEEB",
        )
        self.select_images_button.pack(side=tk.LEFT, padx=5)

        self.clear_all_button = tk.Button(
            button_frame,
            text="Clear All Images",
            command=self._clear_all_images,
            font=AppConfig.DEFAULT_BUTTON_FONT,
        )
        self.clear_all_button.pack(side=tk.LEFT, padx=5)

        self.image_count_label = tk.Label(
            button_frame,
            text="Images: 0",
            font=AppConfig.DEFAULT_BUTTON_FONT,
            fg="blue",
        )
        self.image_count_label.pack(side=tk.LEFT, padx=10)

    def _create_image_list_section(self, parent: tk.Widget) -> None:
        """Create image list section with treeview"""
        list_frame = tk.LabelFrame(
            parent,
            text="Selected Images",
            font=AppConfig.DEFAULT_BUTTON_FONT,
            padx=10,
            pady=10,
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create treeview with scrollbar
        tree_scroll_frame = tk.Frame(list_frame)
        tree_scroll_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(tree_scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.image_tree = ttk.Treeview(
            tree_scroll_frame,
            columns=("Index", "File Name", "Path"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8,
        )
        self.image_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.image_tree.yview)

        # Configure columns
        self.image_tree.heading("Index", text="#")
        self.image_tree.heading("File Name", text="File Name")
        self.image_tree.heading("Path", text="Full Path")

        self.image_tree.column("Index", width=50, anchor=tk.CENTER)
        self.image_tree.column("File Name", width=200)
        self.image_tree.column("Path", width=400)

    def _create_reorder_section(self, parent: tk.Widget) -> None:
        """Create image reordering buttons section"""
        reorder_frame = tk.Frame(parent)
        reorder_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            reorder_frame, text="Reorder Images:", font=AppConfig.DEFAULT_BUTTON_FONT
        ).pack(side=tk.LEFT, padx=5)

        self.move_up_button = tk.Button(
            reorder_frame,
            text="↑ Move Up",
            command=self._move_image_up,
            font=AppConfig.DEFAULT_BUTTON_FONT,
        )
        self.move_up_button.pack(side=tk.LEFT, padx=5)

        self.move_down_button = tk.Button(
            reorder_frame,
            text="↓ Move Down",
            command=self._move_image_down,
            font=AppConfig.DEFAULT_BUTTON_FONT,
        )
        self.move_down_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(
            reorder_frame,
            text="✖ Delete Selected",
            command=self._delete_selected_images,
            font=AppConfig.DEFAULT_BUTTON_FONT,
            fg="red",
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def _create_thumbnail_section(self, parent: tk.Widget) -> None:
        """Create thumbnail display section"""
        thumbnail_outer_frame = tk.LabelFrame(
            parent,
            text="Image Preview",
            font=AppConfig.DEFAULT_BUTTON_FONT,
            padx=10,
            pady=10,
        )
        thumbnail_outer_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create canvas with scrollbar for thumbnails
        canvas_frame = tk.Frame(thumbnail_outer_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.thumbnail_canvas = tk.Canvas(canvas_frame, height=200)
        thumb_scrollbar = tk.Scrollbar(
            canvas_frame, orient=tk.HORIZONTAL, command=self.thumbnail_canvas.xview
        )

        self.thumbnail_canvas.configure(xscrollcommand=thumb_scrollbar.set)
        self.thumbnail_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        thumb_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Frame inside canvas for thumbnails
        self.thumbnail_frame = tk.Frame(self.thumbnail_canvas)
        self.thumbnail_canvas.create_window(
            (0, 0), window=self.thumbnail_frame, anchor=tk.NW
        )

        self.thumbnail_frame.bind(
            "<Configure>",
            lambda e: self.thumbnail_canvas.configure(
                scrollregion=self.thumbnail_canvas.bbox("all")
            ),
        )

    def _create_export_section(self, parent: tk.Widget) -> None:
        """Create PDF export section"""
        export_frame = tk.Frame(parent)
        export_frame.pack(fill=tk.X, pady=20)

        self.export_button = tk.Button(
            export_frame,
            text="📄 Create PDF",
            command=self._create_pdf,
            font=("BIZ-UDGothicR", 16, "bold"),
            bg="#FFD700",
            height=2,
        )
        self.export_button.pack(fill=tk.X, padx=50)

    def _on_layout_changed(self, event=None) -> None:
        """Handle layout selection change"""
        selected_display_name = self.layout_var.get()

        # Find the layout by display name
        for layout_name, layout in AppConfig.LAYOUTS.items():
            if layout.display_name == selected_display_name:
                self.current_layout = layout_name
                self.layout_info_label.config(text=layout.description)
                self._update_pdf_generator()
                break

    def _update_pdf_generator(self) -> None:
        """Update PDF generator with current layout"""
        layout = AppConfig.get_layout(self.current_layout)

        # Preserve existing data
        old_image_paths = []
        old_excel_data = []
        old_excel_headers = []

        if self.pdf_generator:
            old_image_paths = self.pdf_generator.image_paths.copy()
            old_excel_data = self.pdf_generator.excel_data.copy()
            old_excel_headers = self.pdf_generator.excel_headers.copy()

        # Create new generator
        self.pdf_generator = PDFGenerator(layout)

        # Restore data
        if old_image_paths:
            self.pdf_generator.image_paths = old_image_paths
        if old_excel_headers:
            self.pdf_generator.excel_data = old_excel_data
            self.pdf_generator.excel_headers = old_excel_headers

    def _select_excel_file(self) -> None:
        """Handle Excel file selection"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File", filetypes=AppConfig.SUPPORTED_EXCEL_FORMATS
        )

        if file_path:
            success = self.pdf_generator.load_excel_data(file_path)
            if success:
                num_rows = len(self.pdf_generator.excel_data)
                self.excel_status_label.config(
                    text=f"Excel loaded: {num_rows} rows", fg="green"
                )
                self.excel_clear_button.config(state=tk.NORMAL)
                messagebox.showinfo(
                    "Success",
                    f"Excel file loaded successfully.\n{num_rows} rows of data.",
                )
            else:
                messagebox.showerror(
                    "Error", "Failed to load Excel file. Please check the file format."
                )

    def _clear_excel_data(self) -> None:
        """Clear loaded Excel data"""
        self.pdf_generator.clear_excel_data()
        self.excel_status_label.config(text="No Excel data loaded", fg="gray")
        self.excel_clear_button.config(state=tk.DISABLED)
        messagebox.showinfo("Cleared", "Excel data cleared.")

    def _select_images(self) -> None:
        """Handle image selection"""
        file_paths = filedialog.askopenfilenames(
            title="Select Images", filetypes=AppConfig.SUPPORTED_IMAGE_FORMATS
        )

        if file_paths:
            successful, failed = self.pdf_generator.add_images(list(file_paths))

            message = f"Added {successful} images successfully"
            if failed > 0:
                message += f"\n{failed} files failed to load"

            messagebox.showinfo("Images Selected", message)
            self._update_image_list()
            self._update_thumbnails_async()

    def _clear_all_images(self) -> None:
        """Clear all loaded images"""
        if self.pdf_generator.get_image_count() == 0:
            messagebox.showinfo("Info", "No images to clear.")
            return

        result = messagebox.askyesno(
            "Confirm", "Are you sure you want to clear all images?"
        )

        if result:
            self.pdf_generator.clear_images()
            self._update_image_list()
            self._clear_thumbnails()
            messagebox.showinfo("Cleared", "All images cleared.")

    def _update_image_list(self) -> None:
        """Update the image list treeview"""
        # Clear existing items
        for item in self.image_tree.get_children():
            self.image_tree.delete(item)

        # Add current images
        for i, path in enumerate(self.pdf_generator.image_paths):
            filename = os.path.basename(path)
            self.image_tree.insert("", "end", values=(i + 1, filename, path))

        # Update count label
        count = self.pdf_generator.get_image_count()
        self.image_count_label.config(text=f"Images: {count}")

    def _move_image_up(self) -> None:
        """Move selected image up in the list"""
        selection = self.image_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an image to move.")
            return

        item = selection[0]
        values = self.image_tree.item(item, "values")
        index = int(values[0]) - 1

        if index > 0:
            self.pdf_generator.move_image(index, index - 1)
            self._update_image_list()
            self._update_thumbnails_async()

    def _move_image_down(self) -> None:
        """Move selected image down in the list"""
        selection = self.image_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an image to move.")
            return

        item = selection[0]
        values = self.image_tree.item(item, "values")
        index = int(values[0]) - 1

        if index < self.pdf_generator.get_image_count() - 1:
            self.pdf_generator.move_image(index, index + 1)
            self._update_image_list()
            self._update_thumbnails_async()

    def _delete_selected_images(self) -> None:
        """Delete selected images from the list"""
        selection = self.image_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select images to delete.")
            return

        result = messagebox.askyesno(
            "Confirm", f"Delete {len(selection)} selected image(s)?"
        )

        if result:
            # Get indices and sort in reverse order to delete from back to front
            indices = []
            for item in selection:
                values = self.image_tree.item(item, "values")
                indices.append(int(values[0]) - 1)

            indices.sort(reverse=True)

            for index in indices:
                self.pdf_generator.remove_image(index)

            self._update_image_list()
            self._update_thumbnails_async()

    def _update_thumbnails_async(self) -> None:
        """Update thumbnails asynchronously"""
        threading.Thread(target=self._update_thumbnails, daemon=True).start()

    def _update_thumbnails(self) -> None:
        """Update thumbnail display"""
        # Clear existing thumbnails
        self._clear_thumbnails()

        if not self.pdf_generator.image_paths:
            return

        # Generate thumbnails in parallel
        with ThreadPoolExecutor() as executor:
            futures = []
            for path in self.pdf_generator.image_paths:
                future = executor.submit(
                    resize_image_for_thumbnail, path, AppConfig.MAX_THUMBNAIL_SIZE
                )
                futures.append(future)

            # Display thumbnails as they become available
            for i, future in enumerate(futures):
                try:
                    pil_image = future.result()
                    if pil_image:
                        photo = ImageTk.PhotoImage(pil_image)
                        self.photo_images.append(photo)

                        # Create thumbnail label
                        label = tk.Label(self.thumbnail_frame, image=photo)
                        label.grid(
                            row=i // AppConfig.THUMBNAIL_COLUMNS,
                            column=i % AppConfig.THUMBNAIL_COLUMNS,
                            padx=5,
                            pady=5,
                        )
                except Exception as e:
                    print(f"Error creating thumbnail: {format_error_message(e)}")

        # Update scroll region
        self.thumbnail_frame.update_idletasks()
        self.thumbnail_canvas.configure(scrollregion=self.thumbnail_canvas.bbox("all"))

    def _clear_thumbnails(self) -> None:
        """Clear all thumbnails"""
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        self.photo_images.clear()

    def _create_pdf(self) -> None:
        """Create PDF from loaded images and data"""
        # Validate we have content
        if (
            self.pdf_generator.get_image_count() == 0
            and not self.pdf_generator.has_excel_data()
        ):
            messagebox.showerror(
                "Error", "Please select at least one image or load Excel data."
            )
            return

        # Get title and remarks
        title = self.title_entry.get()
        remarks = self.remarks_entry.get()

        # Show progress message
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Creating PDF")
        progress_window.geometry("300x100")
        progress_window.transient(self.root)
        progress_window.grab_set()

        tk.Label(
            progress_window,
            text="Creating PDF...\nPlease wait.",
            font=AppConfig.DEFAULT_BUTTON_FONT,
        ).pack(expand=True)

        self.root.update()

        # Generate PDF
        def generate():
            success, message = self.pdf_generator.generate_pdf(
                title=title, remarks=remarks, open_after_creation=True
            )

            # Close progress window
            progress_window.destroy()

            # Show result
            if success:
                messagebox.showinfo("Success", message)
                # Optionally clear images after successful creation
                # self._clear_all_images()
            else:
                messagebox.showerror("Error", message)

        # Run in thread to keep GUI responsive
        threading.Thread(target=generate, daemon=True).start()

    def run(self) -> None:
        """Start the application main loop"""
        self.root.mainloop()


def create_application() -> SnapPDFApplication:
    """
    Create and return the main application.

    Returns:
        SnapPDFApplication instance
    """
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    app = SnapPDFApplication(root)
    return app
