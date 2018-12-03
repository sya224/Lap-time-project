from tkinter import *
import time
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
data = dict()

def convert(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return str(str(int(h))+':'+str(int(m))+':'+str(s))
class Initialize(Tk): #tintializes all the teams at the start and then calls Main
	def __init__(self):
		Tk.__init__(self)
		self.title('Team Entry')
		Label(self, text = 'Enter all team names seperated by ; ex. a;b;c', font = ('Arial', 20)).grid(row = 0, column = 0)
		self.entry = Entry(self)
		self.entry.grid(row = 0, column = 1)
		Button(self, text = 'Enter', command = self.on_button, font = ('Arial', 20)).grid(row = 1, column = 0)
	def on_button(self): #updates teamNames and calls Main
		global data
		for team in self.entry.get().split(';'):
			data[team] = []
		self.destroy() 
		cMain = Main()  
		cMain.mainloop() 

class Main(Tk): #main class
	def __init__(self): #the init class sets up and prints all the data, sets up buttons
		Tk.__init__(self)
		self.title('Race Timer')
		Button(self, text = 'Semi-Auto', command = self.on_semiAuto, font = ('Arial', 20)).grid(row = 0, column = 0)
		Button(self, text = 'Graph', command = self.on_graph, font = ('Arial', 20)).grid(row = 0, column = 1)
		Label(self, text = 'Lap', font = ('Arial', 20)).grid(row = 1, column = 0)
		global data
		for i in range(1, max([len(data[team]) for team in data])+1):
			Label(self, text = i, font = ('Arial', 20)).grid(row = i+1, column = 0)
		i = 1
		for team in data:
			self.grid_columnconfigure(i, minsize = 150)
			Label(self, text = team, font = ('Arial', 20)).grid(row = 1, column = i)
			j = 2
			for lap in data[team]:
				Label(self, text = convert(lap), font = ('Arial', 20)).grid(row = j, column = i)
				j += 1
			i += 1
		Button(self, text = 'Add Team', command = self.on_addTeam, font = ('Arial', 20)).grid(row = 1, column = len(data)+1)
		Button(self, text = 'Edit', command = self.on_edit, font = ('Arial', 20)).grid(row = 1, column = len(data)+2)
		Button(self, text = 'Save', command = self.on_save, font = ('Arial', 20)).grid(row = 1, column = len(data)+3)
		Button(self, text = 'Leaderboard', command = self.on_leaderboard, font = ('Arial', 20)).grid(row = 1, column = len(data)+4)
	def on_semiAuto(self): #this is called when the semi auto button is pressed
		self.destroy()
		cSemiAuto = SemiAuto()
		cSemiAuto.mainloop()
	def on_graph(self): #this is called when the graph button is pressed
		cGetGraph = GetGraph()
		cGetGraph.mainloop()
	def on_addTeam(self): #this is called when add team button is pressed
		self.destroy() 
		cAddTeam = AddTeam() 
		cAddTeam.mainloop()
	def on_edit(self): #this is called when add team button is pressed
		self.destroy() 
		cEdit = Edit()
		cEdit.mainloop()
	def on_save(self):
		self.destroy()
		cSave = Save()
		cSave.mainloop()
	def on_leaderboard(self):
		cLeaderboard = Leaderboard()
		cLeaderboard.mainloop()

class SemiAuto(Tk):
	def __init__(self):
		Tk.__init__(self)
		global data
		times = dict()
		i = 0
		for name in data:
			self.grid_columnconfigure(i, minsize = 100)
			Label(self, text = name, font = ('Arial', 20)).grid(row = i, column = 0)
			Button(self, text = 'Start', command = lambda name = name, times = times: self.on_start(name, times), font = ('Arial', 20)).grid(row = i, column = 1)
			Button(self, text = 'Lap', command = lambda name = name, times = times: self.on_lap(name, times), font = ('Arial', 20)).grid(row = i, column = 2)
			Button(self, text = 'Stop', command = lambda name = name, times = times: self.on_stop(name, times), font = ('Arial', 20)).grid(row = i, column = 3)
			i += 1
		self.cMain = Main()
	def on_start(self, name, times):
		times[name] = time.time()
	def on_lap(self, name, times):
		data[name].append(round(time.time() - times[name], 2))
		times[name] = time.time()
		self.cMain.destroy()
		self.cMain = Main()
		self.cMain.mainloop()
	def on_stop(self, name, times):
		data[name].append(round(time.time() - times[name], 2))
		self.cMain.destroy()
		self.cMain = Main()
		self.cMain.mainloop()

class GetGraph(Tk): #tintializes all the teams at the start and then calls Main
	def __init__(self):
		Tk.__init__(self)
		self.title('Graph Team Entry')
		Label(self, text = 'Enter all team names to graph seperated by ; ex. a;b;c', font = ('Arial', 20)).grid(row = 0, column = 0)
		self.entry = Entry(self)
		self.entry.grid(row = 0, column = 1)
		Button(self, text = 'Enter', command = self.on_button, font = ('Arial', 20)).grid(row = 1, column = 0)
	def on_button(self): #updates teamNames and calls Main
		toGraph = dict()
		for team in self.entry.get().split(';'):
			toGraph[team] = data[team]
		self.destroy()
		cDispGraph = DispGraph(graph = toGraph)
		cDispGraph.mainloop()

class DispGraph(Tk):
	def __init__(self, graph):
		Tk.__init__(self)
		self.title('Graph Display')
		f = Figure(figsize = (5,5), dpi = 100)
		a = f.add_subplot(111)
		x = list(range(1, max([len(data[team]) for team in data])+1))
		for team in graph:
			a.plot(x, graph[team], label = team)
		a.legend()
		a.xaxis.set_major_locator(MaxNLocator(integer=True))
		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH)
		canvas._tkcanvas.pack(side = TOP, fill = BOTH)


class AddTeam(Tk):
	def __init__(self): #asks for team and all of the laps completed by it
		Tk.__init__(self)
		self.title('Team Add')
		Label(self, text = 'Enter team', font = ('Arial', 20)).grid(row = 0, column = 0)
		self.entry1 = Entry(self)
		self.entry1.grid(row = 0, column = 1)
		Button(self, text = 'Enter', command = self.on_button, font = ('Arial', 20)).grid(row = 1, column = 0)
	def on_button(self): #updates global variables and returns, calls new instance of Main
		global data
		name = self.entry1.get()
		data[name] = []
		self.destroy()
		cMain = Main()
		cMain.mainloop()

class Edit(Tk):
	def __init__(self): #Asks for team name and lap number
		Tk.__init__(self)
		self.title('Edit')
		Label(self, text = 'Enter team name', font = ('Arial', 20)).grid(row = 0, column = 0)
		self.entry1 = Entry(self)
		self.entry1.grid(row = 0, column = 1)
		Label(self, text = 'Enter lap number', font = ('Arial', 20)).grid(row = 1, column = 0)
		self.entry2 = Entry(self)
		self.entry2.grid(row = 1, column = 1)
		self.entry3 = Entry(self)
		self.entry3.grid(row = 2, column = 0)
		Label(self, text = 'Minutes', font = ('Arial', 20)).grid(row = 2, column = 1)
		self.entry4 = Entry(self)
		self.entry4.grid(row = 2, column = 2)
		Label(self, text = 'Seconds', font = ('Arial', 20)).grid(row = 2, column = 3)
		Button(self, text = 'Enter', command = self.on_button, font = ('Arial', 20)).grid(row = 3, column = 0)
	def on_button(self): #updates and calles new instance of Main
		data[self.entry1.get()][int(self.entry2.get())-1] = int(self.entry3.get())*60 + int(self.entry4.get())
		self.destroy()
		cMain = Main()
		cMain.mainloop()

class Save(Tk):
	def __init__(self): #Asks for team name and lap number
		Tk.__init__(self)
		self.title('Save')
		Label(self, text = 'Save as (Enter file name)', font = ('Arial', 20)).grid(row = 0, column = 0)
		self.entry = Entry(self)
		self.entry.grid(row = 0, column = 1)
		Button(self, text = 'Enter', command = self.on_button, font = ('Arial', 20)).grid(row = 1, column = 0)
	def on_button(self):
		with open(self.entry.get() + ".csv", 'w+') as fout: #  This will save the file as user input file name as excel file that we write to it.
			fout_writer = csv.writer(fout, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL) # This will separate the data with comma so it is easy to get data from the file 
			for team in data:
				fout.write(str('Team: '+str(team)+'\n')) # This will write the team name as in order of team's element that user input at first. 
				#fout.write(str('Laps: '+str(convert(data[team]))+'\n')) for debugging 
				#fout.write(str('Laps: '+str(data)+'\n')) # for debugging 
				fout.write(str('Laps: ' +str(data[team])+'\n')) # This will save the data that are shown in the table with correspoding team name as Lap : [lap time +]
		self.destroy()

class Leaderboard(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title('Leaderboard')
		global data
		sortedData = sorted(data.items(), key = lambda laps: len(laps[1]), reverse = True)
		Label(self, text = 'Team Name', font = ('Arial', 20)).grid(row = 0, column = 0)
		Label(self, text = '# Laps Completed', font = ('Arial', 20)).grid(row = 0, column = 1)
		Label(self, text = 'Fastest Lap', font = ('Arial', 20)).grid(row = 0, column = 2)
		Button(self, text = 'Update', command = self.on_update, font = ('Arial', 20)).grid(row = 0, column = 3)
		i = 1
		for team in sortedData:
			self.grid_columnconfigure(i, minsize = 250)
			Label(self, text = team[0], font = ('Arial', 20)).grid(row = i, column = 0)
			Label(self, text = str(len(team[1])), font = ('Arial', 20)).grid(row = i, column = 1)
			Label(self, text = convert(min(team[1])), font = ('Arial', 20)).grid(row = i, column = 2)
			i += 1
	def on_update(self):
		self.destroy()
		cLeaderboard = Leaderboard()
		cLeaderboard.mainloop()

cInitialize = Initialize()
cInitialize.mainloop()