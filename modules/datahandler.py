import csv
from os import rename
from pathlib import Path

class databaseHandler():
	def __init__(self):
		self.row1 = ["DateTime", "Server", "DownSpeed", "UpSpeed", "SpeedPacketLoss", "ShareURL", "AvgPing", "MaxPing", "MinPing", "PingPacketLoss", "Errors"]
		if Path("Data.csv").is_file():
			try:
				with open("Data.csv", "r") as file:
					dataReader = csv.reader(file)
					r1 = next(dataReader)
				if r1 != self.row1:
					raise ValueError("File header is wrong")
			except StopIteration or ValueError:
				self.fileIssue()
		else:
			with open("Data.csv", "w") as file:
				csvWriter = csv.writer(file)
				csvWriter.writerow(self.row1)

	def fileIssue(self):
		while True:
			print("""There seems to be a problem with the database. Choosing an option could result in data loss.
Option (1): Overwrite current file and continue.
Option (2): Backup current file and make a new file.
Option (3): Try to repair current file.
Option (4): Use current file anyway.
(CTRL + C) to exit without changes.""")
			userInput = input(">>> ")
			if userInput == "1":
				with open("Data.csv", "w") as file:
					csvWriter = csv.writer(file)
					csvWriter.writerow(self.row1)
				return
			elif userInput == "2":
				rename("Data.csv", "Data.csv.old")
				with open("Data.csv", "w") as file:
					csvWriter = csv.writer(file)
					csvWriter.writerow(self.row1)
				return
			elif userInput == "3":
				with open("Data.csv", "r+") as file:
					f = file.read()
					file.seek(0)
					file.write(",".join(self.row1) + f[f.find("\n"):-1])
				return
			elif userInput == "4":
				return
			else:
				print("\n" * 100)
				print("Invalid Input, Please try again.")

	def saveData(self, data):
		with open("Data.csv", "a") as file:
			csvWriter = csv.writer(file)
			csvWriter.writerow(data)