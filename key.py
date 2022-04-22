#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json


def _getKey():
    with open("./key.json", "r") as f:
        return json.load(f)


keyDict = _getKey()
