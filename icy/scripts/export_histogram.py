from icy.main import Icy
from icy.util import XLSUtil
from plugins.ylemontag.histogram import Histogram

XLS_FILE = '/tmp/icy_py_excel_test.xls'
NUM_BINS = 256

### compatibility for BLOCKS
# if 'input0' is existing, we assume running in a Pythonscript block of a
# protocol and therefore assign the input variables from the block's connectors
# NOTE: we require ALL of them to be connected in this case!
if 'input0' in locals():
    XLS_FILE = input0
    NUM_BINS = input1
    seq = input2
else:
    seq = Icy.getMainInterface().getFocusedSequence()


def get_histogram(seq, nbins, bin_min, bin_max):
    """Generate two lists with central values and histogram counts."""
    print('%s, %s, %s' % (nbins, bin_min, bin_max))
    hist = Histogram.compute(seq, nbins, bin_min, bin_max)
    print("hist.getBinWidth(): %s" % hist.getBinWidth())
    hist_list = [[], []]
    for i in xrange(nbins):
        bin = hist.getBin(i)
        val = bin.getCentralValue()
        count = bin.getCount()
        hist_list[0].append(val)
        hist_list[1].append(count)
    return hist_list


def get_hist_allch(seq, nbins, bin_min, bin_max):
    histograms = [[], []]
    for ci in range(seq.getSizeC()):
        ch = seq.extractChannel(ci)
        temp = get_histogram(ch, NUM_BINS, bin_min, bin_max)
        if histograms[0] == []:
            histograms[0] = temp[0]
        if not histograms[0] == temp[0]:
            return 'ERROR, central bin values in histogram differ!'
        histograms[1].append(temp[1])
    return histograms


def new_xls_row(ws, values):
    """Add a new row from a list of values to a worksheet."""
    global row
    col = 0
    for val in values:
        if type(val) is str or type(val) is unicode:
            XLSUtil.setCellString(ws, col, row, val)
        else:
            XLSUtil.setCellNumber(ws, col, row, val)
        col += 1
    row += 1


print('Sequence name: "%s"' % seq.name)

num_c = seq.getSizeC()
val_min, val_max = seq.getChannelsGlobalBounds()
bwh = (val_max - val_min + 1) / (NUM_BINS * 2)  # bin width half
print('Bin width calculated from min/max and NUM_BINS: %s' % (bwh*2))

wb = XLSUtil.createWorkbook(XLS_FILE)             # create a new excel document
ws = XLSUtil.createNewPage(wb, "Histogram")       # create a new worksheet

# set excel headers
row = 0
new_xls_row(ws, ["File name", seq.name])
row += 1
new_xls_row(ws, ['Number of channels', num_c])
new_xls_row(ws, ['X Dimension', seq.getSizeX()])
new_xls_row(ws, ['Y Dimension', seq.getSizeY()])
new_xls_row(ws, ['Z Dimension', seq.getSizeZ()])
numpixels = seq.getSizeX() * seq.getSizeY() * seq.getSizeZ()
new_xls_row(ws, ['Total number of pixels', numpixels])
print('Total number of pixels: %s' % numpixels)
new_xls_row(ws, ['Global min', val_min])
new_xls_row(ws, ['Global max', val_max])
row += 1
new_xls_row(ws, ['Number of Histogram bins', NUM_BINS])
new_xls_row(ws, ['Bin width', bwh*2])
row += 2

ch_hist = get_hist_allch(seq, NUM_BINS, val_min + bwh, val_max - bwh)
# ch_hist = get_hist_allch(seq, NUM_BINS, 0, 3)

new_xls_row(ws, ['Histogram'])
new_xls_row(ws, ['central bin value', ''] + ch_hist[0] + ['total'])

ci = 0
for ch in ch_hist[1]:
    new_xls_row(ws, ['channel', ci] + ch + [sum(ch)])
    ci += 1

# close and save the excel file
XLSUtil.saveAndClose(wb)

print('Wrote Excel file: "%s"' % XLS_FILE)
### compatibility for BLOCKS
output0 = XLS_FILE
