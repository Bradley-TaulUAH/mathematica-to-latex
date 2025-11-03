# HW 8-1 pb 4.nb

## Infinite Square Well
**Merzbacher Problem 8.1**  
Pure symbolic version  
Compare which is smaller  
Symbolic overlap integrals  

### INFINITE SQUARE WELL VARIATIONAL CALCULATION

**Potential:** $V = 0$ for $-a \leq x \leq a$, $\infty$ elsewhere  
**Boundary conditions:** $\psi(\pm a) = 0$

---

## PART (a): TRAPEZOIDAL TRIAL FUNCTION

**Trial function:**
$$\psi(x) = \begin{cases}
a - x & \text{for } b \leq x \leq a \text{ (sloped regions)} \\
a - b & \text{for } -b \leq x \leq b \text{ (flat region)} \\
a + x & \text{for } -a \leq x \leq -b \text{ (Triangular function)}
\end{cases}$$

**Normalization integral:**
$$N = \int_{-a}^{a} (a - |x|)^2 \, dx$$

By symmetry:  
$$N = 2\int_0^a (a - x)^2 \, dx$$

**Expanding:**
$$\int_0^a (a^2 - 2ax + x^2) \, dx = \left[a^2x - ax^2 + \frac{x^3}{3}\right]_0^a$$

$$= \left[a^2 \cdot a - a \cdot a^2 + \frac{a^3}{3}\right] - 0$$

$$= a^3 - a^3 + \frac{a^3}{3} = \frac{a^3}{3}$$

**Result:**
$$N = \frac{a^3}{3}$$

$$A = \frac{1}{\sqrt{N}} = \sqrt{\frac{3}{a^3}}$$

---

## Kinetic Energy Calculation

**Derivative of trial function:**
$$\frac{d\psi}{dx} = \begin{cases}
-A & \text{for } 0 \leq x \leq a \\
+A & \text{for } -a \leq x \leq 0
\end{cases}$$

**Kinetic energy expectation value:**
$$\langle T \rangle = \frac{\hbar^2}{2m} \int_{-a}^{a} \left|\frac{d\psi}{dx}\right|^2 \, dx$$

$$= \frac{\hbar^2}{2m} \times 2\int_0^a A^2 \, dx$$

$$= \frac{\hbar^2}{2m} \times 2A^2 a$$

$$= \frac{\hbar^2}{2m} \times 2 \cdot \frac{3}{a^3} \cdot a$$

$$= \frac{\hbar^2}{2m} \times \frac{6}{a^2}$$

$$= \frac{3\hbar^2}{ma^2}$$

**Total energy (V = 0 inside well):**
$$\langle E \rangle = \langle T \rangle = \frac{3\hbar^2}{ma^2}$$

---

## PART (b): Optimize parameter b

**Normalization integral with parameter b:**
$$N = \int_{-a}^{a} \psi^2 \, dx$$

$$= \int_{-a}^{-b} (a + x)^2 \, dx + \int_{-b}^{b} (a - b)^2 \, dx + \int_b^a (a - x)^2 \, dx$$

By symmetry:
$$N = 2\int_b^a (a - x)^2 \, dx + \int_{-b}^{b} (a - b)^2 \, dx$$

**To find optimal b:** Minimize $\langle E \rangle$ with respect to b.

---

## Notes

- Compare variational result to exact ground state: $E_0 = \frac{\pi^2\hbar^2}{8ma^2}$
- The trapezoidal trial function provides an upper bound to the true ground state energy
- Optimization of parameter b should yield a better approximation
