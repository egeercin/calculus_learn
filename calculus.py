import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
})

# Set global dark background and white text
mpl.rcParams.update({
    "axes.facecolor": "black",
    "axes.edgecolor": "white",
    "figure.facecolor": "black",
    "xtick.color": "white",
    "ytick.color": "white",
    "text.color": "white",
    "axes.labelcolor": "white",
    "axes.titlecolor": "white",
    "legend.edgecolor": "white",
    "legend.facecolor": "black",
})

# Define functions
def quadratic(x):
    return x**2

def cubic(x):
    return x**3

def squareroot(x):
    return np.sqrt(x)

def exponential(x):
    return np.exp(x)

def sigmoid(x):
    return 1 / (1 + np.exp(-10 * (x - 1)))

def sine_wave(x):
    return np.sin(x)

def cosine_wave(x):
    return np.cos(x)

# Map names to functions
functions = {
    'x²': quadratic,
    'x³': cubic,
    '√x': squareroot,
    'eˣ': exponential,
    'sgm(x)': sigmoid,
    'sin(x)': sine_wave,
    'cos(x)': cosine_wave,
}

# Plot function
def plot_riemann_sum(ax, func, n):
    ax.clear()
    
    x_curve = np.linspace(0, 2, 200)
    y_curve = func(x_curve)
    ax.plot(x_curve, y_curve, label=r'$f(x)$', color='white', linewidth=0.5)
    ax.set_facecolor('black')

    x = np.linspace(0, 2, n+1)
    dx = x[1] - x[0]
    x_left = x[:-1]
    y_left = func(x_left)

    for i in range(len(x_left)):
        ax.fill(
            [x_left[i], x_left[i], x_left[i]+dx, x_left[i]+dx],
            [0, y_left[i], y_left[i], 0],
            facecolor='orange', alpha=0.5, edgecolor='darkorange', linewidth=1.5, label='Riemann Sum' if i == 0 else ""
        )

    try:
        actual = np.trapz(func(x_curve), x_curve)
    except Exception:
        actual = float('nan')
    approx = np.sum(y_left * dx)
    
    ax.set_title(
    r"""Riemann Sum ($n = %d$)
    Actual $\approx$ %.3f, Approx $\approx$ %.3f""" % (n, actual, approx)
)   
    ax.set_xlim(0, 2)
    ax.set_ylim(0, max(y_curve)*1.1)
    # Set tick and spine colors for dark background
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.legend()

# Initial settings
current_func = quadratic
current_func_name = 'x²'
initial_n = 10

# Set up figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3, bottom=0.25)

# Initial plot
plot_riemann_sum(ax, current_func, initial_n)

# Slider
ax_slider = plt.axes([0.3, 0.1, 0.55, 0.03])
slider = Slider(ax_slider, 'Rectangles', 2, 100, valinit=initial_n, valstep=1, facecolor='orange')

# Radio buttons
ax_radio = plt.axes([0.05, 0.4, 0.15, 0.3], facecolor='lightgray')
radio = RadioButtons(
    ax_radio,
    ('x²', 'x³', '√x', 'eˣ', 'sgm(x)', 'sin(x)', 'cos(x)')
)

# Set label text color manually
for label in radio.labels:
    label.set_color('black')
# Update function
def update(val):
    n = int(slider.val)
    func = functions[radio.value_selected]
    plot_riemann_sum(ax, func, n)
    fig.canvas.draw_idle()

# Connect events
slider.on_changed(update)
radio.on_clicked(update)

plt.show()