import numpy as np
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# External modules
from PointsFileLoader import PointsFileLoader
from KMeamsAlgo import kmeans

class KMeansTab:
    def __init__(self, parent):
        self.points = []
        self.k = tb.IntVar(value=3)
        self.x_input = tb.StringVar(master=parent)
        self.y_input = tb.StringVar(master=parent)

        frame = tb.Frame(parent, padding=10)
        frame.pack(fill=BOTH, expand=YES)

        top_frame = tb.Frame(frame)
        top_frame.pack(pady=10)
        tb.Button(top_frame, text="📂 Load CSV", command=self.load_data).pack(side=LEFT)
        self.file_label = tb.Label(top_frame, text="Or enter points manually ⬇")
        self.file_label.pack(side=LEFT, padx=10)

        input_frame = tb.Frame(frame)
        input_frame.pack(pady=5)
        tb.Label(input_frame, text="X:").pack(side=LEFT)
        tb.Entry(input_frame, textvariable=self.x_input, width=6).pack(side=LEFT)
        tb.Label(input_frame, text="Y:").pack(side=LEFT)
        tb.Entry(input_frame, textvariable=self.y_input, width=6).pack(side=LEFT)
        tb.Button(input_frame, text="➕ Add Point", command=self.add_point).pack(side=LEFT, padx=5)

        control_frame = tb.Frame(frame)
        control_frame.pack(pady=5)
        tb.Label(control_frame, text="K:").pack(side=LEFT)
        tb.Spinbox(control_frame, from_=1, to=10, textvariable=self.k, width=5).pack(side=LEFT)
        tb.Button(control_frame, text="🚀 Run KMeans", command=self.run_kmeans).pack(side=LEFT, padx=10)

        self.plot_frame = tb.Frame(frame)
        self.plot_frame.pack(pady=10, fill=BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(5.5, 5.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.update_plot()

    def load_data(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            loader = PointsFileLoader()
            df = loader.load(path)
            if df is not None:
                self.points = df[['x', 'y']].values.tolist()
                self.file_label.config(text=f"✅ Loaded: {path.split('/')[-1]}")
                self.update_plot()
            else:
                Messagebox.show_error("Failed to load file.")

    def add_point(self):
        try:
            x = float(self.x_input.get())
            y = float(self.y_input.get())
            self.points.append([x, y])
            self.x_input.set("")
            self.y_input.set("")
            self.update_plot()
        except ValueError:
            Messagebox.show_warning("Please enter valid numeric values for X and Y.")

    def run_kmeans(self):
        if not self.points:
            Messagebox.show_warning("Add points or load a dataset first.")
            return
        try:
            k = self.k.get()
            data = self.points
            centroids, clusters, labels = kmeans(data, k)
            self.update_plot(np.array(labels), np.array(centroids))
        except Exception as e:
            Messagebox.show_error(str(e))

    def update_plot(self, labels=None, centroids=None):
        self.ax.clear()
        data = np.array(self.points)

        if len(data) > 0:
            if labels is None:
                self.ax.scatter(data[:, 0], data[:, 1], c='blue')
            else:
                self.ax.scatter(data[:, 0], data[:, 1], c=labels, cmap="rainbow", alpha=0.6)
                self.ax.scatter(centroids[:, 0], centroids[:, 1], c='black', marker='X', s=100)

            max_val = max(data[:, 0].max(), data[:, 1].max(), 10)
            min_val = min(data[:, 0].min(), data[:, 1].min(), 0)
            self.ax.set_xlim(min_val - 1, max_val + 1)
            self.ax.set_ylim(min_val - 1, max_val + 1)
        else:
            self.ax.set_xlim(0, 10)
            self.ax.set_ylim(0, 10)

        self.ax.set_title("K-Means Clustering")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.canvas.draw()
