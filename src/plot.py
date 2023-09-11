"""
This module is responsible for handling the plot using Matplotlib.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.support import puts

class Canvas(FigureCanvas):
    """
    This is the graph field object class.

    It inherits from FigureCanvas and provides a canvas for displaying plots.
    """
    def __init__(self):
        """
        Initialize a Canvas object.

        Initializes a Matplotlib figure and axes for plotting.
        """
        _, self.axes = plt.subplots(
            figsize=pix_to_inch(int(SCREEN_WIDTH / 3), int(SCREEN_HEIGHT / 3)), facecolor='none'
        )
        super().__init__()
        self.pie = None
        self.axes = self.figure.add_subplot(111)

    def plot(self, labels, values):
        """
        Plot a pie chart on the canvas.

        Args:
            labels (list of str): Labels for pie chart segments.
            values (list of float): Values for pie chart segments.

        Clears the existing plot on the canvas and plots a pie chart using the provided data.
        """
        self.axes.cla()
        self.axes.clear()
        try:
            self.axes.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            self.axes.axis('equal')
        except (ValueError, RuntimeWarning):
            puts('Error with plot...')
        self.draw()

def load_plot_content(table) -> tuple[list, list, float]:
    """
    Load data for plotting from a table and calculate percentages.

    Args:
        table: The table containing data to be plotted.

    Returns:
        tuple: A tuple containing the following elements:
            - final_labels (list of str): Labels for the plotted segments.
            - final_values (list of int): Values for the plotted segments.
            - summary (float): The sum of all values.
    """
    row_count = table.rowCount()
    labels = []
    values = []
    for index in range(row_count):
        name = table.item(index, 0).text()
        value = table.item(index, 2).text()
        if value == '0.0':
            continue
        values.append(int(float(value)))
        labels.append(name)
    summary = sum(values)
    others_list = []
    final_labels = []
    final_values = []
    for index, value in enumerate(values):
        if float(value / summary) >= 0.1:
            final_values.append(value)
            final_labels.append(labels[index])
            continue
        others_list.append(value)
    other = sum(others_list)
    if float(other) != 0.0:
        final_values.append(other)
        final_labels.append('Pozostałe')

    return (final_labels, final_values, summary)

def pix_to_inch(width: int, height: int) -> tuple[int, int]:
    """
    Convert pixel dimensions to inches.

    Args:
        width (int): Width in pixels.
        height (int): Height in pixels.

    Returns:
        tuple: A tuple containing the converted width and height in inches.
    """
    return (int(width / 96), int(height / 96))
