import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def format_approx(value):
    """Display numerical results with six digits after the decimal point."""
    try:
        number = complex(value.evalf(20))
    except (TypeError, ValueError):
        return "Cannot evaluate numerically"
    if not (np.isfinite(number.real) and np.isfinite(number.imag)):
        return "No finite result"
    real = round(number.real, 6)
    imaginary = round(number.imag, 6)
    if imaginary == 0:
        return f"{real:.6f}"
    sign = "+" if imaginary > 0 else "-"
    return f"{real:.6f} {sign} {abs(imaginary):.6f}i"


def main():
    x = sp.Symbol("x", real = True)
    expression = input("Input f(x) - for example: x**2 - 1: ")
    # Accept Euler's constant as either e or E, and ^ as exponentiation.
    try:
        f = sp.sympify(
            expression, locals={"x": x, "pi": sp.pi, "e": sp.E, "E": sp.E},
            convert_xor=True,
        )
    except (sp.SympifyError, SyntaxError, TypeError, ValueError):
        print("Invalid expression. Example: pi*x^2 + e^x (use * to multiply).")
        return

    if not isinstance(f, sp.Expr) or f.free_symbols - {x}:
        print("Please input function y = f(x) from console")
        return

    a = sp.Rational(input("Input a: "))
    b = sp.Rational(input("Input b: "))
    c = sp.Rational(input("Input c: "))

    if not a < b or not a <= c <= b:
        print("a < b và a <= c <= b")
        return

    difference_quotient = (f - f.subs(x, c)) / (x - c)
    left = sp.limit(difference_quotient, x, c, dir = "-")
    right = sp.limit(difference_quotient, x, c, dir = "+")

    if left.is_real and left.is_finite and (left - right).equals(0):
        derivative_result = f"f'({c}) ≈ {format_approx(left)}"
    else:
        derivative_result = f"Cannot find a finite two-sided derivative at x = {c}"

    print(derivative_result)

    integral = sp.integrate(f, (x, a, b))
    volume = sp.integrate(sp.pi * f**2, (x, a, b))
    integral_result = f"I ≈ {format_approx(integral)}"
    volume_result = f"V ≈ {format_approx(volume)}"
    print(integral_result)
    print(volume_result)

    f_numeric = sp.lambdify(x, f, "numpy")
    x_values = np.linspace(float(a), float(b), 500)
    y_values = np.broadcast_to(f_numeric(x_values), x_values.shape)

    # Reserve a separate area so the results do not cover the curve.
    fig, (ax, results_ax) = plt.subplots(
        2, 1, figsize=(11, 8), gridspec_kw={"height_ratios": [3, 1]},
        layout="constrained",
    )
    equation = f"$y = {sp.latex(f)}$"
    ax.plot(x_values, y_values, label=equation)
    ax.set_title(equation)
    ax.axhline(0, color="gray", linewidth=1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(alpha=0.3)
    results_ax.axis("off")
    results_ax.text(
        0, 1,
        f"a = {a}, b = {b}, c = {c}\n"
        f"{derivative_result}\n{integral_result}\n{volume_result}",
        transform=results_ax.transAxes, va="top", fontsize=10, wrap=True,
    )
    plt.show()

if __name__ == "__main__":
    main()
