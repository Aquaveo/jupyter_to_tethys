# Subject to Bokeh Bug: Tool Bar disappears https://github.com/ioam/holoviews/issues/2784
import quest
import geoviews as gv
import holoviews as hv
from holoviews.streams import (Params, PolyEdit, BoxEdit, PointDraw)
# from holoviews.operation.datashader import regrid
import panel as pp
# import param

hv.extension('bokeh')
# pp.extension()

tiles = gv.tile_sources.StamenTerrain().options(width=950, height=600)
tiles.extents = (-125, 25, -65, 50)
box_poly = gv.Polygons([]).options(fill_alpha=.2)
box_stream = BoxEdit(source=box_poly, num_objects=1, name="boxedit")
points = gv.Points([])
point_stream = PointDraw(source=points)

elevation_service = quest.util.ServiceSelector(parameter='elevation', default='svc://usgs-ned:1-arc-second')

# Explicitly create a panel widget
btn_download = pp.widgets.Button(name='Download & Fill', button_type='danger')
btn_download_stream = Params(btn_download, ['clicks'], rename={'clicks': 'download_clicks'})

btn_run = pp.widgets.Button(name='Extract', button_type='danger')
btn_run_stream = Params(btn_run, ['clicks'], rename={'clicks': 'run_clicks'})

btn_delin = pp.widgets.Button(name='Delinate', button_type='danger')
btn_delin_stream = Params(btn_delin, ['clicks'], rename={'clicks': 'delin_clicks'})

slider_extract = pp.widgets.IntSlider(name='Stream Threshold', width=200, start=0, end=10, value=1)

map_elements = tiles * box_poly
stream_extract_options = None
elevation_filled = None
streams = None
fill_dataset = None
st_dataset = None


def dmp_callback(*args, **kw):
    global stream_extract_options
    global elevation_filled
    global tiles
    global points
    global box_poly
    global streams
    global fill_dataset
    global st_dataset

    if box_stream.element:
        xs, ys = box_stream.element.array().T
        bbox = [xs[0], ys[1], xs[2], ys[0]]
    else:
        bbox = [-90.88870324076336, 32.245105881134, -90.78133198716839, 32.37688211930573]
    print('BOUNDS:', bbox)
    tiles.extents = tuple(bbox)

    if box_stream._triggering:
        print("Box stream is triggering")
        elements = tiles * box_poly * points

    elif btn_download_stream._triggering:

        # import pdb
        # pdb.set_trace()
        print("btn_download_stream is triggering")

        elevation_raster = quest.api.get_seamless_data(
            service_uri=elevation_service.service,
            bbox=bbox,
            collection_name='examples',
            use_cache=False,    # in standalone Bokeh app this should be set False
            as_open_dataset=False,
        )
        fill_dataset = quest.tools.wbt_fill_depressions(
            dataset=elevation_raster,
        )['datasets'][0]
        fill = quest.api.open_dataset(fill_dataset, with_nodata=True, isel_band=0)

        elevation_filled = gv.Image(fill, ['x', 'y']).options(alpha=0.8)

        stream_extract_options = quest.tools.wbt_extract_streams_workflow
        stream_extract_options.params()['dataset'].precedence = -1
        stream_extract_options.dataset = fill_dataset
        stream_extract_options.set_threshold_bounds()

        print("Bounds" + str(stream_extract_options.params()["stream_threshold"].bounds))
        start, end = stream_extract_options.params()["stream_threshold"].bounds
        slider_extract.start = start
        slider_extract.end = end
        slider_extract.value = stream_extract_options.stream_threshold

        elements = tiles * elevation_filled * box_poly * points

    elif btn_run_stream._triggering:
        print("btn_run_stream is triggering")

        stream_extract_options.stream_threshold = slider_extract.value
        st_dataset = stream_extract_options()['datasets'][0]
        st = quest.api.open_dataset(st_dataset, with_nodata=True, isel_band=0)
        streams = gv.Image(st, ['x', 'y']).options(cmap='Greens')

        elements = tiles * box_poly * elevation_filled * streams * points

    elif btn_delin_stream._triggering:
        print("btn_delin_stream is triggering")

        if point_stream.element:
            original_outlets = [(x, y) for x, y in zip(*point_stream.element.array().T)]
        else:
            original_outlets = (-90.883981967599979, 32.291221825861946)
        result = quest.tools.wbt_watershed_delineation_workflow(
            elevation_dataset=fill_dataset,
            streams_dataset=st_dataset,
            snap_distance=0.1,
            outlets=original_outlets,
        )
        watersheds, snapped_outlets, catalog_entry = result['catalog_entries']

        outline = gv.Polygons(watersheds).options(alpha=0.5, color="yellow")
        original_points = gv.Points(original_outlets).options(color='blue', size=12)
        snapped_points = gv.Points(snapped_outlets).options(color='green', size=12)
        elements = tiles * box_poly * original_points * outline * snapped_points * streams * points

    else:
        print("someone is triggering")
        elements = tiles * box_poly * points

    return elements


dmp = hv.DynamicMap(dmp_callback, streams=[box_stream, btn_download_stream, btn_run_stream, btn_delin_stream])

panel_viewable = pp.Column(pp.Row(elevation_service, btn_download),
          pp.Row(slider_extract, btn_run),
          btn_delin,
          dmp)

doc = panel_viewable.server_doc()
