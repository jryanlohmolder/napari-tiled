"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""

from napari.utils.notifications import show_info
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
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

        # self.url_entry = QTextEdit()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter a url")
        self.connect_button = QPushButton("Connect")
        self.connection_label = QLabel("No url connected")

        self.connection_widget = QWidget()
        connection_layout = QVBoxLayout()
        connection_layout.addWidget(self.url_entry)
        connection_layout.addWidget(self.connect_button)
        connection_layout.addWidget(self.connection_label)
        connection_layout.addStretch()
        self.connection_widget.setLayout(connection_layout)

        self.catalog_table = QTableWidget(0, 1)
        self.catalog_table.setHorizontalHeaderLabels(["ID"])
        self.catalog_table.setVisible(False)

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Orientation.Vertical)

        self.splitter.addWidget(self.connection_widget)
        self.splitter.addWidget(self.catalog_table)

        self.splitter.setStretchFactor(1, 2)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        self.connect_button.clicked.connect(self._on_connect_clicked)

    def _on_connect_clicked(self):
        url = self.url_entry.displayText()
        if not url:
            show_info("Please specify a url.")
            return
        try:
            self.catalog = from_uri(url)
        except Exception:
            show_info("Could not connect. Please check the url.")
            return
        self.connection_label.setText(f"Connected to {url}")
        self.catalog_table.setVisible(True)
        self._populate_table(self.catalog)

    def _populate_table(self, catalog):
        for node in catalog:
            item = QTableWidgetItem(node)
            last_row_position = self.catalog_table.rowCount()
            self.catalog_table.insertRow(last_row_position)
            self.catalog_table.setItem(last_row_position, 0, item)
