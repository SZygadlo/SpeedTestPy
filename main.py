from modules.datahandler import databaseHandler
from modules.pingpy import ping
from modules.speedtestpy import speedtestCLI

import datetime
from math import ceil


class SpeedTest():
	def __init__(self):
		####################
		self.Interval = [1, 0, 0] #Hours Minutes Seconds, the total of all the time is how long inbetween speedtests
		self.Server = None
		#################### TODO make better interface, maybe config file that stores it which can be updated on startup.

		self.dataH = databaseHandler()

		self.main()

	def main(self):
		while True:
			print("It is currently safe to exit the script. (CTRL + C)")
			data = ["", "", "", "", "", "", "", "", "", ""]
			p = ping(timeout=self.nextInterval())
			data[5:8] = str(p.avgPing), str(p.maxPing), str(p.minPing), str(p.packetLoss) + "%"

			print("Starting Speed Test")
			st = speedtestCLI(self.Server)
			print(st.exitCode)
			if st.exitCode == 0:
				data[1:5] = str(st.serverName), str(round(int(st.downloadSpeed) / 125000, 2)), str(round(int(st.uploadSpeed) / 125000, 2)), str(st.packetLoss) + "%", str(st.shareUrl)
			else:
				data[10] = str(st.error)

			data[0] = datetime.datetime.now()
			print("\n" * 100)
			self.dataH.saveData(data)

	def nextInterval(self):
		delta = datetime.timedelta(hours=self.Interval[0], minutes=self.Interval[1], seconds=self.Interval[2])
		now = datetime.datetime.now()
		outDatetime = datetime.datetime.min + ceil((now - datetime.datetime.min) / delta) * delta
		return int(outDatetime.timestamp() - now.timestamp())

SpeedTest()