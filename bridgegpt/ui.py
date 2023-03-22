import tkinter as tk

class Window(tk.Tk):
    def __init__(self, loop, ui_service):
        self.ui_service = ui_service
        self.root = tk.Tk()
        self.root.title("BridgeGPT 0.1")
        self.root.configure(bg="#222")

        # Create chat history displays
        self.chat_history = tk.Text(self.root, state=tk.DISABLED, bg="#222", fg="white")
        self.chat_history_scrollbar = tk.Scrollbar(self.root)
        self.chat_history_scrollbar.grid(row=0, column=1, padx=(0, 0), pady=10, sticky="NS")
        self.chat_history = tk.Text(self.root, state=tk.DISABLED, bg="#222", fg="white", yscrollcommand=self.chat_history_scrollbar.set)
        self.chat_history.grid(row=0, column=0, padx=(0, 0), pady=10, sticky="NSEW")
        self.chat_history_scrollbar.config(command=self.chat_history.yview)

        self.system_history = tk.Text(self.root, state=tk.DISABLED, bg="#222", fg="white")
        self.system_history_scrollbar = tk.Scrollbar(self.root)
        self.system_history_scrollbar.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="NS")
        self.system_history = tk.Text(self.root, state=tk.DISABLED, bg="#222", fg="white", yscrollcommand=self.system_history_scrollbar.set)
        self.system_history.grid(row=0, column=2, padx=(0, 0), pady=10, sticky="NSEW")
        self.system_history_scrollbar.config(command=self.system_history.yview)

        # Create input field
        self.input_field = tk.Entry(self.root)
        self.input_field.bind("<Return>", self.ui_service.send_message)
        self.input_field.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        # Create send button
        self.send_button = tk.Button(
            self.root, text="Send", command=self.ui_service.send_message, bg="#444",
            fg="white", activebackground="#666", activeforeground="white"
        )
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="E")

        # Set column and row weights
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Bind event for window resizing
        #self.root.bind('<Configure>', self.resize_dialogs)

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Load")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.options_menu.add_command(label="Settings")
        self.options_menu.add_command(label="Tool")
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.root.config(menu=self.menu_bar)

    def display_message(self, message, from_input=False):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)
        if from_input:
            self.input_field.delete(0, tk.END)

    def display_system_message(self, message):
        self.system_history.config(state=tk.NORMAL)
        self.system_history.insert(tk.END, message + "\n")
        self.system_history.config(state=tk.DISABLED)
        self.system_history.see(tk.END)

    def resize_dialogs(self, event):
        width = event.width
        height = event.height - self.input_field.winfo_height() - 30
        self.master.grid_propagate(0)
        self.chat_history.config(width=int(round(width*2/3)), height=height)
        self.system_history.config(width=int(round(width/3)), height=height)
