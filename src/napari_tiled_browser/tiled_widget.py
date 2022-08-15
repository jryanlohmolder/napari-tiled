"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""

from napari.utils.notifications import show_info
from qtpy.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget
from tiled.client import from_uri


class TiledBrowser(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.catalog = None

        self.url_entry = QTextEdit()
        self.connect_button = QPushButton("Connect")
        self.test_label = QLabel("No url connected")

        layout = QVBoxLayout()
        layout.addWidget(self.url_entry)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.test_label)
        self.setLayout(layout)

        self.connect_button.clicked.connect(self._on_connect_clicked)

    def _on_connect_clicked(self):
        url = self.url_entry.toPlainText()
        if not url:
            show_info("Please specify a url.")
            return
        print(f"{url = }")
        try:
            self.catalog = from_uri(url)
        except Exception:
            self.test_label.setText("No url connected")
            show_info("Could not connect. Please check the url.")
            return
        print(self.catalog)
        self.test_label.setText(f"Connected to {url}")
