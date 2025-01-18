from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PySide2.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.figure import Figure
import re
from Math import Function

class FunctionPlotterApp(QWidget):
    # Window properties
    WINDOW_X = 500
    WINDOW_Y = 100
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 900
    WINDOW_TITLE = 'GraphCalc - Function Plotter' 

    def __init__(self):
        """
        Initializes the application window, sets up layout, and prepares widgets.
        """
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setGeometry(self.WINDOW_X, self.WINDOW_Y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        # Main layout
        layout = QVBoxLayout()

        # First function input
        self.function1_input = QLineEdit(self)
        self.function1_input.setPlaceholderText('Enter first function of x, e.g., 5*x^3 + 2*x or log10(x) or sqrt(x)')
        layout.addWidget(self.function1_input)

        # Second function input
        self.function2_input = QLineEdit(self)
        self.function2_input.setPlaceholderText('Enter second function of x, e.g., 3*x^2 - x or log2(x)')
        layout.addWidget(self.function2_input)

        # Plot button
        self.plot_button = QPushButton('Plot Functions', self)
        self.plot_button.clicked.connect(self.on_plot)
        layout.addWidget(self.plot_button)

        # Matplotlib canvas for plotting
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Matplotlib toolbar
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)
        self.plotter = Function()

        # Apply styles to the widgets
        self.apply_styles()

    def apply_styles(self):
        """
        Applies styles to the widgets to enhance the UI appearance.
        """
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)

    def on_plot(self):
        """
        Handles the plot button click event. Validates inputs, clears the figure, 
        and plots the functions on the canvas.
        """
        # Get the input functions
        func1 = self.function1_input.text()
        func2 = self.function2_input.text()

        # Validate inputs
        if not self.validate_input(func1) or not self.validate_input(func2):
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid functions.')
            return

        try:
            # Clear the figure and plot the functions
            self.figure.clear()
            self.plotter.plot_functions(func1, func2, self.figure)
            self.canvas.draw()
        except Exception as e:
            # Show error message if plotting fails
            error_message = f'An error occurred while plotting the functions: {str(e)}'
            QMessageBox.warning(self, 'Error', error_message)
            print(error_message)

    def validate_input(self, input_text):
        """
        Validates if the input string is a valid mathematical expression.
        
        Args:
            input_text (str): The input string representing a mathematical function.
        
        Returns:
            bool: True if the input matches the expected pattern, False otherwise.
        """
        # Validate if the input is a valid mathematical expression
        if not input_text.strip():
            return False
        pattern = re.compile(r'^[0-9x\+\-\/\*\^\(\)logsqrt\s\.0-9]+$')
        return bool(pattern.match(input_text))
