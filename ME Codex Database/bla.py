import wx
import audiere
import urllib
import pygame
import pickle
import os.path
from icons import MECDico, Updateico
from clusters import clusters, clusterentries
from species import Tree, codexentries, codexentries2, secondarylist, bluelist, drelllist, me2audiolist, me1audiolist
from codeximages import codeximages
from codex import codex
from updateCheck import Updater
from webbrowser import open as openSite 

if os.path.isfile('settings.pkl') == True:
	settings2 = pickle.load(open('settings.pkl'))
else:
	settingsdict = {
	'background': '#8E9DBC',
	'music': 'True',
	'audio': 'True'
				}
	pickle.dump(settingsdict, open('settings.pkl', 'wb'))
	settings2 = pickle.load(open('settings.pkl'))

indextouse = None
class MainWindow(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, 'Mass Effect Codex Database', size=(500, 627), style= wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

		self.panel = wx.Panel(self, -1)

		self.SetIcon(MECDico.GetIcon())

#This is the Menu Bar at the top of the program.
		menubar = wx.MenuBar()
		help = wx.Menu()
		help.Append(101, '&Update', 'Update')
		help.Append(102, '&About', 'About')
		settings = wx.Menu()
		theme = wx.Menu()
		music = wx.Menu()
		audio = wx.Menu()
		theme.Append(321, '&ME1 Style', 'ME1 Style')
		theme.Append(322, '&ME2 Style', 'ME2 Style')
		music.Append(323, '&Music On', 'Turn Music On')
		music.Append(324, '&Music Off', 'Turn Music Off')
		audio.Append(325, '&Codex Audio On', 'Turn Codex Audio On')
		audio.Append(326, '&Codex Audio Off', 'Turn  Codex Audio Off')
		settings.AppendMenu(221, 'Theme', theme)
		settings.AppendMenu(222, 'Music', music)
		settings.AppendMenu(223, 'Codex Audio', audio)
		menubar.Append(help, '&Help')
		menubar.Append(settings, '&Settings')
		self.SetMenuBar(menubar)

#These are the bindings for the events in the menu bar.
		self.Bind(wx.EVT_MENU, lambda e: Updater(self, 1.1, 'http://coderslair.net/Python%20Programs/ME%20Codex%20Database/Version/version.txt', 'http://coderslair.net/Python%20Programs/ME%20Codex%20Database/ME%20Codex%20Database.7z'))
		self.Bind(wx.EVT_MENU, self.aboutevt, id=102)
		self.Bind(wx.EVT_MENU, self.ME1Theme, id=321)
		self.Bind(wx.EVT_MENU, self.ME2Theme, id=322)
		self.Bind(wx.EVT_MENU, self.musicon, id=323)
		self.Bind(wx.EVT_MENU, self.musicoff, id=324)
		self.Bind(wx.EVT_MENU, self.audioon, id=325)
		self.Bind(wx.EVT_MENU, self.audiooff, id=326)

#These are the sizers for the program.
		mainbox = wx.BoxSizer(wx.HORIZONTAL)
		topbox = wx.BoxSizer(wx.HORIZONTAL)
		leftbox = wx.BoxSizer(wx.HORIZONTAL)
		rightbox = wx.BoxSizer(wx.VERTICAL)

#The second top panel is where the pictures are displayed.
		self.toppanel2 = wx.Panel(self.panel, -1, size=(239, 157), pos=(252, 0))
		mainbox.Add(self.toppanel2, 1, wx.DEFAULT, 0)
		image = wx.StaticBitmap(self.toppanel2, -1, codeximages['Logo'].GetBitmap())

#The left panel has the hierarchy with the codex list.
		leftpanel = wx.Panel(self.panel, -1, size=(250, 580), pos=(0, 0), style= wx.BORDER_SUNKEN)
		leftpanel.SetSizer(leftbox)
		self.tree = wx.TreeCtrl(leftpanel, 1, wx.DefaultPosition, (249, 579), wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS | wx.TR_SINGLE | wx.TR_LINES_AT_ROOT | wx.TR_NO_LINES | wx.TR_FULL_ROW_HIGHLIGHT)
		pccodex = self.tree.AddRoot('Codex')
		self.tree.SetBackgroundColour(settings2['background'])

#This is the bindings for the parts of the hierarchy that contain everything but the planets.
		for codex in sorted(Tree.keys()):
			curCodex = self.tree.AppendItem(pccodex, codex)
			for species in sorted(Tree[codex].keys()):
				curSpecies = self.tree.AppendItem(curCodex, species)
				for data in sorted(Tree[codex][species]):
					curData = self.tree.AppendItem(curSpecies, data)

#The Planets and Locations loop.  Clusters are the first under Planet's and Locations, then systems, then planets.
		pandl = self.tree.AppendItem(pccodex, 'Planets and Locations')
#This is the bindings for the parts of the hierarchy that contain only the planets.
		for cluster in sorted(clusters.keys()):
			curCluster = self.tree.AppendItem(pandl, cluster)
			for system in sorted(clusters[cluster].keys()):
				curSystem = self.tree.AppendItem(curCluster, system)
				for planet in sorted(clusters[cluster][system]):
					self.tree.AppendItem(curSystem, planet)

#This binds the above two bindings for the tree.
		self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)

#This is the right panel that displays the text.
		self.rightpanel = wx.Panel(self.panel, -1, size=(242, 420), pos=(250, 158), style= wx.BORDER_SUNKEN)
		mainbox.Add(self.rightpanel, 2, wx.DEFAULT, 0)
		self.rightpanel.SetSizer(rightbox)
		self.codextext = wx.TextCtrl(self.rightpanel, -1, size=(240, 420), style=wx.TE_READONLY | wx.TE_MULTILINE)
		rightbox.Add(self.codextext, 0, wx.DEFAULT, 1)

#Events for everything in the program are below.
	def aboutevt(self, event):
		credits = wx.AboutDialogInfo()
		credits.SetIcon(MECDico.GetIcon())
		credits.SetName('ME Codex Database')
		credits.AddDeveloper('Trevor Hampton')
		credits.AddDocWriter('Trevor Hampton')
		credits.SetVersion('V 1.1')
		credits.SetCopyright('(C) 2010 Trevor Hampton\n\nMass Effect, Mass Effect 2, \nThe audio, images and data are \nCopyright of Bioware \n\n Special Thanks to omgGarrus for beta testing \n And to Bioware for making such incredible games \n\n If you find any bugs or have an idea \n For something that could be improved \n Email me at trhprogrambugs@gmail.com' )
		wx.AboutBox(credits)
#Events for the settings menu are below.
	def ME1Theme(self, event):
		self.tree.SetBackgroundColour('#8E9DBC')
		settings2['background'] = '#8E9DBC'
		pickle.dump(settings2, open('settings.pkl', 'wb'))
	def ME2Theme(self, event):
		self.tree.SetBackgroundColour('#BE5320')
		settings2['background'] = '#BE5320'
		pickle.dump(settings2, open('settings.pkl', 'wb'))
	def musicon(self, event):
		gmusic.play()
		settings2['music'] = 'True'
		pickle.dump(settings2, open('settings.pkl', 'wb'))
		pygame.mixer.init(24000)
	def musicoff(self, event):
		gmusic.stop()
		settings2['music'] = 'False'
		pickle.dump(settings2, open('settings.pkl', 'wb'))
	def audioon(self, event):
		settings2['audio'] = 'True'
		pickle.dump(settings2, open('settings.pkl', 'wb'))
		pygame.mixer.init(24000)
	def audiooff(self, event):
		settings2['audio'] = 'False'
		pickle.dump(settings2, open('settings.pkl', 'wb'))
		if pygame.mixer.music.get_busy() == True:
			pygame.mixer.music.stop()
			pygame.mixer.quit()
#This is the main event of the program.  This event is the one that defines what happens when a tree item is selected.  It places the text, images and audio that plays when an item is selected.
	def OnSelChanged(self, event):
		curItem = event.GetItem()
		curIndex = self.tree.GetItemText(curItem)
		global indextouse
		if self.tree.GetItemText(curItem) in codexentries:
			self.codextext.Clear()
			if indextouse != 'Logo':
				indextouse = 'Logo'
				image = wx.StaticBitmap(self.toppanel2, -1, codeximages[indextouse].GetBitmap())
				self.toppanel2.Refresh()
		elif self.tree.GetItemText(curItem) in codexentries2:
			self.codextext.Clear()
			if indextouse != 'Logo':
				indextouse = 'Logo'
				image = wx.StaticBitmap(self.toppanel2, -1, codeximages[indextouse].GetBitmap())
				self.toppanel2.Refresh()
		elif self.tree.GetItemText(curItem) in clusterentries:
			self.codextext.Clear()
			if indextouse != 'Logo':
				indextouse = 'Logo'
				image = wx.StaticBitmap(self.toppanel2, -1, codeximages[indextouse].GetBitmap())
				self.toppanel2.Refresh()
		elif self.tree.GetItemText(curItem) in secondarylist:
			self.codextext.Clear()
			indextouse = 'secondary'
			image = wx.StaticBitmap(self.toppanel2, -1, codeximages[indextouse].GetBitmap())
			self.toppanel2.Refresh()
			self.codextext.SetValue(codex[curIndex])
			if curIndex in me2audiolist:
				if settings2['audio'] == 'True':
					pygame.mixer.quit()
					pygame.mixer.init(24000)
					pygame.mixer.music.load('Codex Audio/' +curIndex+ '.ogg')
					pygame.mixer.music.play(0, 0)
					pygame.mixer.music.set_volume(.85)
			elif curIndex in me1audiolist:
				if settings2['audio'] == 'True':
					pygame.mixer.quit()
					pygame.mixer.init(44000)
					pygame.mixer.music.load('Codex Audio/' +curIndex+ '.ogg')
					pygame.mixer.music.play(0, 0)
		elif self.tree.GetItemText(curItem) in bluelist:
			self.codextext.Clear()
			indextouse = 'Blue Suns'
			image = wx.StaticBitmap(self.toppanel2, -1, codeximages[indextouse].GetBitmap())
			self.toppanel2.Refresh()
			self.codextext.SetValue(codex[curIndex])
			if curIndex in me2audiolist:
				if settings2['audio'] == 'True':
					pygame.mixer.quit()
					pygame.mixer.init(24000)
					pygame.mixer.music.load('Codex Audio/' +curIndex+ '.ogg')
					pygame.mixer.music.play(0, 0)
					pygame.mixer.music.set_volume(.85)
			elif curIndex in me1audiolist:
				if settings2['audio'] == 'True':
					pygame.mixer.quit()
					pygame.mixer.init(44000)
					pygame.mixer.music.load('Codex Audio/' +curIndex+ '.ogg')
					pygame.mixer.music.play(0, 0)
		elif self.tree.GetItemText(curItem) in drelllist:
			self.codextext.Clear()
			indextouse = 'Drell'
			image = wx.StaticBitmap(self.toppanel2, -1, codeximages[indextouse].GetBitmap())
			self.toppanel2.Refresh()
			self.codextext.SetValue(codex[curIndex])
			if curIndex in me2audiolist:
				if settings2['audio'] == 'True':
					pygame.mixer.quit()
					pygame.mixer.init(24000)
					pygame.mixer.music.load('Codex Audio/' +curIndex+ '.ogg')
					pygame.mixer.music.play(0, 0)
					pygame.mixer.music.set_volume(.85)
			elif curIndex in me1audiolist:
				if settings2['audio'] == 'True':
					pygame.mixer.quit()
					pygame.mixer.init(44000)
					pygame.mixer.music.load('Codex Audio/' +curIndex+ '.ogg')
					pygame.mixer.music.play(0, 0)
		else:
			self.codextext.Clear()
			indextouse = self.tree.GetItemText(curItem)
			image = wx.StaticBitmap(self.toppanel2, -1, codeximages[indextouse].GetBitmap())
			self.toppanel2.Refresh()
			self.codextext.SetValue(codex[indextouse])
			if indextouse in me2audiolist:
				if settings2['audio'] == 'True':
					pygame.mixer.quit()
					pygame.mixer.init(24000)
					pygame.mixer.music.load('Codex Audio/' +curIndex+ '.ogg')
					pygame.mixer.music.play(0, 0)
					pygame.mixer.music.set_volume(.85)
			elif curIndex in me1audiolist:
				if settings2['audio'] == 'True':
					pygame.mixer.quit()
					pygame.mixer.init(44000)
					pygame.mixer.music.load('Codex Audio/' +curIndex+ '.ogg')
					pygame.mixer.music.play(0, 0)

class autoupdater(wx.Frame):
	def __init__(self):
		updaterSize = (190, 130)
		self.url = 'http://coderslair.net/Python%20Programs/ME%20Codex%20Database/ME%20Codex%20Database.7z'
		self.message = 'N'
		wx.Frame.__init__(self, frame, -1, 'Updater', size=updaterSize, pos=(wx.GetDisplaySize()[0] / 2 - updaterSize[0] / 2, wx.GetDisplaySize()[1] / 2 - updaterSize[1] / 2), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR)
		self.updateevt(1.1, 'http://coderslair.net/Python%20Programs/ME%20Codex%20Database/Version/version.txt')
		self.SetIcon(Updateico.GetIcon())
		updatetxt = wx.StaticText(self, -1, self.message, pos=(10, 10))
		updatebtn = wx.Button(self, -1, 'Go to site', pos=(100, 70))

		self.Bind(wx.EVT_BUTTON, self.gotoevt, updatebtn)
		self.Bind(wx.EVT_CLOSE, self.onClose)

	def onClose(self, event):
		self.Destroy()
	def gotoevt(self, event):
		openSite(self.url)
		self.close()
	def updateevt(self, ver, file):
		try:
			html = urllib.urlopen(file)
			latest = float(html.readline())
		except (IOError, ValueError):
			self.message = 'Can\'t retrieve update information.'
			self.Show()
		else:
			if ver != latest and ver < latest:
				self.message = 'Update Available!'
				self.Show()
				html.close()
			else:
				self.Destroy()

#End of the program.  This is also where the program music is loaded.
app = wx.App(redirect=False)
frame = MainWindow()
frame.Center()
frame.Show()
frame2 = autoupdater()
device = audiere.open_device()
gmusic = device.open_file('Galaxy_Map.mp3')
gmusic.repeating = 1
gmusic.volume = .4
if settings2['music'] == 'True':
	gmusic.play()
app.MainLoop()