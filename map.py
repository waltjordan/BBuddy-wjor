import folium
import sys
import sqlite3 as sl
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore

class mapView():

    # updates map markers
    def updateMap(self):

        conn = sl.connect("berries.db") # connect to the DB
        fg = folium.FeatureGroup() # used to keep track of all markers
        cali = [37.7783, -119.4179] # static lat/long for center of California

        # tiles shows more of a satellite terrain, starting zoom is state scale
        markerMap = folium.Map(location = cali, zoom_start = 6, tiles = 'Stamen Terrain')

        # this section imports and creates markers for all markers in the DB
        with conn:
            data = conn.execute("SELECT * FROM amtable")
            for row in data:
                name = row[0]
                location = [row[1],row[2]]
                folium.Marker(location = location, tooltip = name).add_to(markerMap)
                # must also add a copy to the group so we know about it
                folium.Marker(location = location, tooltip = name).add_to(fg)
        markerMap.save("berrymap.html")
        conn.close()

    # renders map window
    def loadMap(self):

        # create new PyQt5 app
        app = QtWidgets.QApplication(sys.argv)
        # make the window for that app
        window = QtWebEngineWidgets.QWebEngineView()
        # load html from disk and show window
        window.load(QtCore.QUrl.fromLocalFile(QtCore.QFileInfo("berrymap.html").absoluteFilePath()))
        window.setWindowTitle("Berry Map")
        window.resize(1000,600)
        window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        window.show()
        app.exec_()

if __name__ == "__main__":
    mapView().loadMap()
