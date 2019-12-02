import datetime
import os
import shutil
import sys
from os import path

import produce_list_report
from start_up import boot


def date_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]


def copy_css_to_cwd(css_file):
    script_directory = sys.path[0]
    css_path = os.path.join(script_directory, 'resources', css_file)
    shutil.copyfile(css_path, css_file)


def main():
    client, main_board = boot()
    cowley_board = client.get_board('146gQMLj')
    dsm_board = client.get_board('rsKD2538')
    ost_board = client.get_board('9WVxzf50')

    boards = [cowley_board, dsm_board, ost_board, main_board]

    css_file = 'main.css'
    if not path.exists(css_file):
        copy_css_to_cwd(css_file)

    for board in boards:
        email = produce_list_report.produce_email(board)
        with open(board.name + '_' + datetime.date.today().strftime("%Y-%m-%d") + '_email.html', 'w') as f:
            f.write('<head>')
            f.write('<link rel="stylesheet" type="text/css" href="main.css">')
            f.write('</head>')
            f.write(email.print())


main()
