from bokeh.layouts import row
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

# this script is adopted from django2 sample
# run this a bokeh app: bokeh serve myslider.py
import parambokeh
from bokeh.io import curdoc
import numpy as np
import param


class SineWave(param.ParameterizedFunction):
    offset = param.Number(default=0.0, bounds=(-5.0, 5.0))
    amplitude = param.Number(default=1.0, bounds=(-5.0, 5.0))
    phase = param.Number(default=0.0, bounds=(0.0, 2 * np.pi))
    frequency = param.Number(default=1.0, bounds=(0.1, 5.1))
    N = param.Integer(default=200, bounds=(0, None))

    # x_range = param.Range(default=(0, 4*np.pi),bounds=(0,4*np.pi))
    # y_range = param.Range(default=(-2.5,2.5),bounds=(-10,10))

    def __call__(self, **params):
        p = param.ParamOverrides(self, params)
        x = np.linspace(0, 4 * np.pi, p.N)
        y = p.amplitude * np.sin(p.frequency * x + p.phase) + p.offset
        return x, y


# This is a bokeh app needing a bokeh server!
def app(doc):
    x,y = SineWave()
    source = ColumnDataSource(data=dict(x=x, y=y))

    import numpy as np # see TODO below about ranges
    plot = figure(plot_height=400, plot_width=400,
                  tools="crosshair,pan,reset,save,wheel_zoom",
                  x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

    def update_sinewave(sw,**kw):
        x,y = sw()
        source.data = dict(x=x, y=y)
        # TODO couldn't figure out how to update ranges
        #plot.x_range.start,plot.x_range.end=pobj.x_range
        #plot.y_range.start,plot.y_range.end=pobj.y_range

    parambokeh.Widgets(SineWave, mode='server', doc=doc, callback=update_sinewave)
    doc.add_root(row(plot, width=800))

app(curdoc())