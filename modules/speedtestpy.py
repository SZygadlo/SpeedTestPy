import subprocess, os
from pathlib import Path
class speedtestCLI():
	def __init__(self, server=None, path=None):
		self.exitCode = None
		output = self.speedtest(server, path)

		self.output = output
		self.exitCode = output[0]

		if output[0] == 0:
			self.serverName = output[1]
			self.serverId = output[2]
			self.idleLatency = output[3]
			self.idleJitter = output[4]
			self.packetLoss = output[5]
			self.downloadSpeed = output[6]
			self.uploadSpeed = output[7]
			self.downloadBytes = output[8]
			self.uploadBytes = output[9]
			self.shareUrl = output[10]
			self.downloadServerCount = output[11]
			self.downloadLatency = output[12]
			self.downloadLatencyJitte = output[13]
			self.downloadLatencyLow = output[14]
			self.downloadLatencyHigh = output[15]
			self.uploadLatency = output[16]
			self.uploadLatencyJitter = output[17]
			self.uploadLatencyLow = output[18]
			self.uploadLatencyHigh = output[19]
			self.idleLatencyLow = output[20]
			self.idleLatencyHigh = output[21]
			self.error = None
		else:
			self.error = output[1]
				
	def speedtest(self, server, path):
		args = []

		if path == None:
			if os.name == "nt":
				args.append(".\speedtest.exe")
			else:
				args.append("./speedtest")

		else:
			try:
				path = Path(path)
				if path.is_file():
					path = str(path)
					args.append(path)
				else:
					return "Invalid Speedtest Path"
			except:
				return "Invalid Speedtest Path"
		if server != None:
			args.append("-s")
			args.append(str(server))

		args.append("-f")
		args.append("csv")

		speedProc = subprocess.run(args=args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		if speedProc.stderr == "":
			output = speedProc.stdout.split("\",\"")
			output[0] = output[0].replace("\"", "")
			output[-1] = output[-1].replace("\"\n", "")
			output.insert(0, 0)
		else:
			output = [1]
			output.append(", ".join(speedProc.stderr.splitlines()))
		return output