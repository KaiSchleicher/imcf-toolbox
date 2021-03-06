#!/usr/bin/python

"""Handle XML files generated by Bitplane Imaris."""

# TODO: do sanity checking
# TODO: evaluate datatypes from XML cells

import xml.etree.ElementTree as etree
import numpy as np
from log import log
from misc import filename
import volpy as vp


class ImarisXML(object):

    """
    An XML parser to handle Excel-style XML files generated by Imaris.

    Example
    -------
    >>> fh = open('../../sample_data/nuclei_cv/imaris_spots.xml', 'r')
    >>> xmldata = ImarisXML(fh)
    >>> if xmldata._worksheet('Position') is not None:
    ...     True
    True
    >>> if xmldata._worksheet('NonExistingWorksheet') is None:
    ...     True
    True
    """

    def __init__(self, xmlfile, namespace=''):
        """Create a new Imaris-XML object from a file.

        Parameters
        ----------
        xmlfile : file or str
            A filehandle or string for the XML file to parse.
        namespace : string, optional
            A string denoting the namespace expected in the XML file,
            defaults to the one used by MS Excel in its XML format.
        """
        self.tree = None
        self.cells = {}
        # by default, we expect the namespace of Excel XML:
        self.namespace = 'urn:schemas-microsoft-com:office:spreadsheet'
        if namespace:
            self.namespace = namespace
        log.info("Parsing XML file: %s" % filename(xmlfile))
        self.tree = etree.parse(xmlfile)
        log.info("Done parsing XML: %s" % self.tree)
        self._check_namespace()

    def _check_namespace(self):
        """Check if an XML tree has a certain namespace.

        Take an XML etree object and a string denoting the expected namespace,
        check if the namespace of the XML tree matches. Return the namespace if
        yes, raise a TypeError otherwise.
        """
        real_ns = self.tree.getroot().tag[1:].split("}")[0]
        if not real_ns == self.namespace:
            log.critical("ERROR, couldn't find the expected XML namespace!")
            log.critical("Namespace parsed from XML: '%s'" % real_ns)
            raise TypeError

    def _worksheet(self, ws_name):
        """Look up a certain worksheet in the Excel XML tree.

        Parameters
        ----------
        ws_name : string
            The name of the desired worksheet.

        Returns
        -------
        worksheet : etree element
            The XML subtree pointing to the desired worksheet.
        """
        pattern = ".//{%s}Worksheet[@{%s}Name='%s']" % \
            (self.namespace, self.namespace, ws_name)
        # we ignore broken files that contain multiple worksheets having
        # identical names and just return the first one (blame the creator for
        # such stupid files):
        try:
            worksheet = self.tree.findall(pattern)[0]
        except IndexError:
            return None
        log.info("Found worksheet: %s" % worksheet)
        return worksheet

    def _parse_cells(self, ws_name):
        """Parse the cell-contents of a worksheet into a 2D array.

        After parsing the contents, they are added to the global map 'cells'
        using the worksheet name as the key.

        Parameters
        ----------
        ws_name : string
            The name of the worksheet to process.
        """
        rows = self._worksheet(ws_name).findall('.//{%s}Row' % self.namespace)
        cells = []
        for row in rows:
            content = []
            # check if this is a header row:
            style_att = '{%s}StyleID' % self.namespace
            if style_att in row.attrib:
                # we don't process the header row, so skip it
                continue
            for cell in row:
                content.append(cell[0].text)
            log.debug('length of row: %i' % len(row))
            log.debug(content)
            cells.append(content)
        self.cells[ws_name] = cells
        log.debug("--- cells ---\n%s\n--- cells ---" % self.cells)
        log.info("Parsed rows: %i" % len(self.cells))

    def celldata(self, ws_name):
        """Provide access to the cell contents.

        Automatically calls the parser if the selected worksheet
        has not yet been processed before.

        Parameters
        ----------
        ws_name : string
            The name of the desired worksheet.

        Returns
        -------
        out : [[]], rows x cols
            List of lists containing the table cell's data, e.g.
            [ [r1c1, r1c2, r1c3, ...],
              [r2c1, r2c2, r2c3, ...],
              [r3c1, r3c2, r3c3, ...],
              ...                      ]
        """
        if not ws_name in self.cells:
            self._parse_cells(ws_name)
        return(self.cells[ws_name])

    def coordinates(self, ws_name):
        """Extract coordinates and ID's from a list of worksheet-cells.

        Parameters
        ----------
        ws_name : string
            The name of the worksheet to process.

        Returns
        -------
        out : np.ndarray
            A numpy ndarray of shape (N,3) containing 3-tuples (floats) using
            the ID as index, representing the coordinates in (x, y, z) order.
        """
        coords = []
        # make sure the cells were already parsed:
        if not ws_name in self.cells:
            self._parse_cells(ws_name)
        # extract positions and ID:
        for cell in self.cells[ws_name]:
            idx = int(cell[7])
            x = float(cell[0])
            y = float(cell[1])
            z = float(cell[2])
            coords.insert(idx, (x, y, z))
        log.debug("Parsed coordinates: %i" % len(coords))
        return np.array(coords)

    def coordinates_2d(self, ws_name):
        """A wrapper to retrieve a view on the 2D coordinates only."""
        return self.coordinates(ws_name)[:, 0:2]


class StatisticsSpots(vp.Points3D):

    """Class representing "spots" objects exported from the statistics tab."""

    def __init__(self, infile):
        """Load spots positions from a statistics XML export."""
        super(StatisticsSpots, self).__init__(infile)

    def __load_data__(self, infile):
        """Override the loading by using the XML importer."""
        xmldata = ImarisXML(infile)
        self.data = xmldata.coordinates('Position')
        del xmldata
        log.info('Created %i spots from XML export.\n%s' %
                 (len(self.data), str(self.data)))

if __name__ == "__main__":
    print('Running doctest on file "%s".' % __file__)
    import doctest
    doctest.testmod()
