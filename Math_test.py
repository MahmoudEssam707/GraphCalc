import pytest
import sympy as sp
from Math import Function
from matplotlib.figure import Figure
# initialize the object for the Function which includes mathmatical operation and matplotlib
@pytest.fixture
def Math_App():
    """Fixture to initialize the FunctionMath_App."""
    return Function()

# initialize the object for the figure
@pytest.fixture
def figure():
    """Fixture to initialize a matplotlib figure."""
    return Figure()

# playing with different functions and check if the parse_function is working
def test_parse_function_with_caret(Math_App):
    x = sp.symbols("x")
    assert Math_App.parse_function("x^2", x) == x**2 # x^2 = x**2
    assert Math_App.parse_function("x^3 + 2*x^2", x) == x**3 + 2 * x**2 # x^3 + 2*x^2 = x**3 + 2 * x**2
    assert Math_App.parse_function("log2(x)", x) == sp.log(x, 2) # log2(x) = log(x, 2), and anyway logb(x) = log(x, b)
    assert Math_App.parse_function("sqrt(x)", x) == sp.sqrt(x) # sqrt(x) = x½

# try different functions and check if the plot is working
@pytest.mark.parametrize(
    "func1, func2",
    [
        ("x^2", "x + 5"), 
        ("x^3 - 3*x + 1", "x^2 - x - 1"),
        ("sqrt(x)", "x^2"),
        ("x^4 - x^2", "x^3"), 
        ("log10(x)", "log2(x)"), # Bonus Part to make it valid to any base of Logarithm
    ],
)
def test_plot_functions_with_caret(Math_App, func1, func2, figure):
    """Test plotting functions using caret (^) for exponents."""
    try:
        Math_App.plot_functions(func1, func2, figure)
    except Exception as e:
        pytest.fail(f"Plotting failed with error: {e}")

# Hmmmf, this test to validate the inputs anyway, does it has logic error? i hope it no
@pytest.mark.parametrize(
    "func1, func2, expected_points",
    [
        ("x^2", "x + 5", [(-1.79, 3.20), (2.79, 7.79)]),
        ("x^3", "x", [(-1, -1), (0, 0), (1, 1)]),
        ("log2(x)", "log10(x)", [(1, 0)]),
    ],
)
def test_find_intersection_with_caret(Math_App, func1, func2, expected_points):
    x = sp.symbols("x")
    f1 = Math_App.parse_function(func1, x)
    f2 = Math_App.parse_function(func2, x)
    intersection_points = Math_App.find_intersection(f1, f2, x)

    # Ensure expected intersection points match actual points (real only)
    actual_points = [(float(p[0]), float(p[1])) for p in intersection_points]
    expected_points = [(float(x), float(y)) for x, y in expected_points]

    # Allow for floating-point precision tolerance, because you know, imagine error because it's 3.79999 not 3.8
    tolerance = 1e-2
    assert len(actual_points) == len(expected_points), "Number of intersection points mismatch"
    for expected in expected_points:
        assert any(
            abs(expected[0] - actual[0]) < tolerance and abs(expected[1] - actual[1]) < tolerance
            for actual in actual_points
        ), f"Expected point {expected} not found within tolerance in actual points {actual_points}"