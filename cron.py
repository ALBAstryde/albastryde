#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from valuta import download
download.get_Euros()
download.get_USD()
