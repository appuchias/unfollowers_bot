import wx.adv
import wx
import win10toast
import os
TRAY_TOOLTIP = 'InstaBot'
TRAY_ICON = 'icon.png'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Info', self.get_info)
        menu.AppendSeparator()
        create_menu_item(menu, 'Cerrar', self.exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def get_info(self, event):
        toaster = win10toast.ToastNotifier()
        try:
            with open("files/recents.txt") as r:
                news = r.readlines()[-2:]
                toaster.show_toast("Recent followers:", news[0] if len(news[0]) > 1 else "Ninguno")
                toaster.show_toast("Recent unfollowers:", news[1] if len(news[1]) > 1 else "Ninguno")
        except FileNotFoundError:
            toaster.show_toast("Error!", "Espera a que el archivo sea creado")
        except IndexError:
            toaster.show_toast("Error!", "Error leyendo el archivo")
        os.system("python tray_icon.pyw")

    def on_left_down(self, event):
        self.get_info(event)

    def exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True
        

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
