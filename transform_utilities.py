#!/usr/bin/env python
# Contains some utilities shared across transforms.
# Probably requires more testing... only one fail case handled, currently.

# Get urlretrieve from the right spot. Can be simplified to the second method when we're only Python3.
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve
import os


def update_local_file(remote_url, local_file):
    out_file, result = urlretrieve(remote_url, local_file)
    try:
        content_length = result['Content-Length']
        print("Successfully download file of size {} to {}".format(content_length, local_file))
    except KeyError:
        print("Failed to download file with error: {}".format(result['Status']))
        os.remove(local_file)
