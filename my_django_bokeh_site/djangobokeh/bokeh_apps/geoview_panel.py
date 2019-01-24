import geoviews as gv
import holoviews as hv
import panel as pp

hv.extension('bokeh')

boxes = gv.Polygons([]).options(fill_alpha=0.4, line_width=2)
box_stream = hv.streams.BoxEdit(source=boxes, num_objects=1)

import param

class MyParam(param.Parameterized):
    alpha = param.Number(0.5, bounds=(0, 1), doc="alpha")

myparam = MyParam()

def change_basemap(**kw):
    print("change_basemap: " + str(kw))
    tiles = gv.tile_sources.Wikipedia.options(global_extent=True, height=400, width=700, alpha=kw["alpha"])
    return tiles * boxes


dmp = hv.DynamicMap(change_basemap, streams=[box_stream, myparam])


panel_viewable = pp.Column(myparam, dmp)
doc = panel_viewable.server_doc()

