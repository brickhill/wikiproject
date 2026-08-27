import json
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, simpledialog

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


DATA_FILE = Path.home() / "time_tracker.json"


class TimeTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        self.root.geometry("950x700")

        self.tasks = {}
        self.active_task = None
        self.last_update = None

        self.load_data()

        # -----------------------------
        # Top controls
        # -----------------------------

        controls = tk.Frame(root)
        controls.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=10,
            pady=10
        )

        tk.Button(
            controls,
            text="Add Task",
            command=self.add_task
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls,
            text="Remove Task",
            command=self.remove_task
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls,
            text="Stop",
            command=self.stop_task
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls,
            text="Save",
            command=self.save_data
        ).pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(
            controls,
            text="No task running"
        )

        self.status.pack(
            side=tk.LEFT,
            padx=20
        )

        # -----------------------------
        # Main area
        # -----------------------------

        main = tk.Frame(root)
        main.pack(
            fill=tk.BOTH,
            expand=True
        )

        # -----------------------------
        # Task list
        # -----------------------------

        list_frame = tk.Frame(main)
        list_frame.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=10,
            pady=10
        )

        tk.Label(
            list_frame,
            text="Tasks",
            font=("Helvetica", 14, "bold")
        ).pack(pady=(0, 5))

        self.task_list = tk.Listbox(
            list_frame,
            width=30,
            height=20
        )

        self.task_list.pack(
            fill=tk.Y,
            expand=True
        )

        self.task_list.bind(
            "<<ListboxSelect>>",
            self.list_task_selected
        )

        # -----------------------------
        # Matplotlib chart
        # -----------------------------

        chart_frame = tk.Frame(main)
        chart_frame.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.figure, self.ax = plt.subplots(
            figsize=(7, 6)
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=chart_frame
        )

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

        self.canvas.mpl_connect(
            "button_press_event",
            self.chart_clicked
        )

        self.refresh_task_list()
        self.draw_chart()

        # -----------------------------
        # Timer
        # -----------------------------

        self.root.after(
            1000,
            self.update_timer
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    # ==================================================
    # Task management
    # ==================================================

    def add_task(self):

        name = simpledialog.askstring(
            "Add Task",
            "Enter task name:",
            parent=self.root
        )

        if name is None:
            return

        name = name.strip()

        if not name:
            return

        if name in self.tasks:
            messagebox.showwarning(
                "Task already exists",
                "That task already exists.",
                parent=self.root
            )
            return

        self.tasks[name] = 0

        self.refresh_task_list()
        self.draw_chart()
        self.save_data()

    def remove_task(self):

        selection = self.task_list.curselection()

        if not selection:
            messagebox.showinfo(
                "Remove Task",
                "Select a task first.",
                parent=self.root
            )
            return

        name = self.task_list.get(selection[0])

        if self.active_task == name:
            self.stop_task()

        del self.tasks[name]

        self.refresh_task_list()
        self.draw_chart()
        self.save_data()

    # ==================================================
    # Selecting tasks
    # ==================================================

    def list_task_selected(self, event=None):

        selection = self.task_list.curselection()

        if not selection:
            return

        name = self.task_list.get(selection[0])

        self.start_task(name)

    def start_task(self, name):

        if name not in self.tasks:
            return

        # Record time against previous task
        self.update_active_time()

        self.active_task = name
        self.last_update = time.monotonic()

        self.status.config(
            text=f"Running: {name}"
        )

        self.draw_chart()

    def stop_task(self):

        self.update_active_time()

        self.active_task = None
        self.last_update = None

        self.status.config(
            text="No task running"
        )

        self.draw_chart()
        self.save_data()

    # ==================================================
    # Timer
    # ==================================================

    def update_active_time(self):

        if self.active_task is None:
            return

        now = time.monotonic()

        if self.last_update is not None:

            elapsed = now - self.last_update

            self.tasks[self.active_task] += elapsed

        self.last_update = now

    def update_timer(self):

        self.update_active_time()

        if self.active_task:

            seconds = self.tasks[
                self.active_task
            ]

            self.status.config(
                text=(
                    f"Running: {self.active_task} "
                    f"({self.format_time(seconds)})"
                )
            )

            self.draw_chart()

        self.root.after(
            1000,
            self.update_timer
        )

    # ==================================================
    # Pie chart
    # ==================================================

    def draw_chart(self):

        self.ax.clear()

        # Remove tasks with zero time from pie
        chart_tasks = {
            name: seconds
            for name, seconds in self.tasks.items()
            if seconds > 0
        }

        if not chart_tasks:

            self.ax.text(
                0.5,
                0.5,
                "Add some time to a task",
                ha="center",
                va="center",
                fontsize=16
            )

            self.ax.axis("off")

            self.canvas.draw_idle()

            return

        labels = list(chart_tasks.keys())
        values = list(chart_tasks.values())

        explode = [
            0.08 if label == self.active_task else 0
            for label in labels
        ]

        self.ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            explode=explode
        )

        self.ax.set_title(
            "Time spent on tasks"
        )

        self.ax.axis("equal")

        self.canvas.draw_idle()

    # ==================================================
    # Clicking the pie chart
    # ==================================================

    def chart_clicked(self, event):

        if event.inaxes != self.ax:
            return

        if event.xdata is None or event.ydata is None:
            return

        # Convert click position to an angle
        import math

        angle = math.degrees(
            math.atan2(
                event.ydata,
                event.xdata
            )
        )

        # Convert from -180..180 to 0..360
        angle = (90 - angle) % 360

        chart_tasks = {
            name: seconds
            for name, seconds in self.tasks.items()
            if seconds > 0
        }

        if not chart_tasks:
            return

        total = sum(chart_tasks.values())

        position = (
            angle / 360
        ) * total

        running_total = 0

        selected_task = None

        for name, seconds in chart_tasks.items():

            running_total += seconds

            if position <= running_total:
                selected_task = name
                break

        if selected_task:
            self.start_task(selected_task)

            self.select_task_in_list(
                selected_task
            )

    # ==================================================
    # Task list
    # ==================================================

    def refresh_task_list(self):

        self.task_list.delete(
            0,
            tk.END
        )

        for name, seconds in self.tasks.items():

            text = (
                f"{name}  "
                f"({self.format_time(seconds)})"
            )

            self.task_list.insert(
                tk.END,
                text
            )

    def select_task_in_list(self, task):

        for index, name in enumerate(
            self.tasks.keys()
        ):

            if name == task:

                self.task_list.selection_clear(
                    0,
                    tk.END
                )

                self.task_list.selection_set(
                    index
                )

                self.task_list.see(index)

                break

    # ==================================================
    # Formatting
    # ==================================================

    def format_time(self, seconds):

        seconds = int(seconds)

        hours = seconds // 3600

        minutes = (
            seconds % 3600
        ) // 60

        seconds = seconds % 60

        if hours:
            return (
                f"{hours}h "
                f"{minutes:02d}m"
            )

        if minutes:
            return (
                f"{minutes}m "
                f"{seconds:02d}s"
            )

        return f"{seconds}s"

    # ==================================================
    # Save/load
    # ==================================================

    def save_data(self):

        self.update_active_time()

        try:

            with open(
                DATA_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.tasks,
                    file,
                    indent=4
                )

        except OSError as error:

            messagebox.showerror(
                "Save error",
                str(error),
                parent=self.root
            )

    def load_data(self):

        if not DATA_FILE.exists():
            return

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                self.tasks = json.load(file)

        except (
            OSError,
            json.JSONDecodeError
        ):

            self.tasks = {}

    # ==================================================
    # Close
    # ==================================================

    def close(self):

        self.update_active_time()

        self.save_data()

        self.root.destroy()


# ======================================================
# Start application
# ======================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TimeTracker(root)

    root.mainloop()