import numpy as np
import sympy as sp
import re

class Function:
    def plot_functions(self, func1, func2, figure):
        """
        Plots two functions and highlights their intersection points.
        
        Args:
            func1 (str): The first function as a string (e.g., "x^2").
            func2 (str): The second function as a string (e.g., "x+2").
            figure (matplotlib.figure.Figure): A matplotlib figure to plot on.
        """
        x = sp.symbols("x")  # Define the symbol x for sympy
        f1 = self.parse_function(func1, x)  # Parse the first function
        f2 = self.parse_function(func2, x)  # Parse the second function

        x_vals = np.linspace(-10, 10, 400)  # Generate 400 points between -10 and 10
        y1_vals = []
        y2_vals = []

        for val in x_vals:
            try:
                y1 = f1.subs(x, val).evalf()  # Evaluate f1 at val
                y2 = f2.subs(x, val).evalf()  # Evaluate f2 at val
                # Ensure the result is real and not complex
                if y1.is_real and y2.is_real:
                    y1_vals.append(float(y1))
                    y2_vals.append(float(y2))
                else:
                    y1_vals.append(np.nan)  # Skip complex values
                    y2_vals.append(np.nan)
            except (TypeError, ValueError):
                y1_vals.append(np.nan)  # Skip invalid values
                y2_vals.append(np.nan)

        ax = figure.add_subplot(111)  # Add a subplot to the figure
        ax.plot(x_vals, y1_vals, label="Function 1")  # Plot the first function
        ax.plot(x_vals, y2_vals, label="Function 2")  # Plot the second function
        ax.axhline(0, color="black", linewidth=0.5)  # Add horizontal line at y=0
        ax.axvline(0, color="black", linewidth=0.5)  # Add vertical line at x=0
        ax.grid(color="gray", linestyle="--", linewidth=0.5)  # Add grid
        ax.legend()  # Add legend

        # Find intersection points
        intersection_points = self.find_intersection(f1, f2, x)
        for point in intersection_points:
            if point[0].is_real and point[1].is_real:  # Ensure intersection points are real
                ax.plot(float(point[0]), float(point[1]), "ro")  # Plot intersection points
                ax.annotate(
                    f"({float(point[0]):.2f}, {float(point[1]):.2f})",
                    (float(point[0]), float(point[1])),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha="center",
                )  # Annotate intersection points

    def parse_function(self, func_str, x):
        """
        Converts a string representation of a mathematical function into a sympy expression.
        
        Args:
            func_str (str): The function as a string (e.g., "x^2 + log10(x)").
            x (sympy.Symbol): The variable to use in the function.
        
        Returns:
            sympy.Expr: The parsed sympy expression.
        """
        # Replace ^ with ** for compatibility
        func_str = func_str.replace("^", "**")
        # Replace log10(x) with log(x, 10), log2(x) with log(x, 2), etc.
        func_str = re.sub(r"log(\d+)\(([^)]+)\)", r"log(\2, \1)", func_str)
        return sp.sympify(func_str)  # Convert the string to a sympy expression

    def find_intersection(self, f1, f2, x):
        """
        Finds the intersection points of two functions.
        
        Args:
            f1 (sympy.Expr): The first function as a sympy expression.
            f2 (sympy.Expr): The second function as a sympy expression.
            x (sympy.Symbol): The variable used in the functions.
        
        Returns:
            list of tuple: A list of intersection points as (x, y) tuples.
        """
        intersection_points = []
        solutions = sp.solve(f1 - f2, x)  # Solve f1 - f2 = 0 for x
        for sol in solutions:
            try:
                x_val = sol.evalf()  # Evaluate the solution
                y_val = f1.subs(x, x_val).evalf()  # Evaluate f1 at the solution
                if x_val.is_real and y_val.is_real:  # Ensure intersection points are real
                    intersection_points.append((round(x_val, 2), round(y_val, 2)))
            except (TypeError, ValueError):
                continue  # Skip invalid solutions
        return intersection_points  # Return the intersection points
