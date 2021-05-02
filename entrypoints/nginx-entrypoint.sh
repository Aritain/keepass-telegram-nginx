#!/bin/bash

set -e

python3 /main.py > /etc/nginx/nginx.conf
nginx -g 'daemon off;'

