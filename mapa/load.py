import os
from django.contrib.gis.utils import LayerMapping
from models import zoninac_50000, zoninac_50000_mapping

zoninac_50000_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/zoninac_50000.shp'))

def run(verbose=True):
    lm = LayerMapping(zoninac_50000, zoninac_50000_shp, zoninac_50000_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)

