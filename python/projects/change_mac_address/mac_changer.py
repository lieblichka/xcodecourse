#!/usr/bin/env python

import subprocess # подключение модуля subprocess

subprocess.call("ifconfig wlp3s0 down", shell=True)
subprocess.call("ifconfig wlp3s0 hw ether 50:b7:c3:e1:ba:a5",
				 shell=True)
subprocess.call("ifconfig wlp3s0 up", shell=True)

