import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from scheduler import Scheduler
from date_time import current_day

class SchedulerGUI(Scheduler):
    TREE_HEADINGS = ["Date", "Start Time", "End Time", "Action"]
    DAYS_IN_MONTHS = {"January":31, "February":28, "March":31, "April":30, "May":31, "June":30,
    "July":31,"August":31,"September":30,"October":31,"November":30,"December":31}
    MONTHS = ["January", "February","March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]

    @staticmethod
    def update_day_box(month_box, day_box):
        """Called function when new month is selected from a month combo box, edits day box to match selected month"""
        selected_month = month_box.get()
        selected_day = day_box.get()
        if int(selected_day) > SchedulerGUI.DAYS_IN_MONTHS[selected_month]: # if the date selected is a day not present in the month (ie, November 31)
            selected_day = str(SchedulerGUI.DAYS_IN_MONTHS[selected_month])

        day_box.configure(values=[str(i) for i in range(SchedulerGUI.DAYS_IN_MONTHS[selected_month] + 1)[1:]])
        day_box.set(selected_day)

    @staticmethod
    def populate_popup_window(popup_window, first_column=0):
        """adds the elements of a popup window that are needed to input a new schedule or routine item to a popup window.
        The item of first column determines which column the items are placed in; if left as 0 the items will be placed
        on the left of the screen. Returns the following items so that they can be used:
        s_time_hour (the combo box that indicates starting time hour)
        s_time_minute (the combo box that indicates starting time minute)
        e_time_hour (the combo box that indicates ending time hour)
        e_time_minute (the combo box that indicates ending time minute)
        entry (the entry box that indicates the action to be performed)
"""
        # the following elements are created from left to right on the screen
        # labels for categories
        s_time_label = tk.Label(popup_window, text="Start time: ")
        e_time_label = tk.Label(popup_window, text="End time: ")
        action_label = tk.Label(popup_window, text="Action: ")

        # hour buttons, entry widget
        s_time_hour = ttk.Combobox(popup_window, textvariable=tk.StringVar(), state="readonly", width=7,
                                   values=["{:02d}".format(i) for i in range(24)])
        s_time_hour.set("00")
        e_time_hour = ttk.Combobox(popup_window, textvariable=tk.StringVar(), state="readonly", width=7,
                                   values=["{:02d}".format(i) for i in range(24)])
        e_time_hour.set("00")
        entry = tk.Entry(popup_window)

        s_time_label.grid(column=first_column, row=0, sticky="e")  # place the labels
        e_time_label.grid(column=first_column, row=1, sticky="e")
        action_label.grid(column=first_column, row=2, sticky="e")

        s_time_hour.grid(column=first_column+1, row=0, sticky="w")
        e_time_hour.grid(column=first_column+1, row=1, sticky="w")
        entry.grid(column=first_column+1, row=2, columnspan=4)

        # labels for colons
        s_time_colon = tk.Label(popup_window, text=":")
        e_time_colon = tk.Label(popup_window, text=":")

        s_time_colon.grid(column=first_column+2, row=0, sticky="w")
        e_time_colon.grid(column=first_column+2, row=1, sticky="w")

        # minute buttons, entry widget
        s_time_minute = ttk.Combobox(popup_window, textvariable=tk.StringVar(), state="readonly", width=7,
                                     values=["{:02d}".format(i) for i in range(60)])
        s_time_minute.set("00")
        e_time_minute = ttk.Combobox(popup_window, textvariable=tk.StringVar(), state="readonly", width=7,
                                     values=["{:02d}".format(i) for i in range(60)])
        e_time_minute.set("00")

        s_time_minute.grid(column=first_column+3, row=0, sticky="e")
        e_time_minute.grid(column=first_column+3, row=1, sticky="e")

        return s_time_hour, s_time_minute, e_time_hour, e_time_minute, entry

    @staticmethod
    def create_date_buttons(root, display_date="01/01/2025"):
        """creates and returns three combo boxes for a day, month, and year. A frame or root must be passed in for these
        to be placed on, as well as the date these will be initially set to. The day box will change date options
        based on the current date selected."""
        # day combo box
        cur_month = SchedulerGUI.MONTHS[display_date[0] - 1]
        select_day = ttk.Combobox(root, textvariable=tk.StringVar(), state="readonly", width=7,
                                         values=[str(i) for i in range(SchedulerGUI.DAYS_IN_MONTHS[cur_month] + 1)[1:]])
        select_day.set(str(display_date[1]))

        # month combo box
        select_month = ttk.Combobox(root, textvariable=tk.StringVar(), state="readonly", width=10,
                                         values=[m for m in SchedulerGUI.DAYS_IN_MONTHS])
        # bind the update_day_box function to combo box; lamda necessary in order to pass in parameters
        select_month.bind("<<ComboboxSelected>>",
                               lambda event: SchedulerGUI.update_day_box(select_month, select_day))
        select_month.set(cur_month)

        #year combo box
        select_year = ttk.Combobox(root, textvariable=tk.StringVar(), state="readonly", width=7,
                                         values=[str(i + display_date[2]) for i in range(10)])
        select_year.set(str(display_date[2]))
        return select_day, select_month, select_year

    @staticmethod
    def get_combobox_date(select_month, select_day, select_year):
        """returns a list of the month, day, and year as ints. Finds month based on list of months"""
        return [SchedulerGUI.MONTHS.index(select_month.get()) + 1,
                int(select_day.get()), int(select_year.get())]

    def __init__(self, routine_filename, schedule_filename, text_filename):
        super().__init__(routine_filename, schedule_filename)
        # Top right: Text
        # Top left: Buttons to view different days and edit schedule
        # Bottom: treeview (schedule display)

        # create and set up root, values
        self.root = tk.Tk()
        self.root.title("Schedule") # the title of the gui displayed
        self.root.rowconfigure(0, weight=2) # of 7 units of weight, this smaller row is assigned 2
        self.root.rowconfigure(1, weight=5)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.root.resizable(False, False)
        self.display_date = current_day("num")

        # create label in the top right
        text_file = open(text_filename)
        self.label = tk.Label(self.root, text="".join(text_file.readlines()), justify="left")
        text_file.close()

        # creates a treeview with columns as labels,
        self.tree = None
        self.v_scrollbar = None
        self.populate_treeview(self.daily_schedule(self.display_date),
                               "/".join(str(num) for num in self.display_date))

        # creates buttons in top left of screen
        self.select_day, self.select_month, self.select_year = SchedulerGUI.create_date_buttons(self.root, self.display_date)
        self.add_routine_btn = tk.Button(self.root, text="Add routine", command=self.add_routine_window)
        self.add_schedule_btn = tk.Button(self.root, text="Add event", command=self.add_schedule_window)
        self.view_routines_btn = tk.Button(self.root, text="View Routines",
                                           command=lambda:self.populate_treeview(self.routine,"Routines", False))
        self.view_events_btn = tk.Button(self.root, text="View Events",
                                           command=lambda:self.populate_treeview(self.schedule,"All Events", False))
        self.delete_events_btn = tk.Button(self.root, text="Delete event(s)",
                                           command=lambda:self.delete_list_window(self.schedule, True))
        self.delete_routines_btn = tk.Button(self.root, text="Delete routine(s)",
                                           command=lambda:self.delete_list_window(self.routine, False))
        self.view_schedule_btn = tk.Button(self.root, text="View Date:", width=10, # this button's command first sets a new display date and then creates a new treeview using the date combo boxes
                                           command=lambda: (self.change_display_date(SchedulerGUI.get_combobox_date(self.select_month, self.select_day, self.select_year)),
                                                            self.populate_treeview(self.daily_schedule(self.display_date),
                                                                                  "/".join(str(num) for num in self.display_date))))

        # place items
        self.label.grid(row=0, column=1, sticky="nw")
        self.add_routine_btn.grid(row=0, column=0, sticky="nw", padx=5, pady=5, ipadx=30)
        self.add_schedule_btn.grid(row=0, column=0, sticky="ne", ipadx=25, padx=5, pady=5)
        self.view_routines_btn.grid(row=0, column=0, sticky="nw", padx=5, pady=40, ipadx=25)
        self.view_events_btn.grid(row=0, column=0, sticky="ne", padx=5, pady=40, ipadx=21)
        self.delete_events_btn.grid(row=0, column=0, padx=5, sticky="e", pady=55, ipadx=13)
        self.delete_routines_btn.grid(row=0, column=0, padx=5, pady=55, ipadx=18, sticky="w")
        self.view_schedule_btn.grid(row=0, column=0, sticky="s", pady=25)
        self.select_month.grid(row=0, column=0, sticky="sw", padx=5)
        self.select_day.grid(row=0, column=0, sticky="s", padx=25)
        self.select_year.grid(row=0, column=0, sticky="se", padx=25)
        self.root.geometry("1000x500")

    def change_display_date(self, date):
        """changes the default display date"""
        self.display_date = [int(d) for d in date]

    def populate_treeview(self, schedule, date, is_date=True):
        """populates the tree view based on the display date and inputted schedule. The is_date boolean is automatically
        True and creates a 'buffer column' that is blank besides the title of the entire schedule. This should be
        turned to False if making a list that is not a specific date, such as when displaying routines or events"""
        buffer_column = []
        if is_date:
            buffer_column = [""]
        # delete any items in previous tree
        self.tree = ttk.Treeview(self.root, columns=(tuple(x for x in SchedulerGUI.TREE_HEADINGS)))

        # populate the headings
        for heading in SchedulerGUI.TREE_HEADINGS:
            self.tree.heading(heading, text=heading)
            self.tree.column(heading, width=150)
        self.tree.heading("Date", text=date) # the 'date' heading is replaced with the date being displayed
        # populate the items in the schedule

        for item in schedule:
            self.tree.insert(
                "",
                tk.END,
                values=(buffer_column + [x for x in item])
            )

        self.v_scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)
        self.tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.v_scrollbar.grid(row=1, column=1, sticky="nse")

    def create_popup_window(self, title, height="200", width="300"):
        """creates and returns a popup window. Default height and width can be adjusted if desired. """
        popup_window = tk.Toplevel(self.root)
        popup_window.title(title)
        popup_window.geometry(f"{width}x{height}")
        popup_window.resizable(False, False)
        popup_window.transient(self.root) # places pop up on top of the main window
        popup_window.grab_set()
        return popup_window

    def add_routine_window(self):
        """Creates a popup window with combo boxes to select a date and time, entry box to write what the event is,
        as well as tick boxes for each day to select which days of the week things are done on"""
        popup_window = self.create_popup_window("Add Routine")
        s_time_hour, s_time_minute, e_time_hour, e_time_minute, entry = SchedulerGUI.populate_popup_window(popup_window, 1)
        # the following elements are created from left to right on the screen
        # checkboxes for each day
        checkbox_var = [tk.BooleanVar() for i in range(7)] # create seven checkbox_var
        checkboxes = [tk.Checkbutton(popup_window, text=Scheduler.DAYS_IN_WEEK[i], variable=checkbox_var[i]) for i in range(7)]
       # submit button
        add_selected_btn = tk.Button(popup_window, text="Add this routine", width=10,
                                           command=lambda:
                                           self.add_routine_button(f"{s_time_hour.get()}:{s_time_minute.get()}",
                                                                   f"{e_time_hour.get()}:{e_time_minute.get()}",
                                                                   entry.get(),
                                                                   [Scheduler.DAYS_IN_WEEK[i]for i in range(7) if checkbox_var[i].get()],
                                                                   popup_window)) # for each checkbox, checks if it is activated. If it is, adds the day to the list.

        i = 0
        for checkbox in checkboxes: # place the checkboxes
            checkbox.grid(column=0, row=i, sticky="w")
            i+=1
        add_selected_btn.grid(column=1, columnspan=3, row=3, sticky="nsew")
        self.root.wait_window(popup_window) # makes the main screen wait until new screen is destroyed before doing anything

    def add_routine_button(self, s_time, e_time, action, days, popup):
        """Function called when button is clicked on the add routine window. If the start time is before the end time,
        adds it to the routine. Otherwise, causes a warning message to appear"""
        if s_time <= e_time:
            for day in days:
                self.add_routine(day, s_time, e_time, action)
            self.save_routine(self.routine, Scheduler.ROUTINE_TOP_LINE, self.routine_filename)
            self.populate_treeview(self.daily_schedule(self.display_date), "/".join(str(num) for num in self.display_date))
            popup.destroy()
        else: # if the start time is after the end time, the following warning appears:
            messagebox.showwarning("Incorrect Times","Please input a starting time previous to the end time!")

    def add_schedule_button(self, s_time, e_time, action, date, popup):
        """Function called when button is clicked on the add routine window. If the start time is before the end time,
        adds it to the routine. Otherwise, causes a warning message to appear"""
        if s_time <= e_time:
            self.add_schedule(date, s_time, e_time, action)
            self.save_routine(self.schedule, Scheduler.SCHEDULE_TOP_LINE, self.schedule_filename)
            self.populate_treeview(self.daily_schedule(self.display_date), "/".join(str(num) for num in self.display_date))
            popup.destroy()
        else: # if the start time is after the end time, the following warning appears:
            messagebox.showwarning("Incorrect Times","Please input a starting time previous to the end time!")

    def add_schedule_window(self):
        """Creates a popup window with to select a date and time and an entry time to write a new schedule item"""
        popup_window = self.create_popup_window("Add Event","150", "250")
        s_time_hour, s_time_minute, e_time_hour, e_time_minute, entry = SchedulerGUI.populate_popup_window(popup_window)

        day_box, month_box, year_box = SchedulerGUI.create_date_buttons(popup_window, self.display_date)
        add_selected_btn = tk.Button(popup_window, text="Add this event", width=10,
                                           command=lambda:
                                           self.add_schedule_button(f"{s_time_hour.get()}:{s_time_minute.get()}",
                                                                   f"{e_time_hour.get()}:{e_time_minute.get()}",
                                                                   entry.get(),
                                                                    "/".join(str(num) for num in
                                                                             self.get_combobox_date(self.select_month,
                                                                                                    self.select_day,
                                                                                                    self.select_year)),
                                                                    popup_window))

        day_box.grid(column=0, row=3, padx=5, pady=5)
        month_box.grid(column=1, columnspan=2, row=3, sticky="w")
        year_box.grid(column=3, row=3)
        add_selected_btn.grid(column=1, row=4, sticky="nsew", pady=5)
        self.root.wait_window(popup_window) # makes the main screen wait until new screen is destroyed before doing anything

    def delete_list_button(self, lst, check_list, is_schedule, popup):
        """Deletes the items specified in a list. Given the original list, a list of the same size with False values
         where things should be deleted, a specification if this is meant to be the schedule or routine list (Due to
         issues with python passing and copying), and the popup window, which will be deleted."""
        new_list = [lst[i] for i in range(len(lst)) if not check_list[i]]
        if is_schedule:
            self.schedule = new_list
            self.save_routine(self.schedule, Scheduler.SCHEDULE_TOP_LINE, self.schedule_filename)
        else:
            self.routine = new_list
            self.save_routine(self.routine, Scheduler.ROUTINE_TOP_LINE, self.routine_filename)
        self.populate_treeview(self.daily_schedule(self.display_date), "/".join(str(num) for num in self.display_date))
        popup.destroy()

    def delete_list_window(self, lst, is_schedule):
        """Given a list and a specification of whether the deleted list is meant to be the schedule or routine, Creates
        a popup window with a canvas and scrollbar, inside of which is a frame holding checkboxes. Below this is a
        button which will delete each item checked inside the specified list."""
        popup_window = self.create_popup_window("Delete Items", "300", "300")
        canvas = tk.Canvas(popup_window, borderwidth=0) # create a canvas as the overall area
        scrollbar = ttk.Scrollbar(popup_window, orient="vertical", command=canvas.yview) # create scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        frame = tk.Frame(canvas) # create frame to hold checkboxes
        canvas.create_window((0,0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all"))) # if the frame is changed, the scrollbar will also be updated
        checkbox_vars = []
        for item in lst:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(frame, text=", ".join(item), variable=var)
            checkbox.pack(anchor="w")
            checkbox_vars.append(var)

        submit_btn = tk.Button(popup_window, text="Delete Items",
                               command=lambda: self.delete_list_button(lst, [v.get() for v in checkbox_vars], is_schedule,
                                                                       popup_window))

        submit_btn.pack(side="bottom", fill="x")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)



        self.root.wait_window(popup_window) # makes the main screen wait until new screen is destroyed before doing anything

    def run(self):
        self.root.mainloop()
