# -------------------------------------------------------------------
# MOONS Compiler for Tiny
#
# Filip Moons - Student Master in de Toegepaste Computerwetenschappen
# augustus 2014
#
# This source file contains:
# - The definitions of a GUI to give the user an intuitive user
# experience while compiling code. The GUI has options to open a 
# source file, to save a source file, to compile a source file and
# to save the resulting assembly code. Through the GUI, the user has
# a complete overview of the compile process: the syntax tree, the
# three address code and the final assembly code can easily be accessed.
#
# The GUI was generated by wxGlade. The GUI runs through the wxPython-
# module.
# -------------------------------------------------------------------


#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Tue Aug 26 18:20:55 2014
#

import wx

# begin wxGlade: dependencies
import gettext

# end wxGlade

# begin wxGlade: extracode
# end wxGlade

#Import compiler element
from lex import *
from yacc import *
import frontend as frontend
import backend as backend
import frontend_optimalizations as optimalization

data = '''int main() {\nwrite 5 + 5;\nwrite 25*25; \n}'''
file_open = False
path = ""

class HoofdScherm(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: HoofdScherm.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
 

        # Tool Bar
        self.hoofdscherm_toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.TB_TEXT)
        self.SetToolBar(self.hoofdscherm_toolbar)
        self.hoofdscherm_toolbar.AddLabelTool(498, _("Open sourcefile.."), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.hoofdscherm_toolbar.AddSeparator()
        self.hoofdscherm_toolbar.AddLabelTool(499, _("Save source"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.hoofdscherm_toolbar.AddSeparator()
        self.hoofdscherm_toolbar.AddLabelTool(500, _("Compile"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.hoofdscherm_toolbar.AddSeparator()
        self.hoofdscherm_toolbar.AddLabelTool(501, _("Save assembly"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")

        # Tool Bar end
        self.SourceCode = wx.TextCtrl(self, wx.ID_ANY, data, style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.TE_RICH)
        self.notebook_2 = wx.Notebook(self, wx.ID_ANY, style=0)
        self.notebook_2_pane_1 = wx.Panel(self.notebook_2, wx.ID_ANY)
        self.SyntaxTree = wx.TextCtrl(self.notebook_2_pane_1, wx.ID_ANY, _(""), style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.TE_READONLY)
        self.notebook_2_pane_2 = wx.Panel(self.notebook_2, wx.ID_ANY)
        self.TaC = wx.TextCtrl(self.notebook_2_pane_2, wx.ID_ANY, _(""), style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.TE_READONLY)
        self.notebook_2_pane_3 = wx.Panel(self.notebook_2, wx.ID_ANY)
        self.Assembly = wx.TextCtrl(self.notebook_2_pane_3, wx.ID_ANY, _(""), style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TOOL, self.sourcefile, id=498)
        self.Bind(wx.EVT_TOOL, self.savefile, id=499)
        self.Bind(wx.EVT_TOOL, self.compile, id=500)
        self.Bind(wx.EVT_TOOL, self.save_assembly, id=501)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: HoofdScherm.__set_properties
        self.SetTitle(_("Tiny Compiler by Filip Moons (VUB, 2014)"))
        self.SetSize((1007, 664))
        self.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Lucida Grande"))
        self.hoofdscherm_toolbar.Realize()
        self.SourceCode.SetMinSize((480, 600))
        self.SourceCode.SetFont(wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Courier"))
        self.SyntaxTree.SetMinSize((490, 570))
        self.SyntaxTree.SetFont(wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Courier"))
        self.TaC.SetMinSize((490, 570))
        self.TaC.SetFont(wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Courier"))
        self.Assembly.SetMinSize((490, 570))
        self.Assembly.SetFont(wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Courier"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: HoofdScherm.__do_layout
        grid_sizer_1 = wx.GridSizer(1, 2, 9, 0)
        sizer_1_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1.Add(self.SourceCode, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_1.Add(self.SyntaxTree, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.notebook_2_pane_1.SetSizer(sizer_1)
        sizer_1_copy.Add(self.TaC, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.notebook_2_pane_2.SetSizer(sizer_1_copy)
        sizer_1_copy_1.Add(self.Assembly, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.notebook_2_pane_3.SetSizer(sizer_1_copy_1)
        self.notebook_2.AddPage(self.notebook_2_pane_1, _("Syntax Tree"))
        self.notebook_2.AddPage(self.notebook_2_pane_2, _("Three Address Code"))
        self.notebook_2.AddPage(self.notebook_2_pane_3, _("Assembly Code"))
        grid_sizer_1.Add(self.notebook_2, 1, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade


    def compile(self, event):  # wxGlade: HoofdScherm.<event_handler>
        try:
            data = hoofdscherm.SourceCode.GetValue()
            # Give the lexer some input
            lexer.input(data)

            # Tokenize
            print("Output Lexer")
            print("============")
            print("")
            while True:
                tok = lexer.token()
                if not tok: break      # No more input
                print tok

            #Build parse tree
            tree = yacc.parse(data, 0)
            print("")
            print("Syntax tree")
            print("===========")
            print("")
            print tree
            hoofdscherm.SyntaxTree.SetValue(str(tree))
            #Traverse tree for TAC-generation
            code, symboltable = frontend.generateTAC(tree)
            print("")
            print("Tree address code")
            print("=================")
            print("")
            print frontend.show_TAC(code)
            #Constant folding optimalization
            code, symboltable = optimalization.constant_folding(code, symboltable)
            print("")
            print("Constant folding optimalization")
            print("===============================")
            print("")
            print frontend.show_TAC(code)
            #Dead code elimination
            code, symboltable = optimalization.dead_code_elimination(code, symboltable)
            print("")
            print("Dead code elimination")
            print("=====================")
            print("")
            print frontend.show_TAC(code)
            hoofdscherm.TaC.SetValue(frontend.show_TAC(code))
            #Generate assembly code
            print("")
            print("Assembly code")
            print("=============")
            print("")
            assembly = backend.generateAssembly(code,symboltable)
            print backend.show_assembly(assembly)
            hoofdscherm.Assembly.SetValue(backend.show_assembly(assembly))
        except:
            dlg = wx.MessageDialog(self, "There seems to be an error. Please check your code. You can find some useful information in the error logs in the terminal. Good luck, Filip.", "Error", wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy
                        
       


    def sourcefile(self, event):  # wxGlade: HoofdScherm.<event_handler>
        global file_open
        global path
        openFileDialog = wx.FileDialog(self, "Open sourcefile", "", "","Source files (*)|*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        input_stream = open(openFileDialog.GetPath(),'r')
        path = openFileDialog.GetPath()
        file_open = True
        hoofdscherm.SourceCode.SetValue(input_stream.read())
        return

    def savefile(self, event):
        global file_open
        global path
        if not file_open:
            saveFileDialog = wx.FileDialog(self, "Save source to file", "", "","Source files (*)|*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if saveFileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed idea...
            path = saveFileDialog.GetPath()
        file = open(path, "w")
        file.write(hoofdscherm.SourceCode.GetValue())
        file.close()


    def save_assembly(self, event):
        global file_open
        global path
        saveFileDialog = wx.FileDialog(self, "Save assembly to file", "", "","Assembly files (*.s)|*.s", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        path = saveFileDialog.GetPath()+".s"
        file = open(path, "w")
        file.write(hoofdscherm.Assembly.GetValue())
        file.close()
    
        
       
        
        

# end of class HoofdScherm
if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    hoofdscherm = HoofdScherm(None, wx.ID_ANY, "")
    app.SetTopWindow(hoofdscherm)
    hoofdscherm.Show()
    app.MainLoop()
