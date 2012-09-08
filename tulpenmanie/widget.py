# Tulpenmanie, a commodities market client.
# Copyright (C) 2012  Emery Hemingway
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from decimal import *

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtProperty

import tulpenmanie.commodity

class CommodityWidgetBase(object):

    def get_prefix(self):
        return tulpenmanie.commodity.model.item(
            self.commodity_row, tulpenmanie.commodity.model.PREFIX).text()
    prefix = property(get_prefix)

    def get_suffix(self):
        return tulpenmanie.commodity.model.item(
            self.commodity_row, tulpenmanie.commodity.model.SUFFIX).text()
    suffix = property(get_suffix)

    def get_precision(self):
        precision = tulpenmanie.commodity.model.item(
            self.commodity_row, tulpenmanie.commodity.model.PRECISION).text()
        if not precision:
            precision = None
        else:
            precision = int(precision)
        return precision
    precision = property(get_precision)


class CommodityLcdWidget(QtGui.QLCDNumber, CommodityWidgetBase):
    # maybe display prefixes/suffixes as well

    def __init__(self, commodity_row, parent=None):
        super(CommodityLcdWidget, self).__init__(parent)
        self.commodity_row = commodity_row

        self.setStyleSheet('background : black')
        self.default_palette = QtGui.QPalette(self.palette())
        self.default_palette.setColor(QtGui.QPalette.WindowText,
                                      QtCore.Qt.white)

        self.increase_palette = QtGui.QPalette(self.palette())
        self.increase_palette.setColor(QtGui.QPalette.WindowText,
                                       QtCore.Qt.green)

        self.decrease_palette = QtGui.QPalette(self.palette())
        self.decrease_palette.setColor(QtGui.QPalette.WindowText,
                                       QtCore.Qt.red)
        self.setSegmentStyle(self.Flat)

        self.value = None

    def setValue(self, value):
        if self.value and value > self.value:
            self.setPalette(self.increase_palette)
        elif self.value and value < self.value:
            self.setPalette(self.decrease_palette)
        else:
            self.setPalette(self.default_palette)

        self.value = value
        if self.precision:
            value_string = str(round(value, self.precision))
            left, right = value_string.split('.')
            value_string = left + '.' + right.ljust(self.precision, '0')
        else:
            value_string = str(value)

        # This probably takes the radix point into account,
        # which doesn't take up a digit when displayed
        length = len(value_string)
        if self.digitCount() < length:
            self.setDigitCount(length)
        self.display(value_string)


class CommoditySpinBox(QtGui.QDoubleSpinBox, CommodityWidgetBase):

    def __init__(self, commodity_row, parent=None):
        super(CommoditySpinBox, self).__init__(parent)
        self.commodity_row = commodity_row

        self.setPrefix(self.get_prefix())
        self.setSuffix(self.get_suffix())
        if self.precision:
            self.setDecimals(self.precision)


class CommodityWidget(QtGui.QLabel, CommodityWidgetBase):

    #alignment = QtCore.Qt.AlignRight

    def __init__(self, commodity_row, parent=None):
        super(CommodityWidget, self).__init__(parent)
        self.commodity_row = commodity_row
        self.value = None

    def setValue(self, value):
        if self.value and value > self.value:
            self.setStyleSheet('color : green')
        elif self.value and value < self.value:
            self.setStyleSheet('color : red')
        else:
            self.setStyleSheet('color : black')
        self.value = value

        if self.precision:
            value = round(value, self.precision)
        self.setText(self.prefix + str(value) + self.suffix)

    def change_value(self, change):
        value = self.value + change
        if value > self.value:
            self.setStyleSheet('color : green')
        elif value < self.value:
            self.setStyleSheet('color : red')
        else:
            self.setStyleSheet('color : black')
        self.value = value

        if self.precision:
            value = round(value, self.precision)
        self.setText(self.prefix + str(value) + self.suffix)


class UuidComboBox(QtGui.QComboBox):

    #TODO set the default tulpenmanie.commodity.model column to 1

    def _get_current_uuid(self):
        return self.model().item(self.currentIndex(), 0).text()

    def _set_current_uuid(self, uuid):
        results = self.model().findItems(uuid)
        if results:
            self.setCurrentIndex(results[0].row())
        else:
            self.setCurrentIndex(-1)

    currentUuid = pyqtProperty(str, _get_current_uuid, _set_current_uuid)