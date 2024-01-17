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
from tkinter import filedialog, messagebox
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
        messagebox.showinfo("Success", f"Diary saved to {self.filename}.")

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
        self.geometry("600x800")  # Zvětšeno šířku okna

        # Barevný motiv
        self.configure(bg="#F0F0F0")  # Barva pozadí

        self.reading_log = ReadingLog(filename)

        self.create_widgets()

    def create_widgets(self):
        # Barvy pro prvky GUI
        bg_color = "#FFFFFF"  # Bílá barva pro pozadí prvků
        fg_color = "#000000"  # Černá barva pro text

        self.author_label = tk.Label(self, text="Author:", bg="#F0F0F0", fg=fg_color)
        self.author_entry = tk.Entry(self, bg=bg_color)

        self.title_label = tk.Label(self, text="Title:", bg="#F0F0F0", fg=fg_color)
        self.title_entry = tk.Entry(self, bg=bg_color)

        self.year_label = tk.Label(self, text="Year:", bg="#F0F0F0", fg=fg_color)
        self.year_entry = tk.Entry(self, bg=bg_color)

        self.pages_label = tk.Label(self, text="Number of Pages:", bg="#F0F0F0", fg=fg_color)
        self.pages_entry = tk.Entry(self, bg=bg_color)

        self.insert_button = tk.Button(self, text="Insert Entry", command=self.insert_entry, bg="#4CAF50", fg="#FFFFFF")  # Zelené tlačítko
        self.search_button = tk.Button(self, text="Search Entries", command=self.search_entries, bg="#008CBA", fg="#FFFFFF")  # Modré tlačítko
        self.delete_button = tk.Button(self, text="Delete Entry", command=self.delete_entry, bg="#FF0000", fg="#FFFFFF")  # Červené tlačítko
        self.delete_all_button = tk.Button(self, text="Delete All Entries", command=self.delete_all_entries, bg="#FF0000", fg="#FFFFFF")  # Červené tlačítko

        self.save_button = tk.Button(self, text="Save to File", command=self.save_to_file, bg="#4CAF50", fg="#FFFFFF")  # Zelené tlačítko
        self.load_button = tk.Button(self, text="Load from File", command=self.load_from_file, bg="#008CBA", fg="#FFFFFF")  # Modré tlačítko

        # Seznam výsledků
        self.result_listbox = tk.Listbox(self, width=10, height=10, bg=bg_color, fg=fg_color)

        # Widget s počtem knih v deníku
        self.book_count_label = tk.Label(self, text="Book Count: 0", bg="#F0F0F0", fg=fg_color)

        # Umístění prvků do mřížky
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
        self.delete_button.grid(row=5, column=0, pady=10, padx=10, sticky="w")
        self.delete_all_button.grid(row=5, column=1, pady=10, padx=10, sticky="w")
        self.save_button.grid(row=6, column=0, pady=10, padx=10, sticky="w")
        self.load_button.grid(row=6, column=1, pady=10, padx=10, sticky="w")

        self.result_listbox.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.book_count_label.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Konfigurace mřížky pro pružnost
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(7, weight=1)

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

        # Aktualizace počtu knih v deníku
        self.update_book_count()

    def search_entries(self):
        self.result_listbox.delete(0, tk.END)

        author = self.capitalize_text(self.author_entry.get())
        title = self.capitalize_text(self.title_entry.get())
        results = self.reading_log.search_entries(author, title)

        for result in results:
            timestamp = result.get('Timestamp', 'N/A')
            self.result_listbox.insert(tk.END, f"{result['Author']} - {result['Title']}({result['Year']}) --- {result['Pages']} - Added: {timestamp}")

    def delete_entry(self):
        author = self.capitalize_text(self.author_entry.get())
        title = self.capitalize_text(self.title_entry.get())
        self.reading_log.delete_entry(author, title)

        # Aktualizace počtu knih v deníku
        self.update_book_count()

    def delete_all_entries(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete all entries?")
        if confirmation:
            self.reading_log.delete_all_entries()

            # Aktualizace počtu knih v deníku
            self.update_book_count()

    def save_to_file(self):
        self.reading_log.save_to_file()

    def load_from_file(self):
        self.reading_log.load_from_file()
        messagebox.showinfo("Success", "Diary loaded from your Diary.")

        # Aktualizace počtu knih v deníku
        self.update_book_count()

    def capitalize_text(self, text):
        return text.title()

    def update_book_count(self):
        book_count = self.reading_log.get_book_count()
        self.book_count_label.config(text=f"Book Count: {book_count}")

if __name__ == "__main__":
    file_path = "C:/Users/thera/Desktop/Ukol/diary.json"
    app = ReadingLogGUI(file_path)
    app.mainloop()
