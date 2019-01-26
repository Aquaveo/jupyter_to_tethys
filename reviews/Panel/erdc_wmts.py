import quest
import geoviews as gv
import holoviews as hv
import panel as pp

hv.extension('bokeh')


quest_service = 'svc://wmts:seamless_imagery'
tile_service_options = quest.api.get_download_options(quest_service, fmt='param')[quest_service]

boxes = gv.Polygons([]).options(fill_alpha=0.4, line_width=2)
box_stream = hv.streams.BoxEdit(source=boxes, num_objects=1)

import param

class MyParam(param.Parameterized):
    alpha = param.Number(0.5, bounds=(0, 1), doc="alpha")

myparam = MyParam()

def change_basemap(**kw):
    print("change_basemap: " + str(kw))
    url = kw['url']
    alpha = kw["alpha"]
    tiles = gv.WMTS(url).options(global_extent=True, height=400, width=700, alpha=alpha)
    return tiles * boxes


dmp = hv.DynamicMap(change_basemap, streams=[tile_service_options, box_stream, myparam])


def update_subset(**kw):
    print("update_subset: " + str(kw))
    if box_stream.element:
        data = box_stream.data
        bbox = [data['x0'][0], data['y0'][0], data['x1'][0], data['y1'][0]]
    else:
        bbox = [-72.43925984610391, 45.8471360126193, -68.81252476472281, 47.856449699679516]

    # Param Object Changed! This triggers callback change_basemap()
    tile_service_options.bbox = bbox
    arr = quest.api.get_data(
            service_uri=quest_service,
            search_filters=None,
            download_options=tile_service_options,
            collection_name='examples',
            use_cache=False,
            as_open_datasets=True, )[0]

    image = gv.RGB((arr.x, arr.y, arr[0].values,
                    arr[1].values, arr[2].values),
                   vdims=['R', 'G', 'B']).options(width=700, height=400, alpha=0.7)
    return gv.tile_sources.Wikipedia * image

button = pp.widgets.Button(name='Subset', button_type='danger')
dmp_subset = hv.DynamicMap(update_subset, streams=[button])

#pp.Column(tile_service_options, dmp, button, dmp_subset)

# import numpy
# def change_myparam():
#     myparam.alpha = numpy.random.random()

# See:
#  http://pyviz.org/tutorial/13_Deploying_Bokeh_Apps.html
#  https://github.com/pyviz/panel/blob/58826d04396c2611131cda9462c85b0a5f369ef7/panel/viewable.py#L94

panel_viewable = pp.Column(tile_service_options, myparam, dmp, button, dmp_subset)
doc = panel_viewable.server_doc()
#doc.add_periodic_callback(change_myparam, 1000)

