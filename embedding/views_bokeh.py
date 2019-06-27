from django.shortcuts import render

import numpy as np

from bokeh.embed import server_document
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

from threading import Thread

def modify_doc(doc):
    
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
    
    
    # Set up widgets
    text = TextInput(title="title", value='my sine wave')
    offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
    amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
    phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
    freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)
    
    
    # Set up callbacks
    def update_title(attrname, old, new):
    
        plot.title.text = text.value
    
    
    text.on_change('value', update_title)
    
    
    def update_data(attrname, old, new):
    
        # Get the current slider values
        a = amplitude.value
        b = offset.value
        w = phase.value
        k = freq.value
    
        # Generate the new curve
        x = np.linspace(0, 4*np.pi, N)
        y = a*np.sin(k*x + w) + b
    
        source.data = dict(x=x, y=y)
    
    
    for w in [offset, amplitude, phase, freq]:
    
        w.on_change('value', update_data)
    
    
    # Set up layouts and add to document
    inputs = widgetbox(text, offset, amplitude, phase, freq)
    
    doc.add_root(row(inputs, plot, width=800))
    doc.title = "Sliders"


def home(request):    
    script = server_document('http://127.0.0.1:5006/bokehexample')
    
    def bk_worker():
        server = Server({'/bokehexample': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:8000"])
        server.start()
        server.io_loop.start()

    Thread(target=bk_worker).start()
    
    context = {
        'script': script
    }
    return render(request, 'bokehexample/home.html', context)
    
