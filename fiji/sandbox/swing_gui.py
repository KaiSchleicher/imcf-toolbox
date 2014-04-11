from javax.swing import JScrollPane, JPanel, JComboBox, JLabel, JFrame
from java.awt import Color, GridLayout
from java.awt.event import ActionListener


class Listener(ActionListener):
  def __init__(self, label, cb):
    self.label = label
    self.cb = cb
  def actionPerformed(self, event):
    sel = self.cb.getSelectedItem()
    global roimgr
    global roi_ni
    roimgr.select(roi_ni[sel])


roimgr = RoiManager.getInstance()
rois = roimgr.getROIs()
rois_array = roimgr.getRoisAsArray()
roi_ni = {}
roi_in = []
for i in range(roimgr.getCount()):
    name = roimgr.getName(i)
    roi_in.append(name)
    roi_ni[name] = i
print roi_in
print roi_ni


choice_list = ["foo", "bar", "777"]

lbl1 = JLabel("foo label")
lbl2 = JLabel("bar label")

main_panel = JPanel()

### panel 1
panel1 = JPanel()
panel1.add(lbl1)
cb1 = JComboBox(choice_list)
panel1.add(cb1)

### panel 2
panel2 = JPanel()
panel2.add(lbl2)
cb2 = JComboBox(sorted(list(rois.keys())))
cb2.addActionListener(Listener(lbl2, cb2))
panel2.add(cb2)

frame = JFrame("Swing GUI Test Frame")
frame.getContentPane().add(main_panel)
main_panel.add(panel1)
main_panel.add(panel2)
frame.pack()
frame.setVisible(True)
