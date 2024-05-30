import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.root.geometry("800x600")
        self.file_path = None

        self.current_font_family = 'Arial'
        self.current_font_size = 12

        self.create_widgets()
        self.create_menu_bar()
        self.create_status_bar()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, undo=True, wrap='word', font=(self.current_font_family, self.current_font_size))
        self.text_area.pack(fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        self.text_area.bind('<KeyRelease>', self.update_status)

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Print", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        format_menu = tk.Menu(menu_bar, tearoff=0)
        format_menu.add_command(label="Font Size", command=self.choose_font_size)
        menu_bar.add_cascade(label="Format", menu=format_menu)

        self.root.config(menu=menu_bar)

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.root, text="Characters: 0 | Words: 0", anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, event=None):
        content = self.text_area.get(1.0, tk.END)
        num_chars = len(content) - 1  # subtract 1 for the trailing newline character
        num_words = len(content.split())
        self.status_bar.config(text=f"Characters: {num_chars} | Words: {num_words}")

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.update_status()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt"),
                                                          ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.file_path = file_path
            self.root.title(f"Simple Text Editor - {os.path.basename(file_path)}")
            self.update_status()

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Save File", f"Failed to save file\n{str(e)}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"),
                                                            ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.file_path = file_path
                self.root.title(f"Simple Text Editor - {os.path.basename(file_path)}")
                self.update_status()
            except Exception as e:
                messagebox.showerror("Save File As", f"Failed to save file\n{str(e)}")

    def print_file(self):
        try:
            import tempfile
            import subprocess
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                tmp_file.write(self.text_area.get(1.0, tk.END).encode())
                tmp_file_path = tmp_file.name
            subprocess.run(["lpr", tmp_file_path])
        except Exception as e:
            messagebox.showerror("Print File", f"Failed to print file\n{str(e)}")

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def find_text(self):
        find_string = simpledialog.askstring("Find", "Enter text to find:")
        if find_string:
            self.text_area.tag_remove("found", 1.0, tk.END)
            start_pos = 1.0
            while True:
                start_pos = self.text_area.search(find_string, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(find_string)}c"
                self.text_area.tag_add("found", start_pos, end_pos)
                start_pos = end_pos
            self.text_area.tag_config("found", foreground="white", background="blue")

    def replace_text(self):
        find_string = simpledialog.askstring("Find", "Enter text to find:")
        replace_string = simpledialog.askstring("Replace", "Enter text to replace with:")
        if find_string and replace_string:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(find_string, replace_string)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)

    def choose_font_size(self):
        font_size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=self.current_font_size)
        if font_size:
            self.current_font_size = font_size
            self.text_area.config(font=(self.current_font_family, self.current_font_size))

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()