import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def main():
    x = sp.Symbol("x", real=True)
    expression = input("Nhập f(x), ví dụ x**2 - 1: ")
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
        print("Hãy nhập một biểu thức chỉ phụ thuộc vào x.")
        return

    a = sp.Rational(input("Nhập a: "))
    b = sp.Rational(input("Nhập b: "))
    c = sp.Rational(input("Nhập c: "))

    if not a < b or not a <= c <= b:
        print("Cần có a < b và a ≤ c ≤ b.")
        return

    # So sánh hai giới hạn của thương sai phân tại c.
    difference_quotient = (f - f.subs(x, c)) / (x - c)
    left = sp.limit(difference_quotient, x, c, dir="-")
    right = sp.limit(difference_quotient, x, c, dir="+")

    if left.is_real and left.is_finite and (left - right).equals(0):
        derivative_result = f"f'({c}) = {left} (approximately {left.evalf(10)})"
    else:
        derivative_result = f"Cannot find a finite two-sided derivative at x = {c}"

    # Tích phân có dấu. Thể tích dùng diện tích lát cắt pi * f(x)**2.
    print(derivative_result)

    integral = sp.integrate(f, (x, a, b))
    volume = sp.integrate(sp.pi * f**2, (x, a, b))
    integral_result = f"I = {integral} (approximately {integral.evalf(10)})"
    volume_result = f"V = {volume} (approximately {volume.evalf(10)})"
    print(integral_result)
    print(volume_result)

    f_numeric = sp.lambdify(x, f, "numpy")
    x_values = np.linspace(float(a), float(b), 500)
    # Với hàm hằng, lặp lại cùng giá trị y cho mọi điểm x.
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
