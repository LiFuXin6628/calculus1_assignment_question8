import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def main():
    x = sp.Symbol("x", real=True)
    expression = input("Nhập f(x), ví dụ x**2 - 1: ")
    f = sp.sympify(expression, locals={"x": x})

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
        print(f"f'({c}) = {left}")
    else:
        print(f"Không tìm được đạo hàm hữu hạn hai phía tại x = {c}.")

    # Tích phân có dấu. Thể tích dùng diện tích lát cắt pi * f(x)**2.
    integral = sp.integrate(f, (x, a, b))
    volume = sp.integrate(sp.pi * f**2, (x, a, b))
    print(f"I = {integral} (xấp xỉ {integral.evalf(10)})")
    print(f"V = {volume} (xấp xỉ {volume.evalf(10)})")

    f_numeric = sp.lambdify(x, f, "numpy")
    x_values = np.linspace(float(a), float(b), 500)
    # Với hàm hằng, lặp lại cùng giá trị y cho mọi điểm x.
    y_values = np.broadcast_to(f_numeric(x_values), x_values.shape)

    plt.plot(x_values, y_values, label="y = f(x)")
    plt.axhline(0, color="gray", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
