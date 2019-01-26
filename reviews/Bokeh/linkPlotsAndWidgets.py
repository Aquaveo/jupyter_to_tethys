from numpy.random import random

from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models.widgets import Select, TextInput
from bokeh.models.sources import ColumnDataSource
from bokeh.io import curdoc


def get_data(N):
    return dict(x=random(size=N), y=random(size=N), r=random(size=N) * 0.03)


COLORS = ["black", "firebrick", "navy", "olive", "goldenrod"]


def modify_doc(doc):
    source = ColumnDataSource(data=get_data(200))

    p = figure(tools="", toolbar_location=None)
    r = p.circle(x='x', y='y', radius='r', source=source,
                 color="navy", alpha=0.6, line_color="white")

    select = Select(title="Color", value="navy", options=COLORS)
    input = TextInput(title="Number of points", value="200")

    def update_color(attrname, old, new):
        r.glyph.fill_color = select.value

    select.on_change('value', update_color)

    def update_points(attrname, old, new):
        N = int(input.value)
        source.data = get_data(N)

    input.on_change('value', update_points)

    layout = column(row(select, input, width=400), row(p))

    doc.add_root(layout)


modify_doc(curdoc())
