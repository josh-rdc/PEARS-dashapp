import numpy as np

F = lambda t, Z: [(1 - t**2) * Z[1] - Z[0], Z[0]]
x = []
y = []
x_new = []
y_new = []
#F = lambda Z: Z[0]

def rk4MethodSys(dfuns, ICs, tFinal, numPts=100):
    F = lambda t, Z: np.array(dfuns(t, Z), dtype='float')
    t0, Z0 = ICs  # [t0, [x0, y0]] = [t0, Z0]
    t, h = np.linspace(t0, tFinal, numPts, retstep=True)

    Z = np.zeros((len(Z0), len(t)))
    Z[:, 0] = Z0

    for i in range(numPts - 1):
        k1 = h * F(t[i], Z[:, i])
        k2 = h * F(t[i] + 0.5*h, Z[:, i] + 0.5*k1)
        k3 = h * F(t[i] + 0.5*h, Z[:, i] + 0.5*k2)
        k4 = h * F(t[i + 1], Z[:, i] + k3)
        Z[:, i + 1] = Z[:, i] + (k1 + 2*k2 + 2*k3 + k4) / 6
        
    return (t, Z)

t_rk4, Z_rk4 = rk4MethodSys(F, [0, [0, 0.1]], 5, numPts=11)
x = Z_rk4[0]
y = Z_rk4[1]
x_new.extend(Z_rk4[0][0:4])
y_new.extend(Z_rk4[1][0:4])
t = t_rk4.tolist()

h = t[1] - t[0]

print("Initial values from RK4 method:")
for i in range(4):
    print(f"t{i} = {t[i]:.3f}, x{i} = {x[i]:.6f}, y{i} = {y[i]:.6f}")
    
for i in range(3, 10):
    x1 = x[i] + h / 24 * (55 * F(t[i], [x[i], y[i]])[0] - 59 * F(t[i-1], [x_new[i-1], y_new[i-1]])[0] + 37 * F(t[i-2], [x_new[i-2], y_new[i-2]])[0] - 9 * F(t[i-3], [x_new[i-3], y_new[i-3]])[0])
    y1 = y[i] + h / 24 * (55 * F(t[i], [x[i], y[i]])[1] - 59 * F(t[i-1], [x_new[i-1], y_new[i-1]])[1] + 37 * F(t[i-2], [x_new[i-2], y_new[i-2]])[1] - 9 * F(t[i-3], [x_new[i-3], y_new[i-3]])[1])
    
    t_i = t[i] + h  # Use a different variable name for the updated time value
    
    f1_4 = F(t_i, [x1, y1])[0]
    
    # Adam-Moulton
    f1 = x_new[i] + h / 24 * (9 * f1_4 + 19 * F(t_i, [x_new[i], y_new[i]])[0] - 5 * F(t[i-1], [x_new[i-1], y_new[i-1]])[0] + F(t[i-2], [x_new[i-2], y_new[i-2]])[0])
    
    # Evaluate f2(t5, x5, y5)
    f2_4 = F(t_i, [f1, y1])[1]
    
    # Adam-Moulton
    f2 = y_new[i] + h / 24 * (9 * f2_4 + 19 * F(t_i, [x_new[i], y_new[i]])[1] - 5 * F(t[i-1], [x_new[i-1], y_new[i-1]])[1] + F(t[i-2], [x_new[i-2], y_new[i-2]])[1])
    
    x_new.append(f1)
    y_new.append(f2)

print(x_new)
print(y_new)