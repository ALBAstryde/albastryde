import os
from django.contrib.gis.utils import LayerMapping
from models import mun98nic, mun98nic_mapping
from models import dep50nic, dep50nic_mapping

mun98nic_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/mun98nic.shp'))
dep50nic_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/dep50nic.shp'))

def run(verbose=True):
    lm = LayerMapping(mun98nic, mun98nic_shp, mun98nic_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)
    lm = LayerMapping(dep50nic, dep50nic_shp, dep50nic_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)


from lugar.models import Departamento, Municipio
def load():
    dqs=Departamento.objects.all()
    mqs=Municipio.objects.all()

    for i in mqs:
        i.save(force_update=True)

    for i in dqs:
        i.save(force_update=True)
