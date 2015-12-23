'''
This file is part of the EdTech library project at Full Sail University.

    Foobar is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

    Copyright © 2015 Full Sail University.
'''

import ttk

from Tkinter import *

# http://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
def TkCenter(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

class TkModeless(object):
    """A popup."""
    def __init__(self, root, title, message):
        self.window = Toplevel(root)
        self.window.title(title)
        lbl = ttk.Label(self.window, text = message)
        lbl.update_idletasks()
        lbl.pack()
        TkCenter(self.window)
        self.window.state("normal")
        self.window.update_idletasks()

    def Close(self): self.window.destroy()

# http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-grid-of-widgets-in-tkinter
class FrameWithScrollbar(object):
    """A Frame with attached Scrollbar."""
    def __init__(self, root, width, height):
        self.root = root

        self.canvas = Canvas(self.root, borderwidth = 0, width = width, height = height)
        self.frame = ttk.Frame(self.canvas)

    def AddScrollbar(self):
        vsb = ttk.Scrollbar(self.root, orient = "vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = vsb.set)
        self.frame.pack()
        self.canvas.create_window((0, 0), window = self.frame, anchor = "nw")
        vsb.pack(side = "right", fill = "y")
        self.canvas.pack(side = "left", fill = "both", expand = True)
        self.frame.bind("<Configure>", lambda event, canvas = self.canvas: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
