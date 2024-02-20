import subprocess, os, datetime, signal
from math import ceil

class ping():
	def __init__(self, timeout, IP="1.1.1.1"):
		output = self.start(timeout, IP)

		self.avgPing = output[0]
		self.minPing = output[1]
		self.maxPing = output[2]
		self.packetLoss = output[3]
	
	def start(self, timeout, IP):
		args = ["ping", IP]
		if os.name == "nt": # to end the ping and get stats, will need to stdin ctrl+enter
			args.append("/t")
			return ping.startNT(args, timeout)
		else:
			args.append("-q")
			return ping.startUNIX(args, timeout)
	
	def startNT(args, timeout):
		pingProc = subprocess.run(args=args, timeout=timeout, stdout=subprocess.PIPE)

	def startUNIX(args, timeout):
		with subprocess.Popen(args=args, stdout=subprocess.PIPE) as pingProc:
			try:
				pingProc.communicate(timeout=timeout)
			except subprocess.TimeoutExpired:
				pingProc.send_signal(signal.SIGINT)
				output = pingProc.communicate()[0].decode("utf-8")

		output = output[output.find("---\n")+4:-1].splitlines()

		outputTop = output[0].split(", ")[2]
		packetLoss = outputTop[0:outputTop.find("%")]

		outputBottom = output[1][output[1].find("=")+2:-1].split("/")
		avgPing = round(float(outputBottom[1]))
		minPing = round(float(outputBottom[0]))
		maxPing = round(float(outputBottom[2]))

		return [avgPing, minPing, maxPing, packetLoss]

#TODO (only if windows and unix both can use timeout) could refactor with pingproc being started in start instead of startOS and just passing the object to the startOS, with startOS only parsing output.