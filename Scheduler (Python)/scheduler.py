from calendar import Calendar
from date_time import current_day, weekday


class Scheduler:
    ROUTINE_TOP_LINE = ["Day", "Start Time", "End Time", "Action\n"]
    SCHEDULE_TOP_LINE = ["Date", "Start Time", "End Time", "Action\n"]
    DAYS = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6,
                      "Sunday": 7, }
    DAYS_IN_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    D_INDEX = {"Day": 0, "S_Time": 1, "E_Time": 2, "Act": 3}

    @staticmethod
    def compare_routines(rout1, rout2):
        """Given two lists of routines, returns true if the first is sooner and false otherwise"""
        s_index = Scheduler.D_INDEX
        if Scheduler.DAYS[rout1[s_index["Day"]]] < Scheduler.DAYS[rout2[s_index["Day"]]]: # if the first item's day is before the second item's day
            return True
        elif Scheduler.DAYS[rout1[s_index["Day"]]] == Scheduler.DAYS[rout2[s_index["Day"]]]: # if the both events are on the same day
            if rout1[s_index["S_Time"]] < rout2[s_index["S_Time"]]:  # compare the times
                return True
        return False

    @staticmethod
    def compare_schedules(sched1, sched2):
        """Given two lists of schedules, returns true if the first is sooner and false otherwise"""
        s_index = Scheduler.D_INDEX
        sched1_dates = sched1[0].split("/")
        sched2_dates = sched2[0].split("/")
        if sched1_dates[2] < sched2_dates[2]: # if the first item's year is before the second item's year
            return True
        elif sched1_dates[2] > sched2_dates[2]:
            return False
        elif sched1_dates[0] < sched2_dates[0]: # if the first item's month is before the second item's month
            return True
        elif sched1_dates[0] > sched2_dates[0]:
            return False
        elif sched1_dates[1] < sched2_dates[1]: # if the first item's day is before the second item's day
            return True
        elif sched1_dates[1] == sched2_dates[1]: # if the both events are on the same day
            if sched1[s_index["S_Time"]] < sched2[s_index["S_Time"]]:  # compare the times
                return True
        return False

    @staticmethod
    def merge_lists(sched1, sched2, comparison):
        """Given two lists of schedules, returns one sorted version """
        new_list = []
        while len(sched1) > 0 and len(sched2) > 0:
            if comparison(sched1[0], sched2[0]):
                new_list.append(sched1.pop(0))
            else:
                new_list.append(sched2.pop(0))
        new_list = new_list + sched1 + sched2  # append the leftover part of the list
        return new_list

    @staticmethod
    def sort_lists(schedule, comparison):
        if len(schedule) <= 1:  # the base case (allows for a length of 0
            return schedule
        list1 = schedule[0:len(schedule) // 2]  # first half of the list
        list2 = schedule[len(schedule) // 2:]  # second half of the list
        return Scheduler.merge_lists(Scheduler.sort_lists(list1, comparison), Scheduler.sort_lists(list2, comparison), comparison)

    def __init__(self, routine_filename, schedule_filename):
        """Routine File should be a .csv in the format of the provided 'routine.csv'"""
        rout_file = open(routine_filename, "r")
        sched_file = open(schedule_filename, "r")
        self.routine_filename = routine_filename
        self.schedule_filename = schedule_filename
        self.schedule = [x.split(",") for x in sched_file.readlines()[1:]]
        self.routine = [x.split(",") for x in rout_file.readlines()[1:]]
        self.routine = Scheduler.sort_lists(self.routine, Scheduler.compare_routines)
        self.schedule = Scheduler.sort_lists(self.schedule, Scheduler.compare_schedules)
        self.calendar = Calendar()
        rout_file.close()

    def __str__(self):
        # Routine:
        # Monday
        #   6:30-7:30: Do something
        def add_to_list(lst):
            cur_day = ""
            append = ""
            for item in lst:
                if item[Scheduler.D_INDEX["Day"]] != cur_day:
                    cur_day = item[Scheduler.D_INDEX["Day"]]
                    append += f"{cur_day}\n"
                append += f"\t{item[Scheduler.D_INDEX["S_Time"]]}-{item[Scheduler.D_INDEX["E_Time"]]}: {item[Scheduler.D_INDEX["Act"]].strip()}\n"
            return append

        string = f"Schedule:\n"
        string += add_to_list(self.schedule)
        string += f"Routine:\n"
        string += add_to_list(self.routine)
        return string

    def __repr__(self):
        return f"Scheduler(Routine: {self.routine}, Schedule:{self.schedule})"

    def daily_schedule(self, date=current_day("num")):
        """returns a sorted list of each item in a schedule for a given date"""
        final_schedule = [item[1:] for item in self.schedule if item[0] == f"{date[0]}/{date[1]}/{date[2]}"] # a list of each item in the schedule that is the given date
        final_schedule += [item[1:] for item in self.routine if item[0] == weekday(date[0], date[1], date[2])] # a list of each item in the routine that is the weekday of the given date
        return Scheduler.sort_lists(final_schedule, lambda sched1, sched2: sched1[0] < sched2[0]) # sorts the list based on the function which compares start times\

    def remove_event(self, event):
        """given an event or routine, removes that event or routine from the list. Returns nothing"""
        if event in self.routine:
            self.routine.remove(event)
        elif event in self.schedule:
            self.schedule.remove(event)

    def add_routine(self, day, s_time, e_time, action):
        """given a day, start time, end time, and action (all as strings), adds a new routine. Returns nothing"""
        new_event = [day, s_time, e_time, action]
        self.routine = Scheduler.merge_lists(self.routine, [new_event], Scheduler.compare_routines)

    def add_schedule(self, date, s_time, e_time, action):
        """given a date, start time, end time, and action, adds a new event to the schedule. Returns nothing"""
        new_event = [date, s_time, e_time, action]
        self.schedule = Scheduler.merge_lists(self.schedule, [new_event], Scheduler.compare_schedules)

    def save_routine(self, schedule_list=None, top_line=None, filename=None):
        """saves the current schedule to a file. If no parameters are given, defaults to saving the schedule. Returns nothing"""
        if schedule_list is None:
            schedule_list = self.schedule
        if top_line is None:
            top_line = Scheduler.SCHEDULE_TOP_LINE
        if filename is None:
            filename = self.schedule_filename
        with open(filename, "w") as f:
            f.write(",".join(top_line))
            for event in schedule_list:
                event[3] = event[3].strip() + "\n"
                f.write(",".join(event))
