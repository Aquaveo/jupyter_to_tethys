
from bokeh.io import curdoc
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Slider
from bokeh.models.widgets import Paragraph


# This is a bokeh app! Should run with a bokeh server!!
# This bokeh can run outside of jupyter as well!
# bokeh widget on_change event only work with bokeh server
def modify_doc(doc):
    p = Paragraph(text=""" """, width=800, height=100)

    def callback(attr, old, new):
        print("called")  # This outputs to console (In Jupyter goes back to UI via Jupyter websocket)
        p.text = "{}:{}->{}".format(attr, old, new)  # This outputs to widget UI via bokeh websocket

    slider_bokeh = Slider(start=0, end=100, value=1, step=.1, title="Stuff")

    # widget on_change event can only with bokeh server
    slider_bokeh.on_change("value", callback)
    doc.add_root(widgetbox(p, slider_bokeh))


modify_doc(curdoc())
