import holoviews as hv
hv.extension('bokeh', 'matplotlib', width="100")
import param, panel as pp
from colorcet import palette
import dask.dataframe as dd, geoviews as gv, cartopy.crs as crs
from colorcet import fire
from holoviews.operation.datashader import datashade
from geoviews.tile_sources import EsriImagery

topts = dict(width=700, height=600, bgcolor='black', xaxis=None, yaxis=None, show_grid=False)
tiles = EsriImagery.clone(crs=crs.GOOGLE_MERCATOR).options(**topts)


dopts = dict(width=1000, height=600, x_sampling=0.5, y_sampling=0.5)


taxi  = dd.read_parquet('/home/drew/pyviz/data/nyc_taxi_wide.parq').persist()

taxi = taxi.compute()
taxi = taxi.sort_values("tpep_pickup_datetime")

class NYCTaxi(param.Parameterized):
    alpha = param.Magnitude(default=0.75, doc="Map tile opacity")
    cmap = param.ObjectSelector('fire', objects=['fire','bgy','bgyw','bmy','gray','kbc'])
    location = param.ObjectSelector(default='dropoff', objects=['dropoff', 'pickup'])

    def make_view(self, **kwargs):
        print(kwargs)
        pts   = hv.Points(taxi, [self.location+'_x', self.location+'_y'])
        trips = datashade(pts, cmap=palette[self.cmap], **dopts)
        return tiles.options(alpha=self.alpha) * trips

explorer = NYCTaxi(name="Taxi explorer")
panel_viewable = pp.Row(explorer, explorer.make_view)

doc = panel_viewable.server_doc()
