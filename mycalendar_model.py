#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QVariant, QModelIndex, QAbstractTableModel, QDateTime
from PyQt5.QtGui import QColor


class ModelCalendar(QAbstractTableModel):
	"""Abstract model for qtableview."""
	headersName = ['Date', 'Datetime', 'Days', 'Month', 'Year', 'WeekDay', 'Week_number_Sunday', 'Week_number_Monday', 'Day_Year', 'litteral_Date', 'litteral_Date_short', 'litteral_Day', 'litteral_Day_short', 'litteral_Month', 'litteral_Month_short', 'public_french_holidays']

	def __init__(self, array, parent = None):
		"""Init Model Abstract."""
		super(ModelCalendar, self).__init__(parent)
		self.parent = parent
		self.columns = self.headersName
		self.arraydata = array
	
	def headerData(self, section, orientation, role=Qt.DisplayRole):
		"""Set the name list to column name."""
		if role != Qt.DisplayRole:
			return QVariant()
		if orientation == Qt.Horizontal:
			return self.columns[section]
		return QVariant()
	
	def rowCount(self, parent=QModelIndex()):
		"""Get total rows."""
		return len(self.arraydata) 
	
	def columnCount(self, parent=QModelIndex()):
		"""Get total columns."""
		return len(self.columns) 
	
	def data(self, index, role=Qt.DisplayRole):
		"""Get datas."""
		if not index.isValid(): 
			return QVariant() 
		elif role == Qt.TextColorRole:
			currentdate = QDateTime.currentDateTime().toString('yyyyMMdd')
			if self.arraydata[index.row()][self.columns.index('Datetime')]  == currentdate:
				return QVariant(QColor(204, 24, 66))
		elif role == Qt.BackgroundRole:
			if self.arraydata[index.row()][self.columns.index('WeekDay')] in ['0', '6']:
				return QVariant(QColor(218, 220, 235))
			if self.arraydata[index.row()][self.columns.index('public_french_holidays')] != '':
				return QVariant(QColor(204, 222, 235))	
		elif role == Qt.TextAlignmentRole:
			# TextAlignmentRole
			return QVariant()
		elif role != Qt.DisplayRole:
			return QVariant()
		return QVariant(self.arraydata[index.row()][index.column()])
	
	def getData(self, row, colname=None, col=None):
		if self.rowCount() > 0:
			if col is None:
				return self.arraydata[row][self.myindex.index(colname)]
			elif colname is None:
				return self.arraydata[row][col]
		return QVariant()
	
	def getList(self, colname, desc=True):
		"""Build list column."""
		mylist = []
		for row in range(self.rowCount()):
			itemlist = self.arraydata[row][self.myindex.index(colname)]
			if itemlist not in mylist:
				mylist.append(itemlist)
		mylist.sort(reverse=desc)
		return mylist