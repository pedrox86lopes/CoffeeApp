import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


class CoffeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Blend Advisor")
        self.root.geometry("600x400")

        # Database setup
        self.conn = sqlite3.connect("coffee.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS coffee (
                id INTEGER PRIMARY KEY,
                type TEXT,
                quantity INTEGER,
                state TEXT
            )
        ''')
        self.conn.commit()

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Coffee Blend Advisor", font=("Arial", 20))
        title_label.pack(pady=10)

        # Coffee type input
        coffee_type_label = tk.Label(self.root, text="Coffee Type:")
        coffee_type_label.pack()
        self.coffee_type_entry = tk.Entry(self.root)
        self.coffee_type_entry.pack()

        # Coffee quantity input
        coffee_quantity_label = tk.Label(self.root, text="Coffee Quantity (g):")
        coffee_quantity_label.pack()
        self.coffee_quantity_entry = tk.Entry(self.root)
        self.coffee_quantity_entry.pack()

        # Coffee state input
        coffee_state_label = tk.Label(self.root, text="State (Bean/Powder):")
        coffee_state_label.pack()
        self.coffee_state_combo = ttk.Combobox(self.root, values=["Bean", "Powder"])
        self.coffee_state_combo.pack()

        # Buttons
        add_button = tk.Button(self.root, text="Add Coffee", command=self.add_coffee)
        add_button.pack(pady=5)

        suggest_button = tk.Button(self.root, text="Suggest Blend", command=self.suggest_blend)
        suggest_button.pack(pady=5)

        # Inventory display
        self.inventory_text = tk.Text(self.root, height=10, width=70)
        self.inventory_text.pack(pady=10)

        self.update_inventory_display()

    def add_coffee(self):
        coffee_type = self.coffee_type_entry.get().strip()
        coffee_quantity = self.coffee_quantity_entry.get().strip()
        coffee_state = self.coffee_state_combo.get().strip()

        if not coffee_type or not coffee_quantity or not coffee_state:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            coffee_quantity = int(coffee_quantity)
            self.cursor.execute("INSERT INTO coffee (type, quantity, state) VALUES (?, ?, ?)",
                                (coffee_type, coffee_quantity, coffee_state))
            self.conn.commit()
            messagebox.showinfo("Success", "Coffee added successfully!")
            self.update_inventory_display()
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a number.")

    def update_inventory_display(self):
        self.inventory_text.delete(1.0, tk.END)
        self.cursor.execute("SELECT type, quantity, state FROM coffee")
        rows = self.cursor.fetchall()
        for row in rows:
            self.inventory_text.insert(tk.END, f"Type: {row[0]}, Quantity: {row[1]}g, State: {row[2]}\n")

    def suggest_blend(self):
        self.cursor.execute("SELECT type, quantity FROM coffee ORDER BY quantity DESC")
        rows = self.cursor.fetchall()

        if not rows:
            messagebox.showinfo("No Data", "No coffee data available.")
            return

        suggested_blend = ", ".join(f"{row[0]} ({row[1]}g)" for row in rows[:3])
        messagebox.showinfo("Suggested Blend", f"Best Blend: {suggested_blend}")

    def close_app(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
