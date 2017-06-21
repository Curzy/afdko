import os
import subprocess
import traceback
import sys

def runShellCmdLogging(cmd):
	try:
		logList = []
		proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		while 1:
			(stdoutdata, stderrdata) = proc.communicate()
			if stdoutdata:
				print stdoutdata,
				logList.append(stdoutdata)
			if stderrdata:
				print stderrdata,
				logList.append(stderrdata)
			if proc.poll() != None:
				if stdoutdata:
					print stdoutdata,
					logList.append(stdoutdata)
				if stderrdata:
					print stderrdata,
					logList.append(stderrdata)
				break
		log = "".join(logList)
	except:
		msg = "Error executing command '%s'. %s" % (cmd, traceback.print_exc())
		print(msg)
		return 1
	return 0

def run_cmd(*args):
	cmdPath = os.path.dirname(__file__)
	cmd = os.path.basename(sys.argv[0])
	if cmd.endswith("FDK"):
		cmd = cmd[:-3]
	cmd = os.path.join(cmdPath, cmd)
	if len(sys.argv) > 1:
		cmd = "%s %s" % (cmd, " ".join(sys.argv[1:]))
	runShellCmdLogging(cmd)