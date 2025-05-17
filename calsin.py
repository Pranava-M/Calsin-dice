import math
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("3D Scientific Calculator")
        self.geometry("500x700")
        self.configure(bg='#2e2e2e')
        self.history = []
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.style = ttk.Style()
        
        self.configure_styles()
        self.create_widgets()
        self.bind_keys()

    def configure_styles(self):
        self.style.theme_create('calculator', settings={
            "TButton": {
                "configure": {
                    "foreground": "#ffffff",
                    "anchor": "center",
                    "font": ('Helvetica', 12, 'bold'),
                    "borderwidth": 1,
                    "relief": "raised",
                    "padding": 10
                },
                "map": {
                    "foreground": [('pressed', '#ffffff'), ('active', '#ffffff')],
                    "background": [
                        ('pressed', '!disabled', '#4a4a4a'),
                        ('active', '#6a6a6a')
                    ]
                }
            }
        })
        self.style.theme_use('calculator')
        
        # Custom styles
        self.style.configure('TButton', background='#4a4a4a')
        self.style.configure('Display.TEntry', 
                           font=('Digital-7', 24),
                           foreground='#00ff00',
                           background='#1a1a1a',
                           borderwidth=5,
                           relief='sunken')

    def create_widgets(self):
        # Main display
        self.display = ttk.Entry(self, style='Display.TEntry', 
                               justify='right', state='readonly')
        self.display.pack(fill='x', padx=10, pady=20, ipady=15)
        
        # Secondary display
        self.expression_display = ttk.Label(self, text="", 
                                          font=('Arial', 12),
                                          background='#2e2e2e',
                                          foreground='#888888')
        self.expression_display.pack(fill='x', padx=10)
        
        # Button frames
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Number pad
        num_frame = ttk.Frame(main_frame)
        num_frame.grid(row=0, column=0, sticky='nsew')

        buttons = [
            ('7', '8', '9', '⌫', 'C'),
            ('4', '5', '6', '×', '÷'),
            ('1', '2', '3', '+', '-'),
            ('0', '.', 'π', '^', '='),
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                btn = ttk.Button(num_frame, text=text,
                               command=lambda t=text: self.button_click(t))
                btn.grid(row=row_idx, column=col_idx, 
                        sticky='nsew', padx=2, pady=2)

        # Scientific functions
        sci_frame = ttk.Frame(main_frame)
        sci_frame.grid(row=0, column=1, sticky='nsew')

        sci_buttons = [
            ('sin', 'cos', 'tan'),
            ('asin', 'acos', 'atan'),
            ('log', 'ln', '√'),
            ('!', 'e', 'rad'),
            ('(', ')', '±')
        ]

        for row_idx, row in enumerate(sci_buttons):
            for col_idx, text in enumerate(row):
                btn = ttk.Button(sci_frame, text=text,
                               command=lambda t=text: self.sci_button_click(t))
                btn.grid(row=row_idx, column=col_idx, 
                        sticky='nsew', padx=2, pady=2)

        # Configure grid weights
        for i in range(4):
            num_frame.rowconfigure(i, weight=1)
            sci_frame.rowconfigure(i, weight=1)
        for i in range(5):
            num_frame.columnconfigure(i, weight=1)
            sci_frame.columnconfigure(i, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # History
        self.history_text = scrolledtext.ScrolledText(self, 
                                                    height=8,
                                                    bg='#1a1a1a',
                                                    fg='#00ff00',
                                                    insertbackground='white',
                                                    font=('Consolas', 10))
        self.history_text.pack(fill='both', expand=True, padx=10, pady=10)

    def bind_keys(self):
        self.bind('<Return>', lambda e: self.button_click('='))
        self.bind('<BackSpace>', lambda e: self.button_click('⌫'))
        for char in '0123456789+-*/.^()':
            self.bind(char, lambda e, c=char: self.button_click(c))

    def button_click(self, value):
        if value == 'C':
            self.clear_display()
        elif value == '⌫':
            self.backspace()
        elif value == '=':
            self.calculate_result()
        elif value in ['+', '-', '×', '÷', '^']:
            self.set_operation(value)
        else:
            self.add_to_display(value)

    def sci_button_click(self, func):
        try:
            value = self.current_input or "0"
            expression = ""
            
            if func == 'sin':
                result = math.sin(math.radians(float(value)))
            elif func == 'cos':
                result = math.cos(math.radians(float(value)))
            elif func == 'tan':
                result = math.tan(math.radians(float(value)))
            elif func == 'asin':
                result = math.degrees(math.asin(float(value)))
            elif func == 'acos':
                result = math.degrees(math.acos(float(value)))
            elif func == 'atan':
                result = math.degrees(math.atan(float(value)))
            elif func == 'log':
                result = math.log10(float(value))
            elif func == 'ln':
                result = math.log(float(value))
            elif func == '√':
                result = math.sqrt(float(value))
            elif func == '!':
                result = math.factorial(int(float(value)))
            elif func == 'π':
                result = math.pi
            elif func == 'e':
                result = math.e
            elif func == 'rad':
                result = math.radians(float(value))
            elif func == '±':
                result = -float(value)
            else:
                result = "Invalid operation"
            
            self.current_input = str(result)
            self.update_display()
            self.update_history(f"{func}({value}) = {result}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_to_display(self, value):
        self.current_input += str(value)
        self.update_display()

    def clear_display(self):
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.update_display()
        self.expression_display.config(text="")

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.update_display()

    def update_display(self):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
        self.display.config(state='readonly')

    def set_operation(self, operation):
        if self.current_input:
            self.first_number = float(self.current_input)
            self.operation = operation.replace('×', '*').replace('÷', '/')
            self.expression_display.config(text=f"{self.first_number} {operation}")
            self.current_input = ""
            self.update_display()

    def calculate_result(self):
        if self.operation and self.first_number is not None and self.current_input:
            try:
                second_number = float(self.current_input)
                operations = {
                    '+': self.first_number + second_number,
                    '-': self.first_number - second_number,
                    '*': self.first_number * second_number,
                    '/': self.first_number / second_number,
                    '^': self.first_number ** second_number
                }
                result = operations[self.operation]
                full_expression = f"{self.first_number} {self.operation} {second_number} = {result}"
                self.current_input = str(result)
                self.update_display()
                self.update_history(full_expression)
                self.expression_display.config(text="")
                self.first_number = None
                self.operation = None
            except ZeroDivisionError:
                messagebox.showerror("Error", "Division by zero!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_history(self, entry):
        self.history.append(entry)
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)
        self.history_text.configure(state='disabled')

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()