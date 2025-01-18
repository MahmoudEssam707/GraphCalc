import pytest
from PySide2.QtCore import Qt
from gui import FunctionPlotterApp

# Fixture to initialize the QApplication instance for the tests
@pytest.fixture
def qapp():
    from PySide2.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app # Provide the fixture value to the test function 
    app.quit()

# Fixture to create an instance of FunctionPlotterApp
@pytest.fixture
def app(qtbot):
    window = FunctionPlotterApp()
    qtbot.addWidget(window)  # Add the widget to the Qt bot
    yield window # na uh, just return the window but it doesn't mean it's the end of the function 
    window.close() 

# Test the initial state of the application, just to check when starting it up, application is in the correct state
def test_initial_state(app):
    assert app.windowTitle() == 'Function Plotter'
    assert app.function1_input.placeholderText() == 'Enter first function of x, e.g., 5*x^3 + 2*x or log10(x) or sqrt(x)'
    assert app.function2_input.placeholderText() == 'Enter second function of x, e.g., 3*x^2 - x or log2(x)'
    assert app.plot_button.text() == 'Plot Functions'

# Test input validation, checking if the input is valid or not, main thing to test "Mathmatical symbols" and "Functions"
@pytest.mark.parametrize("input_text, expected", [
    ("5*x^3 + 2*x", True),  # This one true with respect to the "^" symbol
    ("log10(x)", True), # This one true with respect to the "log10" function, and also it's valid for log"B"(x) where B is any number
    ("sqrt(x)", True), # This one true with respect to the "sqrt" function and it's valid anyway 
    ("3*x^2 - x", True),  # This one true with respect to the "^" symbol
    ("log2(x)", True), # yes this one i'm talking about the "logB(x)" where B is any number
    ("", False), # if he left it empty then it's invalid
    ("5*y^3 + 2*y", False),  # This one is invalid because it's using "y" instead of "x"
    ("5*x^3 + 2*x + sin(x)", False),  # Didn't care about it for now, but maybe in the future we can make it valid for trigonometric functions
])
def test_validate_input(app, input_text, expected):
    assert app.validate_input(input_text) == expected

# Test plotting functionality with valid inputs
def test_plot_functions_valid_input(app, qtbot, mocker):
    # Mock the plotter to avoid actual plotting, like a fake version of the plotter
    mock_plot = mocker.patch.object(app.plotter, 'plot_functions')

    # Set valid inputs checking by it validaity of "^"
    app.function1_input.setText("5*x^3 + 2*x")  
    app.function2_input.setText("3*x^2 - x")    

    # Click the plot button
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    # Check if the plotter was called with the correct arguments
    mock_plot.assert_called_once_with("5*x^3 + 2*x", "3*x^2 - x", app.figure)

# Test plotting functionality with invalid inputs
def test_plot_functions_invalid_input(app, qtbot, mocker):
    # Mock the plotter to ensure it's not called
    mock_plot = mocker.patch.object(app.plotter, 'plot_functions')

    # Set invalid inputs
    app.function1_input.setText("5*y^3 + 2*y")  # Invalid variable
    app.function2_input.setText("3*x^2 - x")    # Valid function

    # Click the plot button
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    # Ensure the plotter was not called
    mock_plot.assert_not_called()

# Test error handling during plotting
def test_plot_functions_error_handling(app, qtbot, mocker):
    # Mock the plotter to raise an exception
    mock_plot = mocker.patch.object(app.plotter, 'plot_functions', side_effect=Exception("Plotting error"))

    # Set valid inputs
    app.function1_input.setText("5*x^3 + 2*x")  
    app.function2_input.setText("3*x^2 - x")    

    # Click the plot button
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    # Ensure the error message was displayed
    assert app.figure.axes == []  # Ensure the figure is cleared
    assert mock_plot.called  # Ensure the plotter was called
    
# additonal tests for the GUI
# Test the toolbar is present
def test_toolbar_presence(app):
    assert app.toolbar is not None
    assert app.toolbar.parent() == app

# Test the canvas is present
def test_canvas_presence(app):
    assert app.canvas is not None
    assert app.canvas.figure == app.figure