import tkinter as tk
from tkinter import ttk
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os.path

class LifeEventTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Life Event Tracker")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.life_events = []  # List to store the x-axis values (time)
        self.life_event_values = []  # List to store the y-axis values (life event values)
        self.current_value = 0

        # Load saved data
        self.load_data()

        # Create a Notebook widget to hold the tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack()

        # Create the tabs
        self.create_save_tab()
        self.create_load_tab()
        self.create_clear_tab()

        # Create event buttons
        self.create_event_buttons()

        # Create a Figure and set up the plot
        self.fig = Figure(figsize=(8, 4), dpi=100, facecolor="lightgrey")  # Set grey background color
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Life Event Value")
        self.ax.spines['bottom'].set_color('blue')  # Set blue color for plot lines
        self.ax.spines['top'].set_color('blue')
        self.ax.spines['left'].set_color('blue')
        self.ax.spines['right'].set_color('blue')
        self.ax.spines['bottom'].set_linewidth(1.5)  # Set thicker line width for plot lines
        self.ax.spines['top'].set_linewidth(1.5)
        self.ax.spines['left'].set_linewidth(1.5)
        self.ax.spines['right'].set_linewidth(1.5)
        self.ax.tick_params(axis='x', colors='blue')  # Set blue color for tick labels
        self.ax.tick_params(axis='y', colors='blue')
        self.ax.yaxis.grid(color='lightblue', linestyle='dashed')  # Set lighter grid lines
        self.line, = self.ax.plot([], [], '-o', color='blue')  # Blue line for the plot

        # Create a canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Random investing quotes
        self.investing_quotes = [
            "The stock market is filled with individuals who know the price of everything, but the value of nothing. - Philip Fisher",
            "The stock market is a device for transferring money from the impatient to the patient. - Warren Buffett",
            "In investing, what is comfortable is rarely profitable. - Robert Arnott",
            "Investing should be more like watching paint dry or watching grass grow. If you want excitement, take $800 and go to Las Vegas. - Paul Samuelson"
        ]

        self.quote_label = tk.Label(root, text="", font=("Arial", 10, "italic"))
        self.quote_label.pack()

        # Display a random quote initially
        self.display_random_quote()

        # Start the timer for real-time tracking
        self.update_interval = 1000  # Update interval in milliseconds
        self.root.after(self.update_interval, self.update_graph)

    def create_save_tab(self):
        save_tab = ttk.Frame(self.notebook)
        self.notebook.add(save_tab, text="Save")

        save_button = ttk.Button(save_tab, text="Save Chart", command=self.save_chart)
        save_button.pack(padx=10, pady=10)

    def create_load_tab(self):
        load_tab = ttk.Frame(self.notebook)
        self.notebook.add(load_tab, text="Load")

        load_button = ttk.Button(load_tab, text="Load Chart", command=self.load_chart)
        load_button.pack(padx=10, pady=10)

    def create_clear_tab(self):
        clear_tab = ttk.Frame(self.notebook)
        self.notebook.add(clear_tab, text="Clear")

        clear_button = ttk.Button(clear_tab, text="Clear Chart", command=self.clear_chart)
        clear_button.pack(padx=10, pady=10)

    def create_event_buttons(self):
        event_frame = ttk.Frame(self.root)
        event_frame.pack(pady=10)

        # Add the "Small Good Event" button
        small_good_button = ttk.Button(event_frame, text="Small Good Event", command=self.add_small_good_event)
        small_good_button.pack(side=tk.LEFT)
        small_good_button.bind("<Enter>", self.show_small_good_example)
        small_good_button.bind("<Leave>", self.hide_example)

        # Add the "Big Good Event" button
        big_good_button = ttk.Button(event_frame, text="Big Good Event", command=self.add_big_good_event)
        big_good_button.pack(side=tk.LEFT)
        big_good_button.bind("<Enter>", self.show_big_good_example)
        big_good_button.bind("<Leave>", self.hide_example)

        # Add the "Small Bad Event" button
        small_bad_button = ttk.Button(event_frame, text="Small Bad Event", command=self.add_small_bad_event)
        small_bad_button.pack(side=tk.LEFT)
        small_bad_button.bind("<Enter>", self.show_small_bad_example)
        small_bad_button.bind("<Leave>", self.hide_example)

        # Add the "Horrible Event" button
        horrible_button = ttk.Button(event_frame, text="Horrible Event", command=self.add_horrible_event)
        horrible_button.pack(side=tk.LEFT)
        horrible_button.bind("<Enter>", self.show_horrible_example)
        horrible_button.bind("<Leave>", self.hide_example)

    def add_small_good_event(self):
        event_value = self.current_value + random.uniform(0.1, 0.3)  # Add small positive value
        self.add_event(event_value)

    def add_big_good_event(self):
        event_value = self.current_value + random.uniform(0.5, 1.0)  # Add large positive value
        self.add_event(event_value)

    def add_small_bad_event(self):
        event_value = self.current_value - random.uniform(0.1, 0.3)  # Add small negative value
        self.add_event(event_value)

    def add_horrible_event(self):
        event_value = self.current_value - random.uniform(0.5, 1.0)  # Add large negative value
        self.add_event(event_value)

    def add_event(self, event_value):
        self.life_events.append(len(self.life_events))
        self.life_event_values.append(event_value)
        self.current_value = event_value

    def update_graph(self):
        # Add a flatline data point between user inputs
        if len(self.life_events) > 1:
            self.life_events.append(self.life_events[-1] + 0.1)
            self.life_event_values.append(self.life_event_values[-1])

        # Update the plot with new data
        self.line.set_data(self.life_events, self.life_event_values)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        # Schedule the next update
        self.root.after(self.update_interval, self.update_graph)

    def show_small_good_example(self, event):
        self.show_example_text("ex. Bought a new book")

    def show_big_good_example(self, event):
        self.show_example_text("ex. Got promoted at work")

    def show_small_bad_example(self, event):
        self.show_example_text("ex. Missed the bus")

    def show_horrible_example(self, event):
        self.show_example_text("ex. Experienced a major accident")

    def show_example_text(self, text):
        self.example_label.config(text=text)

    def hide_example(self, event):
        self.example_label.config(text="")

    def display_random_quote(self):
        quote = random.choice(self.investing_quotes)
        self.quote_label.config(text=quote)

    def hide_quote(self):
        self.quote_label.config(text="")

    def on_close(self):
        # Save the data before closing the program
        self.save_data()
        self.root.destroy()

    def save_chart(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if file_path:
            with open(file_path, "w") as file:
                for i in range(len(self.life_events)):
                    file.write(f"{self.life_events[i]},{self.life_event_values[i]}\n")

    def load_chart(self):
        file_path = tk.filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if file_path:
            self.clear_chart()
            with open(file_path, "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 2:
                        self.life_events.append(float(values[0]))
                        self.life_event_values.append(float(values[1]))
                        self.current_value = float(values[1])
            self.update_graph()

    def clear_chart(self):
        self.life_events = []
        self.life_event_values = []
        self.current_value = 0
        self.ax.cla()  # Clear the plot
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Life Event Value")
        self.ax.spines['bottom'].set_color('blue')  # Set blue color for plot lines
        self.ax.spines['top'].set_color('blue')
        self.ax.spines['left'].set_color('blue')
        self.ax.spines['right'].set_color('blue')
        self.ax.spines['bottom'].set_linewidth(1.5)  # Set thicker line width for plot lines
        self.ax.spines['top'].set_linewidth(1.5)
        self.ax.spines['left'].set_linewidth(1.5)
        self.ax.spines['right'].set_linewidth(1.5)
        self.ax.tick_params(axis='x', colors='blue')  # Set blue color for tick labels
        self.ax.tick_params(axis='y', colors='blue')
        self.ax.yaxis.grid(color='lightblue', linestyle='dashed')  # Set lighter grid lines
        self.line, = self.ax.plot([], [], '-o', color='blue')  # Blue line for the plot
        self.canvas.draw()

    def load_data(self):
        file_path = "data.txt"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 2:
                        self.life_events.append(float(values[0]))
                        self.life_event_values.append(float(values[1]))
                        self.current_value = float(values[1])

    def save_data(self):
        with open("data.txt", "w") as file:
            for i in range(len(self.life_events)):
                file.write(f"{self.life_events[i]},{self.life_event_values[i]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = LifeEventTrackerGUI(root)

    # Add a label to display example texts
    app.example_label = tk.Label(root, text="", font=("Arial", 10, "italic"))
    app.example_label.pack()

    root.mainloop()
