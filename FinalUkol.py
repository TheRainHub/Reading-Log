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
    def __init__(self, fileName):
        self.fileName = fileName
        self.diary = self.loadFromFile()

    def insertEntry(self, entry):
        existingTitles = {entry['Title'].lower() for entry in self.diary}
        if entry['Title'].lower() in existingTitles:
            messagebox.showerror("Error", "Duplicate entry. Entry not added.")
            return

        entry['Timestamp'] = self.getCurrentTimestamp()
        self.diary.append(entry)
        self.saveToFile()
        messagebox.showinfo("Success", "Entry added successfully.")

    def searchEntries(self, author=None, title=None):
        results = []
        for entry in self.diary:
            if (author is None or entry['Author'].lower() == author.lower()) and (title is None or entry['Title'].lower() == title.lower()):
                results.append(entry)
        return results

    def getAuthorBooks(self, author):
        results = []
        for entry in self.diary:
            if entry['Author'].lower() == author.lower():
                results.append(entry)
        return results

    def deleteEntry(self, author, title):
        self.diary = [entry for entry in self.diary if entry['Author'].lower() != author.lower() or entry['Title'].lower() != title.lower()]
        self.saveToFile()
        messagebox.showinfo("Success", "Entry deleted successfully.")

    def deleteAllEntries(self):
        self.diary = []
        self.saveToFile()
        messagebox.showinfo("Success", "All entries deleted.")

    def getBookCount(self):
        return len(self.diary)

    def saveToFile(self):
        with open(self.fileName, 'w') as file:
            json.dump(self.diary, file, indent=2)
        messagebox.showinfo("Success", f"Diary saved to {self.fileName}")

    def loadFromFile(self):
        try:
            with open(self.fileName, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def getCurrentTimestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ReadingLogGUI(tk.Tk):
    def __init__(self, fileName):
        super().__init__()
        self.title("Reading Log")
        self.geometry("400x600")
        self.darkTheme = tk.BooleanVar(value=False)
        self.configure(bg="#F0F0F0")

        self.readingLog = ReadingLog(fileName)

        self.createWidgets()

        self.updateBookCount()
        self.showAllBooks()

    def createWidgets(self):
        bgColor = "#FFFFFF"
        fgColor = "#000000"

        self.yearSearchEntryLabel = tk.Label(self, text = "Search by Year:", bg = "#F0F0F0", fg = "#000000")
        self.yearSearchEntry = tk.Entry(self, bg="#FFFFFF")


        self.authorLabel = tk.Label(self, text="Author:", bg="#F0F0F0", fg=fgColor)
        self.authorEntry = tk.Entry(self, bg=bgColor)

        self.titleLabel = tk.Label(self, text="Title:", bg="#F0F0F0", fg=fgColor)
        self.titleEntry = tk.Entry(self, bg=bgColor)

        self.yearLabel = tk.Label(self, text="Year:", bg="#F0F0F0", fg=fgColor)
        self.yearEntry = tk.Entry(self, bg=bgColor)

        self.pagesLabel = tk.Label(self, text="Number of Pages:", bg="#F0F0F0", fg=fgColor)
        self.pagesEntry = tk.Entry(self, bg=bgColor)

        
        self.insertButton = tk.Button(self, text="Insert Entry", command=self.insertEntry, bg="#4CAF50", fg="#FFFFFF")
        self.searchButton = tk.Button(self, text="Search Entries", command=self.searchEntries, bg="#008CBA", fg="#FFFFFF")
        self.showAllButton = tk.Button(self, text="Show All Books", command=self.showAllBooks, bg="#008CBA", fg="#FFFFFF")
        self.deleteButton = tk.Button(self, text="Delete Entry", command=self.deleteEntry, bg="#FF0000", fg="#FFFFFF")
        self.deleteAllButton = tk.Button(self, text="Delete All Entries", command=self.deleteAllEntries, bg="#FF0000", fg="#FFFFFF")

        self.saveButton = tk.Button(self, text="Save to File", command=self.saveToFile, bg="#4CAF50", fg="#FFFFFF")
        self.loadButton = tk.Button(self, text="Load from File", command=self.loadFromFile, bg="#008CBA", fg="#FFFFFF")

        self.resultListbox = tk.Listbox(self, width=10, height=10, bg=bgColor, fg=fgColor)

        self.bookCountLabel = tk.Label(self, text="Book Count: 0", bg="#F0F0F0", fg=fgColor)

        self.themeSwitchLabel = tk.Label(self, text="Dark Theme", bg="#F0F0F0", fg="#000000")
        self.themeSwitch = ttk.Checkbutton(self, variable=self.darkTheme, command=self.toggleTheme, style='Switch.TCheckbutton')
    

        self.authorLabel.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        self.authorEntry.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        self.titleLabel.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.titleEntry.grid(row=1, column=1, pady=5, padx=10, sticky="w")
        self.yearLabel.grid(row=2, column=0, pady=5, padx=10, sticky="w")
        self.yearEntry.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        self.pagesLabel.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.pagesEntry.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        self.insertButton.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        self.searchButton.grid(row=4, column=1, pady=10, padx=10, sticky="w")
        self.showAllButton.grid(row=5, column=0, pady=10, padx=10, sticky="w")
        self.deleteButton.grid(row=5, column=1, pady=10, padx=10, sticky="w")
        self.deleteAllButton.grid(row=6, column=0, pady=10, padx=10, sticky="w")
        self.saveButton.grid(row=6, column=1, pady=10, padx=10, sticky="w")
        

        self.resultListbox.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.bookCountLabel.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.themeSwitchLabel.grid(row=9, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        self.themeSwitch.grid(row=9, column=2, pady=10, padx=10, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(7, weight=1)

        style = ttk.Style()
        style.configure('Switch.TCheckbutton', background="#F0F0F0", foreground="#000000")

    def toggleTheme(self):
        if self.darkTheme.get():
            self.configure(bg="#000000")  
            fgColor = "#FFFFFF"
            bgColor = "#000000"
        else:
            self.configure(bg="#FFFFFF")
            fgColor = "#000000"
            bgColor = "#FFFFFF"

        self.authorLabel.config(fg="#000000")
        self.titleLabel.config(fg="#000000")
        self.yearLabel.config(fg="#000000")
        self.pagesLabel.config(fg="#000000")
        self.insertButton.config(bg="#4CAF50", fg="#FFFFFF")
        self.searchButton.config(bg="#008CBA", fg="#FFFFFF")
        self.showAllButton.config(bg="#008CBA", fg="#FFFFFF")
        self.deleteButton.config(bg="#FF0000", fg="#FFFFFF")
        self.deleteAllButton.config(bg="#FF0000", fg="#FFFFFF")
        self.saveButton.config(bg="#4CAF50", fg="#FFFFFF")
        self.loadButton.config(bg="#008CBA", fg="#FFFFFF")
        self.resultListbox.config(bg=bgColor, fg=fgColor)
        self.bookCountLabel.config(bg="#F0F0F0", fg="#000000")
        self.themeSwitchLabel.config(bg="#F0F0F0", fg="#000000")

    def insertEntry(self):
        author = self.capitalizeText(self.authorEntry.get())
        title = self.capitalizeText(self.titleEntry.get())
        year = self.yearEntry.get()
        pages = self.pagesEntry.get()

        try:
            year = int(year)
            pages = int(pages)


            if year < 0 or pages < 0:
                messagebox.showerror("Error", "Year and Pages must be non-negative integers.")
                return
            elif year > 2024:
                messagebox.showerror("Error", "Marty McFly?!!!? DOC?! Mc Brown?!!\nDid you actually invent a time machine?!\n")
                return
            
        except ValueError:
            messagebox.showerror("Error", "Year and Pages must be integers.")
            return

        entry = {'Author': author, 'Title': title, 'Year': year, 'Pages': pages}
        self.readingLog.insertEntry(entry)

        self.authorEntry.delete(0, tk.END)
        self.titleEntry.delete(0, tk.END)
        self.yearEntry.delete(0, tk.END)
        self.pagesEntry.delete(0, tk.END)

        self.updateBookCount()

    def searchEntries(self):
        self.resultListbox.delete(0, tk.END)

        author = self.capitalizeText(self.authorEntry.get())
        title = self.capitalizeText(self.titleEntry.get())

        if not author and not title:
            messagebox.showwarning("Warning", "Please enter author or title.")
            return

        if author and not title:
            results = self.readingLog.getAuthorBooks(author)
        else:
            results = self.readingLog.searchEntries(author, title)

        for result in results:
            timestamp = result.get('Timestamp', 'N/A')
            self.resultListbox.insert(tk.END, f"{result['Author']} - {result['Title']}({result['Year']}) --- {result['Pages']} - Added: {timestamp}")

    def showAllBooks(self):
        self.resultListbox.delete(0, tk.END)
        allBooks = self.readingLog.searchEntries()
        for book in allBooks:
            timestamp = book.get('Timestamp', 'N/A')
            self.resultListbox.insert(tk.END, f"{book['Author']} - {book['Title']}({book['Year']}) --- {book['Pages']} - Added: {timestamp}")

    def deleteEntry(self):
        author = self.capitalizeText(self.authorEntry.get())
        title = self.capitalizeText(self.titleEntry.get())
        self.readingLog.deleteEntry(author, title)
        self.updateBookCount()

    def deleteAllEntries(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete all entries?")
        if confirmation:
            self.readingLog.deleteAllEntries()
            self.updateBookCount()

    def saveToFile(self):
        self.readingLog.saveToFile()

    def loadFromFile(self):
        self.readingLog.loadFromFile()
        messagebox.showinfo("Success! Diary loaded from your Diary.")
        self.updateBookCount()

    def capitalizeText(self, text):
        return text.title()

    def updateBookCount(self):
        bookCount = self.readingLog.getBookCount()
        self.bookCountLabel.config(text=f"Book Count: {bookCount}")

if __name__ == "__main__":
    filePath = "C:/Users/thera/Desktop/Ukol/Reading-Log/diary.json"
    app = ReadingLogGUI(filePath)
    app.mainloop()