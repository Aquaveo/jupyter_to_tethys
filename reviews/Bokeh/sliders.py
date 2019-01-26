

# start bokeh app
# # bokeh serve sliders.py

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


def update_data(attrname, old, new):

    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = np.sin(k*x)

    source.data = dict(x=x, y=y)

freq.on_change('value', update_data)


# Set up layouts and add to document
widget_box = widgetbox(freq)

curdoc().add_root(row(widget_box, plot, width=800))
curdoc().title = "Sliders"

# def change_slider_in_python():
#     freq.value = np.random.uniform(0.1, 5.1)
#
# curdoc().add_periodic_callback(change_slider_in_python, 2000)
