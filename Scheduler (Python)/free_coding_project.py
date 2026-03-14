from gui import SchedulerGUI
import sys

def main():
    sched = SchedulerGUI(sys.argv[1], sys.argv[2], sys.argv[3])
    sched.run()

if __name__ == "__main__":
    main()
