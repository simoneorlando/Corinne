import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Frame, Entry, Scrollbar, Button, messagebox, Listbox, Radiobutton, PhotoImage


class MyGui(ttk.Frame):
    controller = None
    tabs = None
    _log = None
    _screen_width = None
    _screen_height = None
    COLOR_buttons = '#83778B'
    COLOR_frames = '#333333'
    COLOR_foreground = '#D9C7B3'
    COLOR_log = '#1E1E1E'
    
    def __init__(self, master, controller):
        super().__init__()
        self.controller = controller
        self.initUI(master)
    
    def initUI(self, master):
        self.master.title("Corinne")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.option_add('*foreground', 'black')
        self.master.option_add('*background', 'white')
        
        # Style for ttk widgets
        style = ttk.Style()
        style.configure("TNotebook", background=self.COLOR_frames, borderwidth=1, highlightthickness=1)
        style.configure("TNotebook.Tab", background=self.COLOR_frames, foreground="black",
                             lightcolor=self.COLOR_frames, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", self.COLOR_buttons)],
                       foreground=[("selected", 'black')])
        style.configure("TFrame", background=self.COLOR_frames, foreground="black")
        
        # get screen resolution
        self._screen_width, self._screen_height = master.winfo_screenwidth(), master.winfo_screenheight()
        start_x = int((self._screen_width / 4))
        start_y = int((self._screen_height / 4))
        # fit the guy at screen resolution
        master.geometry('%dx%d+%d+%d' % (self._screen_width / 2, self._screen_height / 2, start_x, start_y))
        
        # create all of the containers
        top_frame = Frame(master)
        top_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        top_frame.configure(bg=self.COLOR_frames)
        top_frame.grid_columnconfigure(0, weight=1)
        
        property_frame = Frame(master)
        property_frame.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        property_frame.configure(bg=self.COLOR_frames)
        property_frame.grid_columnconfigure(0, weight=1)
        property_frame.grid_rowconfigure(0, weight=1)
        
        buttons_frame = Frame(master, padx=10, pady=10)
        buttons_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        buttons_frame.configure(bg=self.COLOR_frames)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        buttons_frame.grid_columnconfigure(3, weight=1)
        buttons_frame.grid_columnconfigure(4, weight=1)
        
        open_icon = PhotoImage(file="icons/open.png")
        open_button = Button(buttons_frame, text=" Open", image=open_icon, compound=tk.LEFT, padx=1,
                             highlightthickness=0,
                             command=self.open_file)
        open_button.configure(borderwidth=0, background=self.COLOR_buttons)
        open_button.image = open_icon
        open_button.grid(row=0, column=0, padx=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        render_icon = PhotoImage(file="icons/render.png")
        render_button = Button(buttons_frame, text=" Render", image=render_icon, compound=tk.LEFT, padx=1,
                               highlightthickness=0,
                               command=self.open_render_view)
        render_button.configure(borderwidth=0, background=self.COLOR_buttons)
        render_button.image = render_icon
        render_button.grid(row=0, column=1, padx=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        prod_icon = PhotoImage(file="icons/product.png")
        prod_button = Button(buttons_frame, text="   Product", image=prod_icon, compound=tk.LEFT, highlightthickness=0,
                             command=self.open_product_view)
        prod_button.configure(borderwidth=0, background=self.COLOR_buttons)
        prod_button.image = prod_icon
        prod_button.grid(row=0, column=2, padx=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        sync_icon = PhotoImage(file="icons/sync.png")
        sync_button = Button(buttons_frame, text="  Sync", image=sync_icon, compound=tk.LEFT, highlightthickness=0,
                             command=self.open_sync_view)
        sync_button.configure(borderwidth=0, background=self.COLOR_buttons)
        sync_button.image = sync_icon
        sync_button.grid(row=0, column=3, padx=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        proj_icon = PhotoImage(file="icons/projection.png")
        proj_button = Button(buttons_frame, text="  Projection", image=proj_icon, compound=tk.LEFT,
                             highlightthickness=0,
                             command=self.open_proj_view)
        proj_button.configure(borderwidth=0, background=self.COLOR_buttons)
        proj_button.image = proj_icon
        proj_button.grid(row=0, column=4, padx=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # create the log box
        self._log = Listbox(top_frame, highlightthickness=0, height=5, background=self.COLOR_log,
                            foreground=self.COLOR_foreground)
        #_scrollb = Scrollbar(top_frame, orient=tk.VERTICAL)
        #self._log.configure(yscrollcommand=_scrollb.set)
        #_scrollb.config(command=self._log.yview)
        self._log.grid(column=0, row=0, padx=10, sticky=(tk.N, tk.S, tk.E, tk.W))
        # _scrollb.grid(column=1, row=0, sticky=tk.S + tk.N)
        
        # create the tab manager for property
        self.tabs = ttk.Notebook(property_frame)
    
    # This is where we launch the file manager bar.
    def open_file(self):
        path = filedialog.askopenfilename(initialdir=".",
                                          filetypes=(("DOT graph", "*.gv *.dot"),
                                                     ("Chorgram grammar", "*.txt"), ("all files", "*.*")),
                                          title="Choose a file."
                                          )
        msg_result = []
        # Check in case user enter an unknown file
        # or closes without choosing a file.
        try:
            path_splitted = os.path.split(path)
            ext = path_splitted[1].split('.')
            # Chorgram file
            if ext[1] == 'txt':
                msg_result = self.__open_chorgram_file(path)
            # DOT files
            elif ext[1] == 'dot' or ext[1] == 'gv':
                msg_result = self.__open_dot_file__(path)
            else:
                self.popupmsg("Unknown extension file")
            # update log box
            self.log(msg_result)
        except:
            pass
    
    def __open_chorgram_file(self, path):
        path_splitted = os.path.split(path)
        # ask where store the converted dot file
        ask_for_path: bool = messagebox.askyesno("Chorgram", "A Chorgram file was inserted\n" +
                                                 "Do you wish to save the converted dot file in " +
                                                 path_splitted[0] + "?\n" +
                                                 "(Click NO to choose a new path)")
        if ask_for_path:  # Yes, use same path
            # (input path, path to store)
            msg_result, graph_name = self.controller.GGparser(path, path_splitted[0])
        else:
            new_folder = filedialog.askdirectory()
            msg_result, graph_name = self.controller.GGparser(path, new_folder)
        self.__add_new_tab__(graph_name)
        return msg_result
    
    def __open_dot_file__(self, path):
        # result[0] domitilla boolean
        # result[1] a message
        # result[2] graph name
        result = self.controller.DOTparser(path)
        msg_result = result[1]
        if result[0]:  # if a domitilla graph was founded
            # ask where store the converted dot file
            path_splitted = os.path.split(path)
            ask_for_path: bool = messagebox.askyesno("Domitilla", "A Domitilla file was inserted\n"
                                                                  "Do you wish to store the converted file in " +
                                                     path_splitted[0] + "?\n"
                                                                        "(Click NO to choose a new path)")
            if ask_for_path:  # Yes, use same path
                msg_result.append(
                    self.controller.DomitillaConverter(result[2], path,
                                                       path_splitted[0]))  # (graph name, input path, path to store)
            else:
                new_folder = filedialog.askdirectory()
                msg_result.append(self.controller.DomitillaConverter(result[2], path, new_folder))
        if len(result) > 2:  # case NO-errors detected
            # add a new tab for the new graph just opened
            self.__add_new_tab__(result[2])
        return msg_result
    
    def open_render_view(self):
        try:
            path = filedialog.askopenfilename(initialdir=".", filetypes=(("DOT graph", "*.gv *.dot"),
                                                                         ("all files", "*.*")), title="Choose a file.")
            path_splitted = os.path.split(path)
            ext = path_splitted[1].split('.')
            # Check in case user enter an unknown file
            # or closes without choosing a file.
            if ext[1] != 'dot' and ext[1] != 'gv':
                self.popupmsg("Wrong extension file inserted!\n"
                              "Please insert a DOT file")
            else:
                # define the frame and its geometry
                r_window = tk.Toplevel(padx=20, pady=20, bg=self.COLOR_frames)
                r_window.wm_title("Render")
                r_window.resizable(False, False)
                self.__set_window_dimension__(r_window)
                label_format = tk.Label(r_window, text="Choose a file format for render:", fg=self.COLOR_foreground,
                                        bg=self.COLOR_frames, wraplength=500)
                label_format.grid(row=0, column=0)
                
                # Initialize file format variable for radiobutton
                option = tk.StringVar()
                # Radiobutton
                rb1 = Radiobutton(r_window, text='png', value="png", var=option, bg=self.COLOR_frames)
                rb2 = Radiobutton(r_window, text='pdf', value="pdf", var=option, bg=self.COLOR_frames)
                rb1.grid(row=1, column=0)
                rb2.grid(row=1, column=1)
                # TODO try except for wrong dot files
                b = Button(r_window, text='Render', bg=self.COLOR_buttons,
                           command=lambda: (self.log(["[RENDER] " + self.controller.render(path, option.get())]),
                                            r_window.destroy()))
                b.grid(row=2, column=1)
        except:
            pass
    
    def open_product_view(self):
        # define the frame and its geometry
        p_window = tk.Toplevel(padx=20, pady=20, bg=self.COLOR_frames)
        p_window.wm_title("Product")
        p_window.resizable(False, False)
        # set window dimension
        self.__set_window_dimension__(p_window)
        
        # label and combo for 1st graph
        lbl1 = tk.Label(p_window, text="Choose 1st Graph", bg=self.COLOR_frames, fg=self.COLOR_foreground)
        lbl1.grid(row=0, column=0, pady=10)
        combo1 = ttk.Combobox(p_window, values=list(self.controller.get_all_ca().keys()))
        combo1.grid(row=0, column=1, pady=10)
        
        # label and combo for 2st graph
        lbl2 = tk.Label(p_window, text="Choose 2st Graph", bg=self.COLOR_frames, fg='white')
        lbl2.grid(row=1, column=0, pady=10)
        combo2 = ttk.Combobox(p_window, values=list(self.controller.get_all_ca().keys()))
        combo2.grid(row=1, column=1, pady=10)
        
        make_button = Button(p_window, text='Make product', bg=self.COLOR_buttons,
                             command=lambda:
                             (self.__exec_product_button__(combo1.get(), combo2.get()),
                              p_window.destroy()))
        make_button.grid(row=2, column=0, pady=10)
    
    def open_sync_view(self):
        s_window = tk.Toplevel(padx=20, pady=20, bg=self.COLOR_frames)
        s_window.wm_title("Synchronisation")
        s_window.resizable(False, False)
        # set window dimension
        self.__set_window_dimension__(s_window)
        
        # label and combo for the graph to synchronize
        lbl1 = tk.Label(s_window, text="Choose Graph", fg='white', bg=self.COLOR_frames)
        lbl1.grid(row=0, column=0, padx=10, pady=10)
        option_v1 = tk.StringVar()
        option_v2 = tk.StringVar()
        combo = ttk.Combobox(s_window, values=list(self.controller.get_all_ca().keys()))
        combo.bind("<<ComboboxSelected>>", lambda event: self.__make_sync_interface_menu__(s_window, list(
            self.controller.get_participants(combo.get())), option_v1, option_v2))
        combo.grid(row=1, column=0, padx=10, pady=10)
        
        sync_button = Button(s_window, text='Synchronize', bg=self.COLOR_buttons,
                             command=lambda: (
                                 self.__exec_sync_button__(combo.get(), option_v1.get(), option_v2.get()),
                                 s_window.destroy()))
        
        sync_button.grid(row=4, column=0)
    
    def open_proj_view(self):
        proj_window = tk.Toplevel(padx=20, pady=20, bg=self.COLOR_frames)
        proj_window.wm_title("Projection")
        proj_window.resizable(False, False)
        
        # set window dimension
        self.__set_window_dimension__(proj_window)
        
        # label and combo for the graph to synchronize
        lbl1 = tk.Label(proj_window, text="Choose Graph", bg=self.COLOR_frames, fg='white')
        lbl1.grid(row=0, column=0, padx=10, pady=10)
        
        option = tk.StringVar()
        combo = ttk.Combobox(proj_window, values=list(self.controller.get_all_ca().keys()))
        combo.bind("<<ComboboxSelected>>", lambda event: self.__make_proj_participant_menu__(proj_window, list(
            self.controller.get_participants(combo.get())), option))
        combo.grid(row=1, column=0, padx=10, pady=10)
        
        proj_button = Button(proj_window, text='Project', bg=self.COLOR_buttons,
                             command=lambda: (
                                 self.__exec_proj_button__(combo.get(), option.get()),
                                 proj_window.destroy()))
        
        proj_button.grid(row=4, column=0)
    
    def __add_new_tab__(self, graph_name):
        self.tabs.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=5)
        frame = ttk.Frame(self.tabs)
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        # Add the tab
        self.tabs.add(frame, text=graph_name)
        # create N.states label and textbox
        label_s = tk.Label(frame, text="N° States", wraplength=500, bg=self.COLOR_frames, fg=self.COLOR_foreground)
        label_s.grid(row=0, column=0, pady=10, padx=10)
        entry_s = Entry(frame, justify=tk.CENTER, width=5, fg='black', highlightthickness=0)
        entry_s.grid(row=0, column=1, sticky=tk.W)
        entry_s.insert(tk.END, str(len(self.controller.get_states(graph_name))))
        # create N.edges label and textbox
        label_e = tk.Label(frame, text="N° Edges", wraplength=500, bg=self.COLOR_frames, fg=self.COLOR_foreground)
        label_e.grid(row=1, column=0, pady=10, padx=10)
        entry_e = Entry(frame, justify=tk.CENTER, width=5, fg='black', highlightthickness=0, )
        entry_e.grid(row=1, column=1, sticky=tk.W)
        entry_e.insert(tk.END, str(len(self.controller.get_edges(graph_name))))
        # create Labels label, textbox and Optionmenu
        label_l = tk.Label(frame, text="N° Labels", wraplength=500, bg=self.COLOR_frames, fg=self.COLOR_foreground)
        label_l.grid(row=3, column=0, pady=10, padx=10)
        entry_l = Entry(frame, justify=tk.CENTER, width=5, fg='black', highlightthickness=0, )
        entry_l.grid(row=3, column=1, sticky=tk.W)
        option_l = tk.StringVar()
        elements_l = list(self.controller.get_labels(graph_name))
        entry_l.insert(tk.END, len(elements_l))
        option_l.set(elements_l[0])
        label_menu = ttk.OptionMenu(frame, option_l, elements_l[0], *elements_l)
        label_menu.grid(row=3, column=2, pady=10, padx=10, sticky=tk.W)
        # create participants label, textbox and Optionmenu
        label_p = tk.Label(frame, text="N° Participants", wraplength=500, bg=self.COLOR_frames, fg=self.COLOR_foreground)
        label_p.grid(row=4, column=0, pady=10, padx=10)
        entry_p = Entry(frame, justify=tk.CENTER, width=5, fg='black', highlightthickness=0, )
        entry_p.grid(row=4, column=1, sticky=tk.W)
        option_p = tk.StringVar()
        elements_p = list(self.controller.get_participants(graph_name))
        entry_p.insert(tk.END, len(elements_p))
        option_p.set(elements_p[0])
        part_menu = ttk.OptionMenu(frame, option_p, elements_p[0], *elements_p)
        part_menu.grid(row=4, column=2, pady=10, padx=10, sticky=tk.W)
        # create Start Node label and textbox
        label_sn = tk.Label(frame, text="Start Node", wraplength=500, bg=self.COLOR_frames, fg=self.COLOR_foreground)
        label_sn.grid(row=5, column=0, pady=10, padx=10)
        entry_sn = Entry(frame, justify=tk.CENTER, width=5, fg='black', highlightthickness=0, )
        entry_sn.grid(row=5, column=1, sticky=tk.W)
        entry_sn.insert(tk.END, str(self.controller.get_start_node(graph_name)))
        # create close button
        close_button = Button(frame, text='X', bg=self.COLOR_frames, highlightthickness=0, borderwidth=0, command=lambda: (
            self.controller.remove_record(self.tabs.tab(self.tabs.select(), "text")),
            # remove the record from opened graphs struct
            self.tabs.forget(self.tabs.select())))  # delete the tab
        close_button.grid(row=0, column=2, sticky=tk.E + tk.N)
        
        # once created, select the tab
        self.tabs.select(frame)
    
    def __exec_sync_button__(self, combo_value, interface1, interface2):
        path_to_store = filedialog.asksaveasfilename(initialdir=".", title="Save as",
                                                     filetypes=("DOT graph", "*.gv *.dot"))
        result = self.controller.synchronize(combo_value, interface1, interface2, path_to_store)
        # print the log message
        self.log(result[0])
        # create a new tab for the product graph
        self.__add_new_tab__(result[1])
    
    def __exec_product_button__(self, combo_value1, combo_value2):
        path_to_store = filedialog.asksaveasfilename(initialdir=".", title="Save as",
                                                     filetypes=("DOT graph", "*.gv *.dot"))
        result = self.controller.make_product(combo_value1, combo_value2, path_to_store)
        # print the log message
        self.log(result[0])
        # create a new tab for the product graph
        self.__add_new_tab__(result[1])
    
    def __exec_proj_button__(self, combo_value, participant):
        path_to_store = filedialog.asksaveasfilename(initialdir=".", title="Save as",
                                                     filetypes=("DOT graph", "*.gv *.dot"))
        result = self.controller.projection(combo_value, participant, path_to_store)
        # print the log message
        self.log(result)
    
    def __make_sync_interface_menu__(self, frame, elements, option_v1, option_v2):
        # label and optionMenu for the 1st interface
        option_v1.set(elements[0])
        lbl2 = tk.Label(frame, text="Select 1st participant", bg=self.COLOR_frames, fg=self.COLOR_foreground)
        lbl2.grid(row=2, column=0, padx=10, pady=10)
        op_menu_1 = ttk.OptionMenu(frame, option_v1, elements[0], *elements)
        op_menu_1.grid(row=2, column=1, padx=10, pady=10)
        
        # label and optionMenu for the 2st interface
        option_v2.set(elements[0])
        lbl3 = tk.Label(frame, text='Select 2st participant', bg=self.COLOR_frames, fg=self.COLOR_foreground)
        lbl3.grid(row=3, column=0, pady=10)
        op_menu_2 = ttk.OptionMenu(frame, option_v2, elements[0], *elements)
        op_menu_2.grid(row=3, column=1, padx=10, pady=10)
        
        # update window dimension
        self.__set_window_dimension__(frame)
    
    def __make_proj_participant_menu__(self, frame, elements, option):
        option.set(elements[0])
        lbl = tk.Label(frame, text='Select participant to project', bg=self.COLOR_frames, fg=self.COLOR_foreground)
        lbl.grid(row=2, column=0, padx=10, pady=10)
        op_menu = ttk.OptionMenu(frame, option, elements[0], *elements)
        op_menu.grid(row=2, column=1, padx=10, pady=10)
        self.__set_window_dimension__(frame)
    
    def __set_window_dimension__(self, frame):
        # set window dimension
        width, height = frame.winfo_reqwidth(), frame.winfo_reqheight()
        frame.geometry('+%d+%d' % (self._screen_width / 2 - width / 2, self._screen_height / 2 - height / 2))
        
    def log(self, msg):
        # Write a message in the log box
        for line in msg:
            self._log.insert(tk.END, line)
        self._log.see(tk.END)
    
    def popupmsg(self, msg):
        popup = tk.Toplevel(padx=20, pady=20)
        popup.wm_title("!")
        popup.resizable(False, False)
        
        screen_width, screen_height = popup.winfo_screenwidth(), popup.winfo_screenheight()
        width, height = popup.winfo_reqwidth(), popup.winfo_reqheight()
        
        popup.geometry('+%d+%d' % (screen_width / 2 - width / 2, screen_height / 2 - height / 2))
        
        max_size = popup.winfo_screenwidth() / 3
        label = tk.Label(popup, text=msg, wraplength=max_size)
        label.grid(row=0, column=0)
        
        b = ttk.Button(popup, text="Okay", command=popup.destroy)
        b.grid(row=1, column=0)
