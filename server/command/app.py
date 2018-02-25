from tkinter import Frame, Tk, BOTH, Button, Menu

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title('GUI')
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        _file = Menu(menu)
        _file.add_command(label='Exit', command=self.client_exit)

        menu.add_cascade(label='File', menu=_file)

        edit = Menu(menu)

        edit.add_command(label='Undo')

        menu.add_cascade(label='Edit', menu=edit)

    def client_exit(self):
        exit()


root = Tk()
root.geometry('400x300')

app = Window(root)

if __name__ == '__main__':
    root.mainloop()
