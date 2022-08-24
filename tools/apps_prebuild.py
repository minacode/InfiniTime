import math
import re


ALL_APPS = {
    'Alarm': {
        'symbol': 'Symbols::clock',
        'cpp': 'Alarm.cpp',
        'h': 'Alarm.h'
    },
    'HeartRate': {
        'symbol': 'Symbols::heartBeat',
        'cpp': 'HeartRate.cpp',
        'h': 'HeartRate.h',
    },
    'Metronome': {
        'symbol': 'Symbols::drum',
        'cpp': 'Metronome.cpp',
        'h': 'Metronome.h',
    },
    'Motion': {
        'symbol': 'Symbols::chartLine',
        'cpp': 'Motion.cpp',
        'h': 'Motion.h',
    },
    'Music': {
        'symbol': 'Symbols::music',
        'cpp': 'Music.cpp',
        'h': 'Music.h',
    },
    'Navigation': {
        'symbol': 'Symbols::map',
        'cpp': 'Navigation.cpp',
        'h': 'Navigation.h',
    },
    'Paddle': {
        'symbol': 'Symbols::paddle',
        'cpp': 'Paddle.cpp',
        'h': 'Paddle.h',
    },
    'Paint': {
        'symbol': 'Symbols::paintbrush',
        'cpp': 'InfiniPaint.cpp',
        'h': 'InfiniPaint.h',
    },
    'Steps': {
        'symbol': 'Symbols::shoe',
        'cpp': 'Steps.cpp',
        'h': 'Steps.h',
    },
    'StopWatch': {
        'symbol': 'Symbols::stopWatch',
        'cpp': 'StopWatch.cpp',
        'h': 'StopWatch.h',
    },
    'Timer': {
        'symbol': 'Symbols::hourGlass',
        'cpp': 'Timer.cpp',
        'h': 'Timer.h',
    },
    'Twos': {
        'symbol': '"2"',
        'cpp': 'Twos.cpp',
        'h': 'Twos.h',
    },
}


def get_apps():
    with open('apps.txt', 'r') as file:
        apps = file.readlines()
    
    apps = [app.strip() for app in apps]
    apps.append('Alarm')
    apps.append('Timer')
    return apps


def generate_application_list(apps):
	lines = []
	for app in apps:
		if app in ALL_APPS:
		    # 10 spaces for correct indentation
		    # '{' and '}' separate because format strings interfere with them
		    # Symbols::symbol, Apps::app in the middle
		    # \n at the end for correct format
		    lines.append(' '*10 + '{' + f'{ALL_APPS[app]["symbol"]}, Apps::{app}'  + '},\n')

	# \n at start
	# 8 space for correct indentation of closing braces
	lines = '\n' + ''.join(lines) + ' '*8

	print(lines)

	# 6 apps per screen, result rounded up
	n_screens = math.ceil(len(apps) / 6)
	print(f'Created {n_screens} screens.')

	with open('src/displayapp/screens/ApplicationList.h.template', 'r') as template:
		content = template.read()

	content = re.sub(r'@N_SCREENS@', str(n_screens), content)
	content = re.sub('\s*@APPS@\s*', lines, content)

	with open('src/displayapp/screens/ApplicationList.h', 'w') as out:
		out.write(content)


def generate_cmake_list(apps):
	lines = []
	for app in apps:
		if app in ALL_APPS:
		    lines.append(' '*8 + f'displayapp/screens/{ALL_APPS[app]["cpp"]}\n')

	lines = '\n' + ''.join(lines) + '\n' + ' '*8

	print(lines)

	with open('src/CMakeLists.txt.template', 'r') as template:
		content = template.read()

	content = re.sub(r'\s*@APPS@\s*', lines, content)

	with open('src/CMakeLists.txt', 'w') as out:
		out.write(content)


def generate_display_app(apps):
    include_lines = []
    define_lines = []
    for app in apps:
        if app in ALL_APPS:
            include_lines.append(f'#include "displayapp/screens/{ALL_APPS[app]["h"]}"\n')
            define_lines.append(f'#define APP_{app.upper()}\n')

    include_lines = '\n' + ''.join(include_lines) + '\n'
    define_lines = '\n' + ''.join(define_lines) + '\n\n'

    with open('src/displayapp/DisplayApp.cpp.template', 'r') as template:
        content = template.read()

    content = re.sub(r'\s*@APP_INCLUDES@\s*', include_lines, content)
    content = re.sub(r'\s*@APP_DEFINES@\s*', define_lines, content)

    with open('src/displayapp/DisplayApp.cpp', 'w') as out:
        out.write(content)


def generate_apps(apps):
    lines = []
    for app in apps:
        if app in ALL_APPS:
            lines.append(' '*6 + f'{app},\n')

    lines = '\n' + ''.join(lines)

    with open('src/displayapp/Apps.h.template', 'r') as template:
        content = template.read()

    content = re.sub(r'\s*@APPS@\s*', lines, content)

    with open('src/displayapp/Apps.h', 'w') as out:
        out.write(content)


def main():
    apps = get_apps()
    print('Apps:')
    print(apps)
    generate_application_list(apps)
    generate_cmake_list(apps)
    generate_display_app(apps)
    generate_apps(apps)
    print('Done.')
	

if __name__ == '__main__':
	main()
