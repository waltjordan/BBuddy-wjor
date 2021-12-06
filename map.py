from tkinter import *
import requests
from io import BytesIO
from PIL import Image
from urllib import request as req
import sqlite3 as sl
import folium
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore

import io
import sys

class mapView():

    def __init__(self):
        conn = sl.connect("berries.db")
        fg = folium.FeatureGroup()
        cali = [37.7783, -119.4179]
        markerMap = folium.Map(location = cali, zoom_start = 6.5, tiles = 'Stamen Terrain')
        with conn:
            data = conn.execute("SELECT * FROM amtable")
            for row in data:
                name = row[0]
                location = [row[1],row[2]]
                folium.Marker(location = location, tooltip = name).add_to(markerMap)
                folium.Marker(location = location, tooltip = name).add_to(fg)
        conn.close()
        markerMap.fit_bounds(fg.get_bounds(), padding=0.5)
        data = BytesIO()
        markerMap.save("berrymap.html", close_file=False)
        app = QtWidgets.QApplication(sys.argv)
        window = QtWebEngineWidgets.QWebEngineView()
        #window.setHtml(data.getvalue().decode())
        window.load(QtCore.QUrl("www.google.com"))
        window.setWindowTitle("Berry Map")
        window.resize(1000,600)
        window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        window.show()
        app.exec_()

    def createMap_old(filename_wo_extension, center=None, zoom=None, imgsize="500x500", imgformat="jpeg", maptype="satellite", markers=None):
        # need to get lat/long from db (currently text files)
        # also need berry name for marker Name
        request = "http://maps.google.com/maps/api/staticmap?"
        if center != None:
            request += "center=%s&" % center
        if center != None:
            request += "zoom=%i&" % zoom
        request += "size=%ix%i&" % (imgsize)  # tuple of ints, up to 640 by 640
        request += "format=%s&" % imgformat
        request += "maptype=%s&" % maptype
        if markers != None:
            for marker in markers:
                    request += "%s&" % marker
        request += "sensor=false&"   # must be given, deals with getting loction from mobile device
        request += "key=AIzaSyCz2WexsSRoX06wi7nkEqT1omuoWN4Pji4&"
        response = requests.get(request)
        Image.open(BytesIO(response.content)).convert('RGB').save(filename_wo_extension + "." + imgformat)
        Image.show()





if __name__ == "__main__":
    mapView()
