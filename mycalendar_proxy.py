
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QVariant, QDateTime, QSortFilterProxyModel

class ProxyCalendar(QSortFilterProxyModel):
    def __init__(self):
        super(ProxyCalendar, self).__init__()

    def filterAcceptsRow(self, row, parent):
        return True

    def headerData(self, column, orientation, role = Qt.DisplayRole):
        sourceModel = self.sourceModel()

        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignHCenter|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignHCenter|Qt.AlignVCenter))

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return QVariant( sourceModel.columns[column] )
            else:
                return QVariant()
        else:
            return QVariant()

        return QVariant(int(column+1))