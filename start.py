import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import re

# Daten für die Tabelle
data = []

# Funktion zum Aktualisieren der Tabelle
def update_table():
    for i in tree.get_children():
        tree.delete(i)
    for row_data in data:
        tree.insert("", "end", values=row_data)

# Funktion zum Hinzufügen von Daten zur Tabelle
def add_data():
    global data
    try:
        engram_class_name = engram_entry.get()
        engram_hidden = hidden.get()
        points_cost_value = int(points_cost.get()) if points_cost.get().strip() != "" else 2
        level_requirement_value = int(level_requirement.get()) if level_requirement.get().strip() != "" else 2
        remove_pre_req_value = remove_pre_req.get()

        data.append([
            engram_class_name,
            engram_hidden,
            points_cost_value,
            level_requirement_value,
            remove_pre_req_value
        ])
        update_table()
    except ValueError:
        messagebox.showerror("Fehler", "EngramPointsCost und EngramLevelRequirement müssen Ganzzahlen sein.")

# Funktion zum Bearbeiten der ausgewählten Zeile
def edit_data():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror("Fehler", "Keine Zeile ausgewählt.")
        return
    selected_item = selected_items[0]
    selected_index = tree.index(selected_item)
    try:
        engram_class_name = engram_entry.get()
        engram_hidden = hidden.get()
        points_cost_value = int(points_cost.get()) if points_cost.get().strip() != "" else 2
        level_requirement_value = int(level_requirement.get()) if level_requirement.get().strip() != "" else 2
        remove_pre_req_value = remove_pre_req.get()

        data[selected_index] = [
            engram_class_name,
            engram_hidden,
            points_cost_value,
            level_requirement_value,
            remove_pre_req_value
        ]
        update_table()
        clear_entries()
    except ValueError:
        messagebox.showerror("Fehler", "EngramPointsCost und EngramLevelRequirement müssen Ganzzahlen sein.")

# Funktion zum Löschen der ausgewählten Zeile
def delete_data():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror("Fehler", "Keine Zeile ausgewählt.")
        return
    selected_item = selected_items[0]
    selected_index = tree.index(selected_item)
    data.pop(selected_index)
    update_table()
    clear_entries()

# Funktion zum Laden der Zeile in die Eingabefelder bei Doppelklick
def load_data(event):
    selected_items = tree.selection()
    if selected_items:
        item = selected_items[0]
        values = tree.item(item, "values")
        if values:
            engram_entry.delete(0, "end")
            engram_entry.insert(0, values[0])
            hidden.set(values[1])
            points_cost.delete(0, "end")
            points_cost.insert(0, values[2])
            level_requirement.delete(0, "end")
            level_requirement.insert(0, values[3])
            remove_pre_req.set(values[4])

# Funktion zum Löschen der Eingabefelder
def clear_entries():
    engram_entry.delete(0, "end")
    hidden.set(False)
    points_cost.delete(0, "end")
    level_requirement.delete(0, "end")
    remove_pre_req.set(False)

# Funktion zum Extrahieren und Hinzufügen von Daten aus einem String
def extract_and_add_data(input_string):
    global tree
    try:
        match = re.search(r'EngramClassName="(.*?)"', input_string)
        if match:
            engram_class_name = match.group(1)
        else:
            raise ValueError("EngramClassName nicht gefunden.")

        engram_hidden = "EngramHidden=true" in input_string
        points_cost_match = re.search(r'EngramPointsCost=(\d+)', input_string)
        engram_points_cost = int(points_cost_match.group(1)) if points_cost_match else 2
        level_requirement_match = re.search(r'EngramLevelRequirement=(\d+)', input_string)
        engram_level_requirement = int(level_requirement_match.group(1)) if level_requirement_match else 2
        remove_pre_req = "RemoveEngramPreReq=true" in input_string

        data.append([
            engram_class_name,
            engram_hidden,
            engram_points_cost,
            engram_level_requirement,
            remove_pre_req
        ])
        update_table()
    except (ValueError, IndexError):
        messagebox.showerror("Fehler", "Ungültiges Datenformat im Eingabestring.")

# Funktion zum Laden von Daten aus einer Datei
def load_data_from_file():
    global data
    file_path = filedialog.askopenfilename(title="Entry laden \"OverrideNamedEngramEntries\"")
    if file_path:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                extract_and_add_data(line.strip())
        update_table()

# Funktion zum Laden von zusätzlichen Daten aus einer Datei
def load_additional_data_from_file():
    global data
    file_path = filedialog.askopenfilename(title="Engram Entrys laden \"EngramEntry_Campfire_C\"")
    if file_path:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                engram_class_name = line.strip()
                data.append([
                    engram_class_name,
                    False,
                    2,
                    2,
                    False
                ])
        update_table()

# Funktion zum Speichern der Daten in eine Datei
def save_data_to_file():
    global data
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Textdateien", "*.txt")], title="Daten speichern")
    if file_path:
        with open(file_path, "w") as file:
            for row_data in data:
                file.write(f'OverrideNamedEngramEntries=(EngramClassName="{row_data[0]}",EngramHidden={row_data[1]},EngramPointsCost={row_data[2]},EngramLevelRequirement={row_data[3]},RemoveEngramPreReq={row_data[4]})\n')

# GUI erstellen
root = tk.Tk()
root.title("Engram Entries")

# Automatische Anpassung der Größe an die Fenstergröße
root.geometry("1024x768")  # Startgröße
# root.grid_rowconfigure(6, weight=1)
# root.grid_columnconfigure(0, weight=1)

# Rahmen für die Tabelle erstellen
table_frame = ttk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

# Tabelle erstellen
columns = ("EngramClassName", "EngramHidden", "EngramPointsCost", "EngramLevelRequirement", "RemoveEngramPreReq")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)  # Breite der Spalten auf 150 setzen
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar für die Tabelle erstellen
tree_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=tree_scrollbar.set)

# Eingabefelder erstellen
input_frame = tk.Frame(root)
input_frame.pack()

tk.Label(input_frame, text="EngramClassName").pack(side=tk.LEFT)
engram_entry = tk.Entry(input_frame)
engram_entry.pack(side=tk.LEFT)

tk.Label(input_frame, text="EngramHidden").pack(side=tk.LEFT)
hidden = tk.BooleanVar()
hidden_checkbox = tk.Checkbutton(input_frame, variable=hidden)
hidden_checkbox.pack(side=tk.LEFT)

tk.Label(input_frame, text="EngramPointsCost").pack(side=tk.LEFT)
points_cost = tk.Entry(input_frame)
points_cost.pack(side=tk.LEFT)

tk.Label(input_frame, text="EngramLevelRequirement").pack(side=tk.LEFT)
level_requirement = tk.Entry(input_frame)
level_requirement.pack(side=tk.LEFT)

tk.Label(input_frame, text="RemoveEngramPreReq").pack(side=tk.LEFT)
remove_pre_req = tk.BooleanVar()
remove_pre_req_checkbox = tk.Checkbutton(input_frame, variable=remove_pre_req)
remove_pre_req_checkbox.pack(side=tk.LEFT)

# Schaltflächen für Aktionen erstellen
action_frame = tk.Frame(root)
action_frame.pack()

add_button = tk.Button(action_frame, text="Hinzufügen", command=add_data)
edit_button = tk.Button(action_frame, text="Bearbeiten", command=edit_data)
delete_button = tk.Button(action_frame, text="Löschen", command=delete_data)
load_data_button = tk.Button(action_frame, text="Entrys laden \"OverrideNamedEngramEntries\"", command=load_data_from_file)
load_additional_data_button = tk.Button(action_frame, text="Engram Entrys laden \"EngramEntry_Campfire_C\"", command=load_additional_data_from_file)
save_data_button = tk.Button(action_frame, text="Daten Speichern", command=save_data_to_file)

add_button.pack(side=tk.LEFT)
edit_button.pack(side=tk.LEFT)
delete_button.pack(side=tk.LEFT)
load_data_button.pack(side=tk.LEFT)
load_additional_data_button.pack(side=tk.LEFT)
save_data_button.pack(side=tk.LEFT)

# Doppelklick-Ereignis für die Tabelle hinzufügen
tree.bind("<<TreeviewSelect>>", load_data)

# GUI starten
root.mainloop()
