#!/usr/bin/env python
# Contains some utilities shared across transforms.
# Probably requires more testing... only one fail case handled, currently.

# Get urlretrieve from the right spot. Can be simplified to the second method when we're only Python3.
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve
import os

from qgis.core import QgsMessageLog


def update_local_file(remote_url, local_file):
    log("Downloading file to: {}".format(local_file))
    try:
        out_file, result = urlretrieve(remote_url, local_file)
    except IOError:
        return False

    try:
        content_length = result['Content-Length']
        if content_length < 1000:
            os.remove(local_file)
    except KeyError:
        os.remove(local_file)
        return False
    return True


def log(message, error=False):
    log_level = QgsMessageLog.INFO
    if error:
        log_level = QgsMessageLog.CRITICAL
    QgsMessageLog.logMessage(message, 'Processing', level=log_level)
