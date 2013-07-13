#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI for statistics calculations from MTrack2 tracklists.
"""

import sys
import argparse
from mtrack2_stats import gen_stats
from ui_generic_in_out_opt import *


def select_file(element):
    """Show file dialog and update an elements text with the result.

    This is a callback function for usage with "Browse" buttons or similar in a
    PyQt GUI. It displays the system's file selection dialog and updates the
    supplied GUI element with the result. To use it with Qt's connect() method,
    a lambda function must be used there, e.g.

    >>> connect(btn, sig, lambda elt=self.line_edit: select_file(elt))

    The main purpose of this is to eliminate the need for implementing a
    separate callback function for each slot, resulting in many more or less
    identical code segments.
    """
    element.setText(QtGui.QFileDialog.getOpenFileName())


class MTrack2MainWindow(Ui_MainWindow):

    """Main Window for MTrack2 GUI."""

    def setup_window(self, window):
        """Customize the generic UI to our specific case."""
        super(MTrack2MainWindow, self).setupUi(window)
        window.setWindowTitle("MTrack2 statistics")
        self.label.setText("MTrack2 results analyzer")
        txt = "Input TXT File containing MTrack2 results (Ctrl+O)"
        self.le_infile.setPlaceholderText(txt)
        self.cb_option.setText("Write column labels into CSV file.")
        # self.cb_option.setDisabled(True)
        window.addAction(self.sc_ctrl_w)
        window.addAction(self.sc_ctrl_q)
        QtCore.QObject.connect(self.pb_infile, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_infile: select_file(elt))
        QtCore.QObject.connect(self.pb_outfile, QtCore.SIGNAL("clicked()"),
            lambda elt=self.le_outfile: select_file(elt))
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("rejected()"),
            window.close)
        QtCore.QObject.connect(self.bb_ok_cancel, QtCore.SIGNAL("accepted()"),
            self.run_calculations)
        QtCore.QObject.connect(self.sc_ctrl_w, QtCore.SIGNAL("triggered()"),
            window.close)
        QtCore.QObject.connect(self.sc_ctrl_q, QtCore.SIGNAL("triggered()"),
            window.close)
        QtCore.QObject.connect(self.sl_verbosity,
            QtCore.SIGNAL("valueChanged(int)"), self.sb_verbosity.setValue)
        QtCore.QMetaObject.connectSlotsByName(window)

    def preset_fields(self, values):
        """Preset field contents with supplied values."""
        if not values:
            return
        self.le_infile.setText(values[0])
        self.le_outfile.setText(values[1])

    def run_calculations(self):
        """Collect the settings and launch the calculation."""
        infile = str(self.le_infile.text())
        outfile = str(self.le_outfile.text())
        label = False
        if (self.cb_option.checkState() == 2):
            label = True
        verbosity = self.sl_verbosity.value()
        gen_stats(f_in=infile, f_out=outfile, label=label,
            deltas=[1, 5], verbosity=verbosity)
        # TODO: should we exit after the work's done? -> ask user!
        # sys.exit()
        # if we don't exit, reset at least the outfile's name
        self.le_outfile.setText('')


def parse_arguments():
    """Parse commandline arguments for preset values."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-p', '--preset', required=False,
        help='Prefill fields with values in this list.')
    try:
        args = argparser.parse_args()
    except IOError as err:
        argparser.error(str(err))
    if args.preset != None:
        return args.preset.split(',')
    else:
        return None


def main():
    """Set up the GUI window and show it."""
    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()
    gui = MTrack2MainWindow()
    gui.setup_window(main_window)
    gui.preset_fields(parse_arguments())
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
