#!/usr/bin/python
# coding: utf-8
import locale
import os
import sys

from Tasker.API.config import ProductionConfig, DevelopmentConfig
from Tasker.API.core.Factory import create_app

config = DevelopmentConfig
use_reloader = True
if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
    config = ProductionConfig
    use_reloader = False

# Setting locale for date conversions
if sys.platform.lower().startswith('linux'):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
elif sys.platform.lower().startswith('win'):
    locale.setlocale(locale.LC_TIME, 'fr-FR')
else:
    locale.setlocale(locale.LC_TIME, 'fr_FR')

app = create_app(config)


if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0", use_reloader=use_reloader)