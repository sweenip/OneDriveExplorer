import re
import io
from collections import namedtuple, OrderedDict
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

ASCII_BYTE = rb" !\"#\$%&\'\(\)\*\+,-\./0123456789:;<=>\?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^_`abcdefghijklmnopqrstuvwxyz\{\|\}\\\~\t"
String = namedtuple("String", ["s", "offset"])
uuid4hex = re.compile(b'{[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}}', re.I)


def unicode_strings(buf, n=4):
    reg = rb"((?:[%s]\x00){%d,})" % (ASCII_BYTE, n)
    uni_re = re.compile(reg)
    match = uni_re.search(buf)
    return match.group().decode("utf-16")


def folder_search(dict_list, input, duuid):
    for k, v in dict_list.items():
        if(isinstance(v, list)):
            for dic in v:
                if duuid in dic['Object_UUID']:
                    dic['Children'].append(input)
                else:
                    folder_search(dic, input, duuid)


dir_list = []
folder_structure = OrderedDict()


def main():
    def parent_child(d, parent_id=None):
        if parent_id is None:
            # This line is only for the first call of the function
            parent_id = tv.insert("", "end", text=d['Name'], values=(d['Folder_UUID'], d['Object_UUID'], d['Name'], d['Type'], len(d['Children'])))

        for c in d['Children']:
            # Here we create a new row object in the TreeView and pass its return value for recursion
            # The return value will be used as the argument for the first parameter of this same line of code after recursion
            parent_child(c, tv.insert(parent_id, "end", text=c['Name'], values=(c['Folder_UUID'], c['Object_UUID'], c['Name'], c['Type'], len(c['Children']))))

    def selectItem(a):
        curItem = tv.focus()
#        print(tv.item(curItem))
        values = tv.item(curItem, 'values')
        details.config(state='normal')
        details.delete('1.0', tk.END)
        line = f'Name: {values[2]}\nType: {values[3]}\nFolder_UUID: {values[0]}\nObject_UUID: {values[1]}'
        if values[3] == 'Folder':
            line += f'\n\n# Children: {values[4]}'
        details.insert(tk.END, line)
        details.see(tk.END)
        details.config(state='disable')

    import sys

    with open(sys.argv[1], 'rb') as f:
        b = f.read()

    for match in re.finditer(uuid4hex, b):
        data = io.BytesIO(b)
        s = match.start()
        diroffset = s - 40
        data.seek(diroffset)
        duuid = data.read(32).decode("utf-8")
        if duuid not in dir_list:
            dir_list.append(duuid)

    folder_structure = {'Folder_UUID': '',
                        'Object_UUID': dir_list[0],
                        'Type': 'Folder',
                        'Name': 'Root',
                        'Children': []
                        }

    for match in re.finditer(uuid4hex, b):
        data = io.BytesIO(b)
        s = match.start()
        diroffset = s - 40
        objoffset = s - 79
        data.seek(diroffset)
        duuid = data.read(32).decode("utf-8")
        data.seek(objoffset)
        ouuid = data.read(32).decode("utf-8")
        name = unicode_strings(data.read())
        if ouuid in dir_list:
            input = {'Folder_UUID': duuid,
                     'Object_UUID': ouuid,
                     'Type': 'Folder',
                     'Name': name,
                     'Children': []
                     }
            if duuid in folder_structure['Object_UUID']:
                folder_structure['Children'].append(input)
            else:
                folder_search(folder_structure, input, duuid)
        else:
            input = {'Folder_UUID': duuid,
                     'Object_UUID': ouuid,
                     'Type': 'File',
                     'Name': name,
                     'Children': []
                     }
            if duuid in folder_structure['Object_UUID']:
                folder_structure['Children'].append(input)
            else:
                folder_search(folder_structure, input, duuid)

    root = ThemedTk()
    root.title('OneDriveExplorer')
    root.iconbitmap('Images/OneDrive.ico')

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    tool_menu = tk.Menu(menubar, tearoff=0)
    submenu = tk.Menu(tool_menu, tearoff=0)

    for theme_name in sorted(root.get_themes()):
        submenu.add_command(label=theme_name,
                            command=lambda t=theme_name: [submenu.entryconfig(submenu.index(ttk.Style().theme_use()), background=''),
                                                          root.set_theme(t),
                                                          submenu.entryconfig(submenu.index(ttk.Style().theme_use()), background='grey')])

    tool_menu.add_cascade(label="Skins",
                          menu=submenu)
    menubar.add_cascade(label="Tools",
                        menu=tool_menu)

    outer_frame = ttk.Frame(root)
    main_frame = ttk.Frame(outer_frame,
                           relief='groove',
                           padding=5)

    outer_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    outer_frame.grid_rowconfigure(0, weight=1)
    outer_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    pw = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)

    tv_frame = ttk.Frame(main_frame)
    tv = ttk.Treeview(tv_frame, show='tree', selectmode='browse')
    scrollb = ttk.Scrollbar(tv_frame, orient="vertical", command=tv.yview)
    tabControl = ttk.Notebook(main_frame)
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='Details')
    sg = ttk.Sizegrip(main_frame)

    details = tk.Text(tab1, undo=False, width=50, state='disable')
    tv.configure(yscrollcommand=scrollb.set)

    tabControl.grid_rowconfigure(0, weight=1)
    tabControl.grid_columnconfigure(0, weight=1)
    tab1.grid_rowconfigure(0, weight=1)
    tab1.grid_columnconfigure(0, weight=1)

    tv_frame.grid_rowconfigure(0, weight=1)
    tv_frame.grid_columnconfigure(0, weight=1)

    parent_child(folder_structure)

    pw.add(tv_frame)
    pw.add(tabControl)

    tv.grid(row=0, column=0, sticky="nsew")
    scrollb.grid(row=0, column=1, sticky="nsew")
    sg.grid(row=1, columnspan=3, sticky='se')
    details.grid(row=0, column=0, sticky="nsew")
    pw.grid(row=0, column=0, sticky="nsew")

    tv.bind('<<TreeviewSelect>>', selectItem)

    root.mainloop()


if __name__ == '__main__':
    main()