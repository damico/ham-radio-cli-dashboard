import curses
import sys
import traceback
import pytz
from datetime import datetime
import maidenhead as mh

from helper import read_json_io
from wu import get_current_observation, print_wu_data


def main(config_path):
    try:

        config = read_json_io(config_path)
        print(config)

        wu_json = get_current_observation(config['wu_api_id'], config['wu_api_key'])

        # -- Initialize --
        stdscr = curses.initscr()  # initialize curses screen
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

        curses.noecho()  # turn off auto echoing of keypress on to screen
        curses.cbreak()  # enter break mode where pressing Enter key
        stdscr.nodelay(1)
        #  after keystroke is not required for it to register
        stdscr.keypad(1)  # enable special Key values such as curses.KEY_LEFT etc

        # -- Perform an action with Screen --
        stdscr.border(0)
        stdscr.addstr(0, 3, ' Ham Radio Dashboard v0.1 ', curses.color_pair(3))
        stdscr.addstr(5, 5, config['callsign'], curses.color_pair(1))
        stdscr.addstr(8, 5, 'LAT/LNG:', curses.A_NORMAL)
        stdscr.addstr(8, 15, str(config['station_geo'][0])+', '+str(config['station_geo'][1]), curses.A_NORMAL)

        iaru_loc = mh.to_maiden(config['station_geo'][0], config['station_geo'][1])
        stdscr.addstr(9, 5, 'IARU Loc:', curses.A_NORMAL)
        stdscr.addstr(9, 15, iaru_loc, curses.A_NORMAL)

        elev = config['elev']
        stdscr.addstr(10, 5, 'Elev.:', curses.A_NORMAL)
        stdscr.addstr(10, 15, str(elev)+' m', curses.A_NORMAL)

        stdscr.addstr(stdscr.getmaxyx()[0] - 2, 2, 'Q - Quit', curses.color_pair(3))

        begin_x = 60;
        begin_y = 4
        height = 16;
        width = 50
        win = curses.newwin(height, width, begin_y, begin_x)

        win.border(0)

        win.box()
        win.addstr(0, 3, " Weather Station: " + str(wu_json['observations'][0]['stationID']) + " ", curses.color_pair(2))
        print_wu_data(win, config['wu_api_id'], config['wu_api_key'])

        seconds = 0
        while True:
            stdscr.refresh()
            win.refresh()
            stdscr.addstr(6, 5, 'UTC: ', curses.A_NORMAL)
            stdscr.addstr(7, 5, 'LOCAL: ', curses.A_NORMAL)
            now = datetime.now()
            local = pytz.timezone("America/Sao_Paulo")
            local_dt = local.localize(now, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)

            utc_date_time = utc_dt.strftime("%m/%d/%Y, %H:%M:%S")
            stdscr.addstr(6, 15, utc_date_time, curses.A_NORMAL)
            local_date_time = local_dt.strftime("%m/%d/%Y, %H:%M:%S")
            stdscr.addstr(7, 15, local_date_time, curses.A_NORMAL)

            # stay in this loop till the user presses 'q'
            ch = stdscr.getch()
            if ch == ord('q') or ch == ord('Q'):
                break
            stdscr.timeout(1000)
            seconds = seconds + 1
            if seconds == (20 * 60):
                seconds = 0
                print_wu_data(win, config['wu_api_id'], config['wu_api_key'])
        # -- End of user code --

    except:
        traceback.print_exc()  # print trace back log of the error

    finally:
        # --- Cleanup on exit ---
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


if __name__ == "__main__":
    main(sys.argv[1])
