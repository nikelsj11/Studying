import sys
import subprocess

DB_NAME = 'morph-dicts'
DB_COLLECTION = 'speakrus'


def get_line_count(file_name):
    return int(subprocess.check_output('wc -l %s' % file_name, shell=True).strip().split()[0])


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))