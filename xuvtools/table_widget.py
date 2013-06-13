#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from qt_table_widget import *

class My_UI_Window(Ui_MainWindow):
    def __init__(self):
        '''This list contains the list of cells in logical order, which
        represent the positions in consecutive order. Values are tuples of
        the form [row, col].
        '''
        self.clist = []
        # define the list of available orderings:
        self.orderings = [
            self.order_leftright_topbottom,
            self.order_leftright_bottomtop,
            self.order_topbottom_leftright,
            self.order_bottomtop_leftright,
            self.order_snakeline_topleft,
            self.order_snakeline_topright
        ]
        self.update_cellslist = self.orderings[0]
        self.rows = 0
        self.cols = 0

    def setupUi(self, MainWindow):
        super(My_UI_Window, self).setupUi(MainWindow)
        MainWindow.setWindowTitle("Grid Aligner")
        QtCore.QObject.connect(self.sb_h, QtCore.SIGNAL("valueChanged(int)"), self.set_cols)
        QtCore.QObject.connect(self.sb_v, QtCore.SIGNAL("valueChanged(int)"), self.set_rows)
        QtCore.QObject.connect(self.pb_inc_h, QtCore.SIGNAL("clicked()"), self.inc_cols)
        QtCore.QObject.connect(self.pb_dec_h, QtCore.SIGNAL("clicked()"), self.dec_cols)
        QtCore.QObject.connect(self.pb_inc_v, QtCore.SIGNAL("clicked()"), self.inc_rows)
        QtCore.QObject.connect(self.pb_dec_v, QtCore.SIGNAL("clicked()"), self.dec_rows)
        QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL("cellChanged(int, int)"), self.update_cell_status)
        QtCore.QObject.connect(self.cb_ordering, QtCore.SIGNAL("currentIndexChanged(int)"), self.set_ordering)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.cols = self.tableWidget.columnCount()
        self.rows = self.tableWidget.rowCount()
        self.change_table_size(2, 2)

    def block_table_signals(self, b):
        '''Blocks/unblocks signal from the table.

        Parameters
        ----------
        b : bool
        '''
        QtCore.QObject.blockSignals(self.tableWidget, b)

    def set_ordering(self, idx):
        self.update_cellslist = self.orderings[idx]
        self.update_cellslist()

    def inc_cols(self):
        self.change_table_size(self.rows, self.cols + 1)

    def dec_cols(self):
        self.change_table_size(self.rows, self.cols - 1)

    def set_cols(self, ncols):
        self.change_table_size(self.rows, ncols)

    def inc_rows(self):
        self.change_table_size(self.rows + 1, self.cols)

    def dec_rows(self):
        self.change_table_size(self.rows - 1, self.cols)

    def set_rows(self, nrows):
        self.change_table_size(nrows, self.cols)

    def order_leftright_topbottom(self):
        '''Fill the cellslist with the (row,col) tuples in the appropriate
        order, each line from left to right (ls = linescan), from top to
        bottom (tb).'''
        cells = np.zeros(shape=(self.rows * self.cols, 2), dtype=int)
        self.cellsval = np.zeros((self.rows, self.cols), dtype=int)
        for row in range(self.rows):
            for col in range(self.cols):
                cells[(row * self.cols) + col] = [row, col]
        # FIXME: the clist must be filled with the correct values representing
        # the current checked/unchecked status!!
        self.clist = np.ma.array(cells, mask=[0])

    def order_leftright_bottomtop(self):
        '''Fill the cellslist with the (row,col) tuples in the appropriate
        order, each line from left to right (ls = linescan), from bottom to
        top (bt).'''
        cells = np.zeros(shape=(self.rows * self.cols, 2), dtype=int)
        self.cellsval = np.zeros((self.rows, self.cols), dtype=int)
        for row in range(self.rows):
            line = (self.rows - 1) * (self.cols) - (row * self.cols)
            for col in range(self.cols):
                cells[(line) + col] = [row, col]
                # print "%s: [%s, %s]" % (line + col, row, col)
        self.clist = np.ma.array(cells, mask=[0])

    def order_topbottom_leftright(self):
        '''Fill the cellslist with the (row,col) tuples in the appropriate
        order, each row from top to bottom, from left to right.'''
        cells = np.zeros(shape=(self.rows * self.cols, 2), dtype=int)
        self.cellsval = np.zeros((self.rows, self.cols), dtype=int)
        for col in range(self.cols):
            for row in range(self.rows):
                # print "%s: [%s, %s]" % ((col * self.rows) + row, row, col)
                cells[(col * self.rows) + row] = [row, col]
        self.clist = np.ma.array(cells, mask=[0])

    def order_bottomtop_leftright(self):
        '''Fill the cellslist with the (row,col) tuples in the appropriate
        order, each row from bottom to top, from left to right.'''
        cells = np.zeros(shape=(self.rows * self.cols, 2), dtype=int)
        self.cellsval = np.zeros((self.rows, self.cols), dtype=int)
        for row in range(self.rows):
            for col in range(self.cols):
                # print "%s: [%s, %s]" % (self.rows - 1 + (col * self.rows) - row, row, col)
                cells[self.rows - 1 + (col * self.rows) - row] = [row, col]
        self.clist = np.ma.array(cells, mask=[0])

    def order_snakeline_topleft(self):
        cells = np.zeros(shape=(self.rows * self.cols, 2), dtype=int)
        self.cellsval = np.zeros((self.rows, self.cols), dtype=int)
        for row in range(self.rows):
            line = row * self.cols
            for col in range(self.cols):
                if (row % 2) == 0:
                    cells[line + col] = [row, col]
                else:
                    cells[(line + self.cols - 1) - col] = [row, col]
        self.clist = np.ma.array(cells, mask=[0])

    def order_snakeline_topright(self):
        cells = np.zeros(shape=(self.rows * self.cols, 2), dtype=int)
        self.cellsval = np.zeros((self.rows, self.cols), dtype=int)
        for row in range(self.rows):
            line = row * self.cols
            for col in range(self.cols):
                if (row % 2) == 0:
                    cells[(line + self.cols - 1) - col] = [row, col]
                else:
                    cells[line + col] = [row, col]
        self.clist = np.ma.array(cells, mask=[0])

    def unmasked_idx(self, row, col):
        return self.clist.data.tolist().index([row, col])

    def masked_idx(self, row, col):
        return np.ma.compress_rows(self.clist).tolist().index([row, col])

    def gen_cell(self, row, col, text=''):
        '''Create and assign a new table cell.

        Creates the content widget for a cell, assigns the default state
        (checked) and puts the item at the given place in the table.

        Parameters
        ----------
        row, col : int
            The location of the new cell in the table.
        text : string
            The text to be shown in the cell.
        '''
        cell = QtGui.QTableWidgetItem(text)
        cell.setCheckState(QtCore.Qt.Checked)
        self.tableWidget.setItem(row, col, cell)

    def cell_enable(self, row, col):
        self.clist.mask[self.unmasked_idx(row, col)] = False
        return self.masked_idx(row, col)

    def cell_disable(self, row, col):
        '''Here we need to look up the masked index before disabling the
        cell, otherwise it can't be found anymore.'''
        idx = self.masked_idx(row, col)
        self.clist.mask[self.unmasked_idx(row, col)] = True
        return idx

    def is_enabled(self, row, col):
        try:
            self.clist.tolist().index([row, col])
        except ValueError:
            return False
        return True

    def update_cell_status(self, row, col):
        # print 'this is update_cell_status %s %s' % (row, col)
        item = self.tableWidget.item(row, col)
        if item is None:
            # print "item at (%s, %s) is None, creating one" % (row, col)
            idx = self.masked_idx(row, col)
            cell = QtGui.QTableWidgetItem(str(idx))
            cell.setCheckState(QtCore.Qt.Checked)
            self.tableWidget.setItem(row, col, cell)
        else:
            # the new status is defined by the checkbox
            # print "item at (%s, %s) exists" % (row, col)
            newstat = item.checkState()
            curstat = self.is_enabled(row, col) * 2
            if (curstat != newstat):
                if newstat == 2:
                    idx = self.cell_enable(row, col)
                    item.setText(str(idx))
                else:
                    idx = self.cell_disable(row, col)
                    item.setText('--')
                for i in range(idx, len(np.ma.compress_rows(self.clist))):
                    [trow, tcol] = np.ma.compress_rows(self.clist)[i]
                    titem = self.tableWidget.item(trow, tcol)
                    titem.setText(str(i))
        return item

    def upd_celltext(self, start=0, end=0):
        '''Update the contents (index numbers) for a range of cells.

        Updates the value shown in a cell (representing its position
        in the consecutive list) for a specified range of clist index
        numbers.

        Parameters
        ----------
        start, end : int, optional
            The range of clist index numbers to update.
        '''
        self.block_table_signals(True)
        if end == 0:
            end = len(np.ma.compress_rows(self.clist))
        print "this is upd_celltext(%s, %s)" % (start, end)
        print np.ma.compress_rows(self.clist)
        for i in range(start, end):
            try:
                [trow, tcol] = np.ma.compress_rows(self.clist)[i]
                print "%s: (%s, %s)" % (i, trow, tcol)
            except IndexError:
                print "%s: not in clist" % i
                pass
            # print "ctx (%s, %s): %s" % (trow, tcol, i)
            titem = self.tableWidget.item(trow, tcol)
            titem.setText(str(i))
        self.block_table_signals(False)

    def change_table_size(self, nrows, ncols):
        if nrows < 1:
            nrows = 1
        if ncols < 1:
            ncols = 1
        dcols = ncols - self.cols
        drows = nrows - self.rows
        if drows + dcols == 0:
            return
        print 'change_table_size from (%s, %s) to (%s, %s)' % \
            (self.rows, self.cols, nrows, ncols)
        # adjust number of columns:
        for i in range(dcols):
            self.tableWidget.insertColumn(0)
        for i in range(dcols * -1):
            self.tableWidget.removeColumn(0)
        # adjust number of rows:
        for i in range(drows):
            self.tableWidget.insertRow(0)
        for i in range(drows * -1):
            self.tableWidget.removeRow(0)
        self.rows = self.tableWidget.rowCount()
        self.cols = self.tableWidget.columnCount()
        self.sb_v.setValue(self.rows)
        self.sb_h.setValue(self.cols)
        self.update_cellslist()
        # print self.clist
        # update cell contents:
        for (row, col) in self.clist:
            self.update_cell_status(row, col)


if __name__ == "__main__":
    # instantiate a QApplication object
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = My_UI_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
