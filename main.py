import customtkinter as ctk
import random
from sorting_algorithms import *

# Initialize Logic
dataset = []
stop_flag = False
sorting_alg = SortingAlgorithms()

# GUI Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title('Modern Sorting Visualizer')
root.state('zoomed')  # This makes the window open maximized (fullscreen)
root.geometry('1100x650')

# Define Variables
sorting_algorithm = ctk.StringVar(value='Bubble Sort')
graph_type = ctk.StringVar(value='Bar')

# --- Helper Functions for Slider Labels ---
def update_size_label(val):
    size_label.configure(text=f"Dataset Size: {int(val)}")

def update_speed_label(val):
    speed_label.configure(text=f"Speed: {round(val, 2)}s")

# --- Logic Functions ---
def start_btn():
    global dataset, stop_flag
    generateBtn.configure(state="disabled")
    startBtn.configure(state="disabled")
    stopBtn.configure(state="normal")
    resetBtn.configure(state="disabled")

    if stop_flag: stop_flag = False
    
    speed = float(animation_speed.get())
    algo = sorting_algorithm.get()
    
    if algo == 'Bubble Sort':
        sorting_alg.bubble_sort(dataset, draw_data, speed, stop_flag)
        update_header_labels(sorting_alg.get_comparisons_count(), 'O(n^2)')
    elif algo == 'Quick Sort':
        sorting_alg.quick_sort(dataset, 0, len(dataset) - 1, draw_data, speed)
        draw_data(dataset, ['green' for _ in range(len(dataset))])
        update_header_labels(sorting_alg.get_comparisons_count(), 'O(n log n)')
    elif algo == 'Insertion Sort':
        # Remove the indices (0 and len-1)
        sorting_alg.insertion_sort(dataset, draw_data, speed)
        draw_data(dataset, ['green' for _ in range(len(dataset))])
        update_header_labels(sorting_alg.get_comparisons_count(), 'O(n^2)')

    elif algo == 'Selection Sort':
        # Remove the indices (0 and len-1)
        sorting_alg.selection_sort(dataset, draw_data, speed)
        draw_data(dataset, ['green' for _ in range(len(dataset))])
        update_header_labels(sorting_alg.get_comparisons_count(), 'O(n^2)')

    elif algo == 'Merge Sort':
        # Remove the indices (0 and len-1) based on your sorting_algorithms.py definition
        sorting_alg.merge_sort(dataset, draw_data, speed)
        draw_data(dataset, ['green' for _ in range(len(dataset))])
        update_header_labels(sorting_alg.get_comparisons_count(), 'O(n log n)')
    # ... (other algorithms follow same pattern)

    generateBtn.configure(state="normal")
    startBtn.configure(state="normal")
    stopBtn.configure(state="disabled")
    resetBtn.configure(state="normal")

def stop_btn():
    global stop_flag
    stop_flag = True

def reset_btn():
    global dataset
    dataset = []
    comparison_label.configure(text="Comparisons: 0")
    algorithm_complexity_label.configure(text="Complexity: -")
    cv.delete("all")

def draw_data(data_set, clr):
    cv.delete('all')
    if not data_set: return
    
    cv_height = 400
    cv_width = 800
    x_width = cv_width / (len(data_set) + 1)
    offset = 30
    max_val = max(data_set) if max(data_set) > 0 else 1
    data = [i / max_val for i in data_set]

    for i, h in enumerate(data):
        x0 = i * x_width + offset
        y0 = cv_height - h * 350
        color = clr[i] if i < len(clr) else '#764AF1'
        
        if graph_type.get() == 'Bar':
            cv.create_rectangle(x0, y0, x0 + (x_width - 2), cv_height, fill=color, outline="")
        elif graph_type.get() == 'Stem':
            cv.create_line(x0 + (x_width/2), cv_height, x0 + (x_width/2), y0, fill=color, width=2)
            cv.create_oval(x0 + (x_width/2) - 3, y0 - 3, x0 + (x_width/2) + 3, y0 + 3, fill=color)
        elif graph_type.get() == 'Scatter':
            cv.create_oval(x0, y0, x0 + 6, y0 + 6, fill=color)
            
        if len(data_set) < 30:
            cv.create_text(x0 + (x_width/2), y0 - 10, text=str(data_set[i]), fill="white", font=("Arial", 9))
    root.update_idletasks()

def generate_dataset():
    global dataset
    dataset = [random.randrange(int(min_val.get()), int(max_val.get()) + 1) for _ in range(int(dataset_size.get()))]
    draw_data(dataset, ['#FF597B' for _ in range(len(dataset))])

def process_input():
    global dataset
    try:
        dataset = [int(x) for x in entry.get().split(",")]
        draw_data(dataset, ['#FF597B' for _ in range(len(dataset))])
    except: pass

def update_header_labels(c, t):
    comparison_label.configure(text=f"Comparisons: {c}")
    algorithm_complexity_label.configure(text=f"Complexity: {t}")

# --- Modern GUI Implementation ---
sidebar = ctk.CTkFrame(root, width=250, corner_radius=10)
sidebar.pack(side="left", fill="y", padx=15, pady=15)

ctk.CTkLabel(sidebar, text="Controls", font=("Roboto", 18, "bold")).pack(pady=15)

sorting_algo = ctk.CTkComboBox(sidebar, variable=sorting_algorithm, values=['Bubble Sort', 'Quick Sort', 'Insertion Sort', 'Selection Sort', 'Merge Sort'])
sorting_algo.pack(pady=5, padx=20)

graph = ctk.CTkComboBox(sidebar, variable=graph_type, values=['Bar', 'Scatter', 'Stem'])
graph.pack(pady=5, padx=20)

# Dataset Size Slider + Label
size_label = ctk.CTkLabel(sidebar, text="Dataset Size: 25")
size_label.pack(pady=(15, 0))
dataset_size = ctk.CTkSlider(sidebar, from_=5, to=50, number_of_steps=45, command=update_size_label)
dataset_size.set(25)
dataset_size.pack(pady=5, padx=20)

min_val = ctk.CTkEntry(sidebar, placeholder_text="Min Value (1)")
min_val.pack(pady=5, padx=20)
max_val = ctk.CTkEntry(sidebar, placeholder_text="Max Value (100)")
max_val.pack(pady=5, padx=20)

# Speed Slider + Label
speed_label = ctk.CTkLabel(sidebar, text="Speed: 0.5s")
speed_label.pack(pady=(15, 0))
animation_speed = ctk.CTkSlider(sidebar, from_=0.01, to=1.0, command=update_speed_label)
animation_speed.set(0.5)
animation_speed.pack(pady=5, padx=20)

# Buttons
generateBtn = ctk.CTkButton(sidebar, text='Generate Dataset', command=generate_dataset, fg_color='#764AF1')
generateBtn.pack(pady=10, padx=20)
startBtn = ctk.CTkButton(sidebar, text='Start Sorting', command=start_btn, fg_color='#019267')
startBtn.pack(pady=5, padx=20)
stopBtn = ctk.CTkButton(sidebar, text='Stop', command=stop_btn, fg_color='#FF597B', state="disabled")
stopBtn.pack(pady=5, padx=20)
resetBtn = ctk.CTkButton(sidebar, text='Reset', command=reset_btn, fg_color='#555')
resetBtn.pack(pady=5, padx=20)

entry = ctk.CTkEntry(sidebar, placeholder_text="10, 5, 8, 2...")
entry.pack(pady=15, padx=20)
ctk.CTkButton(sidebar, text="Process Input", command=process_input, fg_color="#3B8ED0").pack(pady=5, padx=20)

# Right Panel
right_panel = ctk.CTkFrame(root, fg_color="transparent")
right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

header = ctk.CTkFrame(right_panel, fg_color="#2b2b2b", corner_radius=10)
header.pack(fill="x", pady=(0, 20))

comparison_label = ctk.CTkLabel(header, text="Comparisons: 0", font=('Roboto', 16, "bold"))
comparison_label.pack(side="left", padx=20, pady=10)
algorithm_complexity_label = ctk.CTkLabel(header, text="Complexity: -", font=('Roboto', 16, "bold"))
algorithm_complexity_label.pack(side="right", padx=20, pady=10)

cv = ctk.CTkCanvas(right_panel, bg='#1a1a1a', highlightthickness=0)
cv.pack(fill="both", expand=True)

root.mainloop()