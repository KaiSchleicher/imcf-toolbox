#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.6.3 on Mon Oct 29 18:32:40 2012

import wx
from wx_filechooser import FileChooser
from closest_neighbours import ClosestNeighbours

# begin wxGlade: extracode
# end wxGlade



class MyBaseFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        self.infile1 = ''
        self.infile1 = ''
        self.outfile1 = ''

        # begin wxGlade: MyBaseFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        label = "File containing reference spots"
        self.label_1 = wx.StaticText(self, -1, label, style=wx.ALIGN_RIGHT)
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "")
        self.button_1 = wx.Button(self, -1, "Select")

        label = "File containing candidate spots"
        self.label_2 = wx.StaticText(self, -1, label, style=wx.ALIGN_RIGHT)
        self.text_ctrl_2 = wx.TextCtrl(self, -1, "")
        self.button_2 = wx.Button(self, -1, "Select")

        label = "File to store results"
        self.label_3 = wx.StaticText(self, -1, label, style=wx.ALIGN_RIGHT)
        self.text_ctrl_3 = wx.TextCtrl(self, -1, "")
        self.button_3 = wx.Button(self, -1, "Select")

        self.button_4 = wx.Button(self, -1, "Go")


        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.hdlr_btn_select_1, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.hdlr_btn_select_2, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.hdlr_btn_select_3, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.hdlr_btn_select_4, self.button_4)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyBaseFrame.__set_properties
        self.SetTitle("Spots Distance Calculator")
        self.text_ctrl_1.SetMinSize((180, 29))
        self.text_ctrl_2.SetMinSize((180, 29))
        # end wxGlade

    def __do_layout(self):
        st_label = wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
        st_txt_ctrl = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL
        st_btn = wx.RIGHT|wx.ALIGN_CENTER_VERTICAL
        st_btn2 = wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL
        # begin wxGlade: MyBaseFrame.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(4, 3, 2, 2)

        grid_sizer_1.Add(self.label_1, 0, st_label, 4)
        grid_sizer_1.Add(self.text_ctrl_1, 0, st_txt_ctrl, 0)
        grid_sizer_1.Add(self.button_1, 0, st_btn, 20)

        grid_sizer_1.Add(self.label_2, 0, st_label, 4)
        grid_sizer_1.Add(self.text_ctrl_2, 0, st_txt_ctrl, 0)
        grid_sizer_1.Add(self.button_2, 0, st_btn, 20)

        grid_sizer_1.Add(self.label_3, 0, st_label, 4)
        grid_sizer_1.Add(self.text_ctrl_3, 0, st_txt_ctrl, 0)
        grid_sizer_1.Add(self.button_3, 0, st_btn, 20)

        grid_sizer_1.Add((20, 0), 0, st_txt_ctrl, 0)
        # grid_sizer_1.Add(self.fbbutton, 0, st_btn2, 10)
        grid_sizer_1.Add(self.button_4, 0, st_btn2, 10)

        self.SetSizer(grid_sizer_1)
        grid_sizer_1.Fit(self)
        grid_sizer_1.AddGrowableCol(1)
        self.Layout()
        # end wxGlade

    def hdlr_btn_select_1(self, event): # wxGlade: MyBaseFrame.<event_handler>
        list_filter = 'Excel XML file (*.xml)|*.xml'
        fcd = FileChooser(wcd=list_filter)
        fname = fcd.get_path()
        if fname:
            self.text_ctrl_1.SetValue(fname)
        event.Skip()

    def hdlr_btn_select_2(self, event): # wxGlade: MyBaseFrame.<event_handler>
        list_filter = 'Excel XML file (*.xml)|*.xml'
        fcd = FileChooser(wcd=list_filter)
        fname = fcd.get_path()
        if fname:
            self.text_ctrl_2.SetValue(fname)
        event.Skip()

    def hdlr_btn_select_3(self, event): # wxGlade: MyBaseFrame.<event_handler>
        list_filter = 'Text file (*.txt)|*.txt'
        fcd = FileChooser(wcd=list_filter)
        fname = fcd.get_path()
        if fname:
            self.text_ctrl_3.SetValue(fname)
        event.Skip()

    def hdlr_btn_select_4(self, event):
        print('files selected:\n%s\n%s\n%s\n' % (self.text_ctrl_1.GetValue(),
            self.text_ctrl_2.GetValue(), self.text_ctrl_3.GetValue()))
        event.Skip()

# end of class MyBaseFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyBaseFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
