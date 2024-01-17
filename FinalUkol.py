"""
This is my final zpro programm, which was made just for fun by KinkLYNAmikadze(Mykhailo Plokhin)

Jednoduchá Python aplikace s grafickým uživatelským rozhraním (GUI) pomocí knihovny Tkinter. 
Slouží k vedení čtenářského deníku s funkcemi jako vkládání, vyhledávání, mazání a ukládání dat do souboru.
Aplikace také zobrazuje aktuální počet knih v deníku. Design byl vylepšen o barevný motiv pro příjemné uživatelské rozhraní.
      


Napište program, který bude sloužit jako čtenářský deník. Základem programu bude datová struktura reprezentující přečtenou knihu.


Pro každou knihu uchovávejte následující údaje:

-Autor
-Titul
-Žánr (jedna kniha může spadat do více žánrů)
-Rok vydání
-Počet stran
-Den, měsíc, rok přečtení


Uživatel programu bude moci:

-Vytvářet nový deník
-Deník ukládat do souboru
-Deník načítat ze souboru
-Vkládat jednotlivé záznamy
-Vyhledávat záznamy podle autora a titulu
-Mazat záznamy podle autora a titulu
-Vymazat všechny záznamy
-Zcela zrušit deník


"""

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

class ReadingLog:
    def __init__(self, filename):
        self.filename = filename
        self.diary = self.load_from_file()

    def insert_entry(self, entry):
        existing_titles = {entry['Title'].lower() for entry in self.diary}
        if entry['Title'].lower() in existing_titles:
            messagebox.showerror("Error", "Duplicate entry. Entry not added.")
            return

        entry['Timestamp'] = self.get_current_timestamp()
        self.diary.append(entry)
        self.save_to_file()
        messagebox.showinfo("Success", "Entry added successfully.")

    def search_entries(self, author=None, title=None):
        results = []
        for entry in self.diary:
            if (author is None or entry['Author'].lower() == author.lower()) and (title is None or entry['Title'].lower() == title.lower()):
                results.append(entry)
        return results

    def get_author_books(self, author):
        results = []
        for entry in self.diary:
            if entry['Author'].lower() == author.lower():
                results.append(entry)
        return results

    def delete_entry(self, author, title):
        self.diary = [entry for entry in self.diary if entry['Author'].lower() != author.lower() or entry['Title'].lower() != title.lower()]
        self.save_to_file()
        messagebox.showinfo("Success", "Entry deleted successfully.")

    def delete_all_entries(self):
        self.diary = []
        self.save_to_file()
        messagebox.showinfo("Success", "All entries deleted.")

    def get_book_count(self):
        return len(self.diary)

    def save_to_file(self):
        with open(self.filename, 'w') as file:
            json.dump(self.diary, file, indent=2)
        messagebox.showinfo("Success", f"Diary saved to {self.filename}")

    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_current_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ReadingLogGUI(tk.Tk):
    def __init__(self, filename):
        super().__init__()
        self.title("Reading Log")
        self.geometry("400x600")
        self.dark_theme = tk.BooleanVar(value=False)
        self.configure(bg="#F0F0F0")

        self.reading_log = ReadingLog(filename)

        self.create_widgets()

        self.update_book_count()
        self.show_all_books()

    def create_widgets(self):
        bg_color = "#FFFFFF"
        fg_color = "#000000"

        self.author_label = tk.Label(self, text="Author:", bg="#F0F0F0", fg=fg_color)
        self.author_entry = tk.Entry(self, bg=bg_color)

        self.title_label = tk.Label(self, text="Title:", bg="#F0F0F0", fg=fg_color)
        self.title_entry = tk.Entry(self, bg=bg_color)

        self.year_label = tk.Label(self, text="Year:", bg="#F0F0F0", fg=fg_color)
        self.year_entry = tk.Entry(self, bg=bg_color)

        self.pages_label = tk.Label(self, text="Number of Pages:", bg="#F0F0F0", fg=fg_color)
        self.pages_entry = tk.Entry(self, bg=bg_color)

        self.insert_button = tk.Button(self, text="Insert Entry", command=self.insert_entry, bg="#4CAF50", fg="#FFFFFF")
        self.search_button = tk.Button(self, text="Search Entries", command=self.search_entries, bg="#008CBA", fg="#FFFFFF")
        self.show_all_button = tk.Button(self, text="Show All Books", command=self.show_all_books, bg="#008CBA", fg="#FFFFFF")
        self.delete_button = tk.Button(self, text="Delete Entry", command=self.delete_entry, bg="#FF0000", fg="#FFFFFF")
        self.delete_all_button = tk.Button(self, text="Delete All Entries", command=self.delete_all_entries, bg="#FF0000", fg="#FFFFFF")

        self.save_button = tk.Button(self, text="Save to File", command=self.save_to_file, bg="#4CAF50", fg="#FFFFFF")
        self.load_button = tk.Button(self, text="Load from File", command=self.load_from_file, bg="#008CBA", fg="#FFFFFF")

        self.result_listbox = tk.Listbox(self, width=10, height=10, bg=bg_color, fg=fg_color)

        self.book_count_label = tk.Label(self, text="Book Count: 0", bg="#F0F0F0", fg=fg_color)

        self.theme_switch_label = tk.Label(self, text="Dark Theme", bg="#F0F0F0", fg="#000000")
        self.theme_switch = ttk.Checkbutton(self, variable=self.dark_theme, command=self.toggle_theme, style='Switch.TCheckbutton')

        self.author_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        self.author_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        self.title_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.title_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")
        self.year_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")
        self.year_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        self.pages_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.pages_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        self.insert_button.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        self.search_button.grid(row=4, column=1, pady=10, padx=10, sticky="w")
        self.show_all_button.grid(row=5, column=0, pady=10, padx=10, sticky="w")
        self.delete_button.grid(row=5, column=1, pady=10, padx=10, sticky="w")
        self.delete_all_button.grid(row=6, column=0, pady=10, padx=10, sticky="w")
        self.save_button.grid(row=6, column=1, pady=10, padx=10, sticky="w")

        self.result_listbox.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.book_count_label.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.theme_switch_label.grid(row=9, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        self.theme_switch.grid(row=9, column=2, pady=10, padx=10, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(7, weight=1)

        style = ttk.Style()
        style.configure('Switch.TCheckbutton', background="#F0F0F0", foreground="#000000")

    def toggle_theme(self):
        if self.dark_theme.get():
            self.configure(bg="#000000")  
            fg_color = "#FFFFFF"
            bg_color = "#000000"
        else:
            self.configure(bg="#FFFFFF")
            fg_color = "#000000"
            bg_color = "#FFFFFF"

        self.author_label.config(fg="#000000")
        self.title_label.config(fg="#000000")
        self.year_label.config(fg="#000000")
        self.pages_label.config(fg="#000000")
        self.insert_button.config(bg="#4CAF50", fg="#FFFFFF")
        self.search_button.config(bg="#008CBA", fg="#FFFFFF")
        self.show_all_button.config(bg="#008CBA", fg="#FFFFFF")
        self.delete_button.config(bg="#FF0000", fg="#FFFFFF")
        self.delete_all_button.config(bg="#FF0000", fg="#FFFFFF")
        self.save_button.config(bg="#4CAF50", fg="#FFFFFF")
        self.load_button.config(bg="#008CBA", fg="#FFFFFF")
        self.result_listbox.config(bg=bg_color, fg=fg_color)
        self.book_count_label.config(bg="#F0F0F0", fg="#000000")
        self.theme_switch_label.config(bg="#F0F0F0", fg="#000000")


    def insert_entry(self):
        author = self.capitalize_text(self.author_entry.get())
        title = self.capitalize_text(self.title_entry.get())
        year = self.year_entry.get()
        pages = self.pages_entry.get()

        try:
            year = int(year)
            pages = int(pages)
        except ValueError:
            messagebox.showerror("Error", "Year and Pages must be integers.")
            return

        entry = {'Author': author, 'Title': title, 'Year': year, 'Pages': pages}
        self.reading_log.insert_entry(entry)

        self.author_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

        self.update_book_count()

    def search_entries(self):
        self.result_listbox.delete(0, tk.END)

        author = self.capitalize_text(self.author_entry.get())
        title = self.capitalize_text(self.title_entry.get())

        if not author and not title:
            messagebox.showwarning("Warning", "Please enter author or title.")
            return

        if author and not title:
            results = self.reading_log.get_author_books(author)
        else:
            results = self.reading_log.search_entries(author, title)

        for result in results:
            timestamp = result.get('Timestamp', 'N/A')
            self.result_listbox.insert(tk.END, f"{result['Author']} - {result['Title']}({result['Year']}) --- {result['Pages']} - Added: {timestamp}")

    def show_all_books(self):
        self.result_listbox.delete(0, tk.END)
        all_books = self.reading_log.search_entries()
        for book in all_books:
            timestamp = book.get('Timestamp', 'N/A')
            self.result_listbox.insert(tk.END, f"{book['Author']} - {book['Title']}({book['Year']}) --- {book['Pages']} - Added: {timestamp}")

    def delete_entry(self):
        author = self.capitalize_text(self.author_entry.get())
        title = self.capitalize_text(self.title_entry.get())
        self.reading_log.delete_entry(author, title)
        self.update_book_count()

    def delete_all_entries(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete all entries?")
        if confirmation:
            self.reading_log.delete_all_entries()
            self.update_book_count()

    def save_to_file(self):
        self.reading_log.save_to_file()

    def load_from_file(self):
        self.reading_log.load_from_file()
        messagebox.showinfo("Success", "Diary loaded from your Diary.")
        self.update_book_count()

    def capitalize_text(self, text):
        return text.title()

    def update_book_count(self):
        book_count = self.reading_log.get_book_count()
        self.book_count_label.config(text=f"Book Count: {book_count}")

if __name__ == "__main__":
    file_path = "C:/Users/thera/Desktop/Ukol/Reading-Log/diary.json"
    app = ReadingLogGUI(file_path)
    app.mainloop()