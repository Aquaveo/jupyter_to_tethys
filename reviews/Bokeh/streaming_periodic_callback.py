from math import cos, sin

from bokeh.plotting import figure
from bokeh.models.sources import ColumnDataSource
from bokeh.io import curdoc


def modify_doc(doc):
    p = figure(match_aspect=True)
    p.circle(x=0, y=0, radius=1, fill_color=None, line_width=2)

    # this is just to help the auto-datarange
    p.rect(0, 0, 2, 2, alpha=0)

    # this is the data source we will stream to
    # set one point (1, 0) as the streaming start point
    # see: https://bokeh.pydata.org/en/latest/docs/reference/models/sources.html#bokeh.models.sources.ColumnDataSource
    source = ColumnDataSource(data=dict(x=[1], y=[0]))
    p.circle(x='x', y='y', size=12, fill_color='white', source=source)

    def update():
        # get the last (x, y) from current source
        x, y = source.data['x'][-1], source.data['y'][-1]

        # construct the new values for all columns, and pass to stream
        new_data = dict(x=[x * cos(0.1) - y * sin(0.1)], y=[x * sin(0.1) + y * cos(0.1)])
        # https://bokeh.pydata.org/en/latest/docs/reference/models/sources.html#bokeh.models.sources.ColumnDataSource.stream
        source.stream(new_data, rollover=5)

    doc.add_periodic_callback(update, 1000)  # callback made via websocket
    doc.add_root(p)


modify_doc(curdoc())
