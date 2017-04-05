# coding: utf-8
"""
    This file is part of Plugin KodiLite by pcd@xtrend-alliance.com
    Copyright (C) 2014

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
############### v8.0 ##################
from enigma import eConsoleAppContainer,gPixmapPtr
try:
       from Plugins.Extensions.KodiLite.lib.Utils import *
except:       
       from lib.Utils import *
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigText, ConfigYesNo
from Components.config import NoSave
from Components.ConfigList import ConfigListScreen
from Screens.MessageBox import MessageBox
import os
from os import path, system

from Components.Task import Task, Job, job_manager as JobManager, Condition
from Screens.TaskView import JobView
from Screens.Console import Console
from Components.Button import Button
from Tools.Directories import fileExists, copyfile
from Tools.LoadPixmap import LoadPixmap
######################
import xml.etree.cElementTree 
import gettext
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Sources.List import List
from enigma import eTimer
try:
       from Plugins.Extensions.KodiLite.lib.SkinLoader import loadPluginSkin
except:       
       from lib.SkinLoader import loadPluginSkin
from GlobalActions import globalActionMap #mfaraj2608 needed for today changes
from keymapparser import readKeymap, removeKeymap #mfaraj2608 needed for today changes
##########################to avoid conflict with similar plugins
#import xpath
#import xbmcaddon, xbmcgui
import re
import datetime,time
##########################
from Screens.Standby import TryQuitMainloop
from Screens.InputBox import PinInput

#from Screens.VirtualKeyBoard import VirtualKeyBoard
try:
       from Plugins.Extensions.KodiLite.lib.VirtualKeyBoard import VirtualKeyBoard
       from Plugins.Extensions.KodiLite.lib.Spinner import Spinner
except:       
       from lib.VirtualKeyBoard import VirtualKeyBoard
       from lib.Spinner import Spinner
       
##########################
import gettext
def _(txt):
	t = gettext.dgettext("KodiLite", txt)
	if t == txt:
		print "[KodiLiteA] fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t

##########################
##########################
from glob import glob
import sys
from os.path import join, basename
##########################

             
select_file="/tmp/select.txt"
THISPLUG = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"
THISADDON = ""
HANDLE = 1
NEWDEFPY = ""
ARG = " "
DEBUG = 0
SELECT = []
newstext = " "
date = " "
NewUpdate = " "
PICPOS = []
dtext1 = " "
LAST = ""
F4MCMD = ""

#HOST = "http://mirrors.kodi.tv/addons/jarvis/"
#HOST = "https://github.com/hadynz/repository.arabic.xbmc-addons/tree/master/repo"
HOST = ""
HOST1 = "http://mirrors.kodi.tv/addons/jarvis/"

def getUrl(url):
        print "Here in getUrl url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def findmax(match = []):
                A = []
                B = []
                C = []
                D = []
                E = []
                imax = 0
                for item in match:
                        item = item.replace("%7E", "~")
                        x = item.split(".")
                        print "In findmax x =", x
                        A.append(int(x[0]))
#                        A.append((x[0]))
                lx = len(x)        
                Amax = max(A) 
                print "In findmax Amax =", Amax
                i1 = 0
                for a in A:
                      if a == Amax:
                             imax = i1
                             break
                      i1 = i1+1                
#                maxitem = str(Amax)
                print "In findnax imax A=", imax
                if lx > 1:
                    for item in match:        
                        x = item.split(".")
                        if int(x[0]) == int(Amax):
                                B.append(int(x[1]))
                        else:
#                                continue  
                                B.append(int('0'))       
                    Bmax = max(B) 
                    print "In findnax Bmax =", Bmax
                    i2 = 0
                    for b in B:
                         if b == Bmax:
                                imax = i2
                                break
                         i2 = i2+1                    
#                    maxitem = str(Amax) + "." + str(Bmax)
                    print "In findnax imax B=", imax
                    if lx > 2:
                      for item in match:        
                        x = item.split(".")
                        if (int(x[0]) == int(Amax)) and (int(x[1]) == int(Bmax)):
                                C.append(int(x[2]))
                        else:        
                                C.append(int('0'))
                      Cmax = max(C)
                      print "In findnax Cmax =", Cmax
                      i3 = 0
                      for c in C:
                            if c == Cmax:
                                   imax = i3
                                   break
                            i3 = i3+1
#                      maxitem = str(Amax) + "." + str(Bmax) + "." + str(Cmax)
                      print "In findnax imax C=", imax  
                print "In findnax imax final =", imax                              
                maxitem = match[imax]
                print "maxitem =", maxitem
                return maxitem        

   
        
def dellog():###to clear log files

   import os
   if os.path.exists("/tmp/e.log"):
      os.remove("/tmp/e.log")
   if os.path.exists("/tmp/xbmc_log"):
      os.remove("/tmp/xbmc_log")
   if os.path.exists("/tmp/KodiLite_log"):
      os.remove("/tmp/KodiLite_log")      
      
   if os.path.exists("/tmp/KodiLite_error"):
      os.remove("/tmp/KodiLite_error")
    
   if os.path.exists("/tmp/data.txt"):
      os.remove("/tmp/data.txt")  
   if os.path.exists("/tmp/vidinfo.txt"):
      os.remove("/tmp/vidinfo.txt")       
   if os.path.exists("/tmp/vidinfo.txt"):
      os.remove("/tmp/type.txt") 
      
def log(msg):
        f1=open("/tmp/e.log","a")
        f1.write(msg)
        f1.close()
          
def jointext(file1, file2):
                  f1=open(file1,"r+")
                  txt1 = f1.read()
                  f2=open(file2,"r")
                  txt2 = f2.read()
                  txt = txt1 + txt2
                  f1.write(txt)
                  f1.close()
                  f2.close()
                  

def parameters_string_to_dict(parameters):
    paramDict = {}
#    print "Here in parameters =", parameters
    if parameters:
        paramPairs = parameters.split("&")
        for paramsPair in paramPairs:
#            print "Here in paramPairs =", paramPairs
            if not "=" in paramsPair:
                    continue
            paramSplits = paramsPair.split('=')
            if paramSplits[0]=="?url":
               paramSplits[0]='url'
            paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def getpics(names, pics, tmpfold, picfold):
              if config.plugins.kodiplug.skinres.value == "fullhd":
                    nw = 300
              else:
                    nw = 200      
              pix = []
              if config.plugins.kodiplug.thumb.value == "False":
                      if config.plugins.kodiplug.skinres.value == "fullhd":
                                defpic = THISPLUG + "/skin/images/defaultL.png" 
                      else:       
                                defpic = THISPLUG + "/skin/images/default.png"    
                      npic = len(pics)
                      i = 0
                      while i < npic:
                             pix.append(defpic)
                             i = i+1
                      return pix
              cmd = "rm " + tmpfold + "/*"
              os.system(cmd)
              npic = len(pics)
              j = 0
              print "In getpics names =", names
              while j < npic:
                   name = names[j]
                   print "In getpics name =", name
                   if name is None:
                          name = "Video"
                   try:
                          name = name.replace("&", "")
                          name = name.replace(":", "")
                   except:
                          pass       
                   url = pics[j]
                   if url is None:
                          url = " "
                   if ".png" in url:
                          tpicf = tmpfold + "/" + name + ".png"
#                          picf = picfold + "/" + name + ".png"
                   else:       
                          tpicf = tmpfold + "/" + name + ".jpg"
#                          picf = picfold + "/" + name + ".jpg"
                   picf = picfold + "/" + name + ".png"       
                   if fileExists(picf):
                          cmd = "cp " + picf + " " + tmpfold
                          os.system(cmd)
                   
                   if not fileExists(picf):
                       if THISPLUG in url:
                          try:
                                  cmd = "cp " + url + " " + tpicf
                                  os.system(cmd)
                          except:
                                  pass
                       else:
#                          try:
                                  if url.startswith("https"):
                                         url = url.replace("https", "http")
                                  cmd = "wget -O '" + tpicf +"' -c '" + url + "'"
                                  os.system(cmd)
                                  """
                          except:
                                  if ".png" in tpicf:
                                          cmd = "cp " + THISPLUG + "/skin/images/default.png " + tpicf
                                  else:
                                          cmd = "cp " + THISPLUG + "/skin/images/default.jpg " + tpicf
                                  os.system(cmd)
                                  """        
                       if not fileExists(tpicf): 
                                  if ".png" in tpicf:
                                          cmd = "cp " + THISPLUG + "/skin/images/default.png " + tpicf
                                  else:
                                          cmd = "cp " + THISPLUG + "/skin/images/default.jpg " + tpicf
                                  os.system(cmd)

                       try:
                          try:
                                import Image
                          except:
                                from PIL import Image
                          im = Image.open(tpicf)
                          imode = im.mode
                          if im.mode != "P":
                                 im = im.convert("P")
                          w = im.size[0]
                          d = im.size[1]
                          r = float(d)/float(w)
                          d1 = r*nw
                          if w != nw:        
                                 x = int(nw)

                                 y = int(d1)
                                 im = im.resize((x,y), Image.ANTIALIAS)
                          tpicf = tmpfold + "/" + name + ".png"
                          picf = picfold + "/" + name + ".png"
                          im.save(tpicf)

                       except:

                          tpicf = THISPLUG + "/skin/images/default.png" 
                          
                   pix.append(j)
                   pix[j] = picf
                   j = j+1       
              cmd1 = "cp " + tmpfold + "/* " + picfold + " && rm " + tmpfold + "/* &"
              os.system(cmd1)
              return pix
                  
             
def up(names, tmppics, pos, menu, pixmap):
                menu.up()
                pos = pos - 1
                num = len(names)
                if pos == -1:
                              pos = num - 1
                              menu.moveToIndex(pos)  
                name = names[pos]
                if name == "Exit":
                         if config.plugins.kodiplug.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitLL.png" 
                         else:       
                                pic1 = THISPLUG + "/skin/images/ExitL.png"     
                         pixmap.instance.setPixmapFromFile(pic1)
                else:
                        try: 
                         pic1 = tmppics[pos]
                         pixmap.instance.setPixmapFromFile(pic1)
                        except:
                         pass 
                return pos
                
def down(names, tmppics, pos, menu, pixmap):
                menu.down()
                pos = pos + 1
                num = len(names)
                if pos == num:
                              pos = 0
                              menu.moveToIndex(pos) 
                name = names[pos]
                if name == "Exit":
                         if config.plugins.kodiplug.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitLL.png" 
                         else:       
                                pic1 = THISPLUG + "/skin/images/ExitL.png"     
                         pixmap.instance.setPixmapFromFile(pic1)
                else:
                        try:
                         pic1 = tmppics[pos]
                         pixmap.instance.setPixmapFromFile(pic1)
                        except:
                         pass 
                return pos
                      
def left(names, tmppics, pos, menu, pixmap):
         menu.pageUp()
         pos = menu.getSelectionIndex()
         name = names[pos]
         
         if name != "Exit":
                pic1 = tmppics[pos]
                pixmap.instance.setPixmapFromFile(pic1)

         else:      
                try:
                         if config.plugins.kodiplug.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitLL.png" 
                         else:       
                                pic1 = THISPLUG + "/skin/images/ExitL.png"     
                         pixmap.instance.setPixmapFromFile(pic1) 
                except:
                  pass       
         return pos
         
def right(names, tmppics, pos, menu, pixmap):
         menu.pageDown()
         pos = menu.getSelectionIndex()
         name = names[pos]
         if name != "Exit":
                pic1 = tmppics[pos]
                pixmap.instance.setPixmapFromFile(pic1)
         else:      
                try:
                       if config.plugins.kodiplug.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitLL.png" 
                       else:       
                                pic1 = THISPLUG + "/skin/images/ExitL.png"     
                       pixmap.instance.setPixmapFromFile(pic1)
                except:
                       pass                       
         return pos                  
                
config.plugins.kodiplug = ConfigSubsection()
config.plugins.kodiplug.tempdel = ConfigYesNo(False)
config.plugins.kodiplug.picdel = ConfigYesNo(False)
config.plugins.kodiplug.subtitle = ConfigYesNo(False)
config.plugins.kodiplug.cachefold = ConfigText("/media/hdd", False)
config.plugins.kodiplug.vlcip = ConfigText("192.168.1.1", False)
config.plugins.kodiplug.mmenu = ConfigYesNo(True)
#config.plugins.kodiplug.debug = ConfigYesNo(False)
config.plugins.kodiplug.thumb = ConfigSelection(default = "False", choices = [("True", _("yes")),("False", _("no")), ("Single", _("single"))])   
config.plugins.kodiplug.backup = ConfigYesNo(False)
config.plugins.kodiplug.directpl = ConfigYesNo(False)
config.plugins.kodiplug.textcol = NoSave(ConfigSelection(default = "0xffffff", choices = [("0xffffff", _("white")), ("0xb3b3b9", _("grey"))]))  
config.plugins.kodiplug.textsel = NoSave(ConfigSelection(default = "0xf07655", choices = [("0xf07655", _("red")),("0xe5b243", _("yellow")), ("0xffffff", _("white"))]))   
config.plugins.kodiplug.textfont = ConfigSelection(default = "22", choices = [("25", _("medium")), ("35", _("large")), ("22", _("small"))])  
config.plugins.kodiplug.skinres = ConfigSelection(default = "hd", choices = [("fullhd", _("Full-HD 1920x1080")), ("hd", _("HD 1280x720"))])  
config.plugins.kodiplug.wait = ConfigSelection(default = "10", choices = [("10", _("10sec")),("20", _("20sec")),("30", _("30sec")),("40", _("40sec")),("60", _("60sec")), ("120", _("120sec")), ("180", _("180sec")), ("240", _("240sec")), ("300", _("300sec"))])  
config.plugins.kodiplug.listcol = NoSave(ConfigSelection(default = "0x000000", choices = [("0x40000000", _("black")), ("0x40002d39", _("blue"))]))  
config.plugins.kodiplug.mainback = NoSave(ConfigSelection(default = "default", choices = [("default", _("default")), ("skin2", _("skin2"))]))  
config.plugins.kodiplug.viewdownloads = NoSave(ConfigSelection(default="disabled", choices = [("disabled",_("Not assigned")), ("help",_("Key help"))]))
config.plugins.kodiplug.youtubequal = NoSave(ConfigSelection(default="2", choices = [("1",_("SD")), ("2",_("720p")), ("3",_("1080p"))]))

def update_xbmc_text(addon_id):##mfaraj to update the file from xbmc client to be used by xbmc library files
            if addon_id==None:
               return
            try:cachefolder=config.plugins.kodiplug.cachefold.value
            except:cachefolder="/media/hdd"
            afile=open("/etc/xbmc.txt",'w')
            afile.write(cachefolder)
            afile.close()

            
def startspinner():
                cursel = THISPLUG+"/skin/spinner"
    		Bilder = []
		if cursel:
			for i in range(30):
				if (os.path.isfile("%s/wait%d.png"%(cursel,i+1))):
					Bilder.append("%s/wait%d.png"%(cursel,i+1))
		else:
		        Bilder = []
                #self["text"].setText("Press ok to exit")
                return Spinner(Bilder)             
def buildBilder():
                cursel = THISPLUG+"/skin/spinner"
    		Bilder = []
		if cursel:
			for i in range(30):
				if (os.path.isfile("%s/wait%d.png"%(cursel,i+1))):
					Bilder.append("%s/wait%d.png"%(cursel,i+1))
		else:
		        Bilder = []
                #self["text"].setText("Press ok to exit")
                
                return Bilder

class XbmcConfigScreen(ConfigListScreen,Screen):
   	
	def __init__(self, session, args = 0):
		self.session = session
		self.setup_title = _("Plugin Configuration")
		self["title"] = Button(self.setup_title)
		Screen.__init__(self, session)
		self.skinName = "Kodiconfig"

		cfg = config.plugins.kodiplug 
                self.list = [
                        getConfigListEntry(_("Cache folder"), cfg.cachefold),
                        getConfigListEntry(_("Skin resolution-(restart e2 after change)"), cfg.skinres),
                        getConfigListEntry(_("Text font in lists"), cfg.textfont),
                        getConfigListEntry(_("Wait time for lists (sec)"), cfg.wait),
                        getConfigListEntry(_("Install subtitles support ?"), cfg.subtitle),
                        getConfigListEntry(_("VLC server ip"), cfg.vlcip),
#                        getConfigListEntry(_("Stop download at Exit from plugin ?"), cfg.tempdel),
#                        getConfigListEntry(_("Delete thumbpics at Exit from plugin ?"), cfg.picdel),
#                        getConfigListEntry(_("Show in mainmenu-(restart e2 after change)"), cfg.mmenu),
#                        getConfigListEntry(_("View downloads key-(restart e2 after change)"), cfg.viewdownloads), 
#                        getConfigListEntry(_("Debug log ?"), cfg.debug),
                        getConfigListEntry(_("Show thumbpic ?"), cfg.thumb),
                        getConfigListEntry(_("Move addons to cache folder ?"), cfg.backup),
                        getConfigListEntry(_("Play videos direct with no download option ?"), cfg.directpl),

#                        getConfigListEntry(_("Text colour in lists"), cfg.textcol),
#                        getConfigListEntry(_("Selected-text colour in lists"), cfg.textsel),
#                        getConfigListEntry(_("List background colour"), cfg.listcol),
#                        getConfigListEntry(_("YouTube video quality"), cfg.youtubequal),
 			]
		ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
		self["status"] = Label()
		self["statusbar"] = Label()
		self["key_red"] = Button(_("Exit"))
		self["key_green"] = Button(_("Save"))

		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "TimerEditActions"],
		{
			"red": self.cancel,
			"green": self.save,
			"cancel": self.cancel,
			"ok": self.save,
		}, -2)
		self.onChangedEntry = []
	
	def changedEntry(self):
		for x in self.onChangedEntry:
			x()
               	
	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]
	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())
	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary

	def cancel(self):
		for x in self["config"].list:
			x[1].cancel()
                self.close()


	def save(self):
                self.saveAll()
                picfold = config.plugins.kodiplug.cachefold.value + "/xbmc/pic"
                cmd = "rm -rf " + picfold
                os.system(cmd)
                subs = config.plugins.kodiplug.subtitle.value
                tfile = THISPLUG + "/scripts/script.module.SubsSupport"
                if not os.path.exists(tfile):
                    if subs is True:
                       fdest = THISPLUG + "/scripts"
                       dest = "/tmp/subssupport.zip"
                       xfile = "http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiLite/Script-modules/kodi/script.module.SubsSupport-1.0.0.zip" 
                       cmd1 = "wget -O '" + dest + "' '" + xfile + "'"
                       cmd2 = "unzip -o -q '/tmp/subssupport.zip' -d " + fdest
                       
                       cmd = []
                       cmd.append(cmd1)
                       cmd.append(cmd2)
                       
                       print "In main cmd =", cmd
                       title = _("Installing script subssupport %s")
                       self.session.openWithCallback(self.subsdown,Console,_(title),cmd)
                else:
                       pass  
                self.session.open(TryQuitMainloop, 3) 
                           
        def subsdown(self):
                pass       
                       
class Rundefault(Screen):
    def __init__(self, session, name, url, nextrun,progressCallBack=None):
                Screen.__init__(self, session)
                self.name = name
                self.session=session
                self.url = url
                self.nextrun = nextrun

                self.onShown.append(self.start)
                self.error=None
                self.data1=''
########################
                self.updateTimer = eTimer()
                try:
                      self.updateTimer_conn = self.updateTimer.timeout.connect(self.updateStatus)
                except AttributeError:
                      self.updateTimer.callback.append(self.updateStatus)
                self.timecount = 0
                ncount = config.plugins.kodiplug.wait.value 

#                nc = int(ncount)*1000
#                timeint = int(float(nc/120))
#                print "timeint =", timeint
                self.timeint = 1000
                self.nct = int(ncount)
#                self.nct = int(float(nc/self.timeint))
#                print "self.nct =", self.nct
#		self.updateTimer.start(timeint)
#		self.updateStatus()
########################                
                self.error=''                
                self.progressCallBack=progressCallBack
                self.progress=(_('Please wait...\n'))
                if os.path.exists("/tmp/stopaddon"):
                   os.remove("/tmp/stopaddon")
    def start(self):
                url = self.url
                name = self.name
                if DEBUG == 1:
                       print "In Rundefault name =", name
                       print "In Rundefault url =", url
                       print "In Rundefault self.nextrun =", self.nextrun
#                print "In Rundefault url B=", url       
                if (THISPLUG not in url):
                        desc = " "
                        self.progressCallBack("Finished")
                        self.updateTimer.stop()
                        self.session.open(Playvid, name, url, desc)
                        self.close()
                        
                else:		
########################pictures?###########
                   n1 = url.find("default.py?", 0)
                   urla = url[(n1+11):]
                   print "In Rundefault urla =", urla
                   plugin_id=os.path.split(THISADDON)[1]
                   if ("plugin.image" in plugin_id) or ("plugin.picture" in plugin_id) and ("url=" not in urla) and ("plugin://" not in urla):
                        print "In Rundefault going in picshow"
                        self.picshow(urla)
                   else:
#######################pictures#############
                        global HANDLE
                        hdl = int(HANDLE)
                        hdl = hdl+1
                        HANDLE = str(hdl)
                        n1 = url.find('?', 0)
                        if n1<0:
                                return
                                
                        url1 = url[:n1]
                        url2 = url[n1:]
                        url2 = url2.replace(" ", "%20") 
                        if "plugin://plugin.video.youtube/" in url:
                               url1 = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins/plugin.video.youtube/default.py"
                               url2 = url2.replace("plugin://plugin.video.youtube/?", "path=/root/video&")

#                        url2 = url[n1:]
#                        url2 = url2.replace(" ", "%20")        
                        arg = url1 + " " + HANDLE + " '" + url2 + "'"
                        if DEBUG == 1:
                               print "Rundefault arg =", arg
                        self.arg = arg
                        self.stream()
                        
    def picshow(self, urla):
                xurl = urla
                xdest = "/tmp/picture.png"
	        downloadPage(xurl, xdest).addCallback(self.picture).addErrback(self.showError)

    def showError(self, error):
                print "ERROR :", error

    def picture(self, fplug):                        
                pic = "/tmp/picture.png"
##                self.session.open(Showpic, pic)
#                self.close()        
                self.session.open(Splash3, pic)        
                        
                   
    def stoprun(self):
                self.close() 
		try:
			
			self.container.appClosed.remove(self.runFinished)
			self.container.dataAvail.remove(self.dataAvail)
                        self.progressCallBack("Finished")    
                except:
                        pass
    
                                         

    def dataAvail(self,rstr):
            if os.path.exists("/tmp/stopaddon"):
                self.stoprun()
                return
            if rstr:
               self.data1=self.data1+rstr
               if self.progressCallBack is not None:
                  self.progress=self.progress+"..."
                  self.progressCallBack(self.progress)
            #if self.progress_callback is not None:
               #self.progress_callback('Please wait..")
    
                                                   
    def stream(self):

                self.picfold = config.plugins.kodiplug.cachefold.value+"/xbmc/pic"
                self.tmpfold = config.plugins.kodiplug.cachefold.value+"/xbmc/tmp"
#                cmd = "rm -rf " + self.tmpfold
#                system(cmd)
                
                if os.path.exists("/tmp/stopaddon"):
                   self.stoprun()
                   return
                
                if DEBUG == 1:
                       print "In rundef self.arg =", self.arg
                cmd = "python " + self.arg
                print "In rundef cmd A=", cmd
#                cmd = cmd.replace("&", "\\&")
#                cmd = cmd.replace("(", "\\(")
#                cmd = cmd.replace(")", "\\)")
                afile = file("/tmp/test.txt","w")       
                afile.write("going in default.py")
                afile.write(cmd)
                fdef = 'default'#NEWDEFPY[:-3]
                args = cmd.split(" ")
                arg1 = args[1]
                arg2 = args[2]
                arg3 = args[3]
                arg4=config.plugins.kodiplug.cachefold.value
                sys.argv = [arg1,arg2, arg3,arg4]                
                self.plugin_id=os.path.split(THISADDON)[1]
#                dellog()
                
                print "539arg3 =",arg3
                if 'select=true' in arg3 :
                      f = open("/tmp/result.txt", "w")
	              line = arg3.replace("'?", "")
	              params=parameters_string_to_dict(line)
	              print "Here in select writing result.txt params =", params
	              url = params.get("url","0")
                      text = url + "\n"
                      print "Here in select writing result.txt text =", text
                      f.write(text)
                      f.close()
        
                      myfile = file(r"/tmp/arg1.txt")       
                      icount = 0
                      for line in myfile.readlines(): 
                            sysarg = line
                            icount = icount+1
                            if icount > 0:
                                 break
                        
                      print "sysarg =", sysarg
                      args = sysarg.split(" ")
#              
                      cmd = "python '" + args[0] +"' '1' '" + args[2] + "'"
                  
                   
                else:
                   
                   xpath_file=THISPLUG+"/plugins/"+self.plugin_id+"/xpath.py"
                   fixed2_file=THISPLUG+"/plugins/"+self.plugin_id+"/fixed2"
                   default_file=THISPLUG+"/plugins/"+self.plugin_id+"/default.py" 
#                   if not os.path.exists(xpath_file): 
#                   os.system("cp -f "+THISPLUG+"/lib/xpath.py "+xpath_file)
#                      os.system("touch " + fixed2_file)                                       
#                   if not os.path.exists(fixed2_file):
#                      os.system("cp -f "+THISPLUG+"/lib/xpath.py "+xpath_file)
#                      os.system("touch " + fixed2_file)

                   print "In rundef cmd B=", cmd
###                   cmd='python '+default_file+' 1 '+"'"+arg3+"'" 
                   print "In rundef cmd C=", cmd
                       
                ###############################

               
                 
                #cmd='python '+xpath_file+' 1 '+arg3      
                self.container = eConsoleAppContainer()
#		self.container.appClosed.append(self.action)
##                try:
##		       self.container.appClosed.append(self.finad)
##                except:       
##                       self.container.appClosed.connect(self.finad) 			        
#		self.container.dataAvail.append(self.dataAvail)
##		try:
##		       self.container.dataAvail.append(self.dataAvail)
##                except:       
##                       self.container.dataAvail.connect(self.dataAvail) 	
		self.data1=''		
#                if os.path.exists("/tmp/KodiLite_log"):
#                    os.remove("/tmp/KodiLite_log")
                    
                if os.path.exists("/tmp/data.txt"):
                   os.remove("/tmp/data.txt")                    		
#                if DEBUG == 1:
                self.lastcmd = cmd
                global LAST
                LAST = self.lastcmd
                cmd = cmd + " &"
                print "In Rundefault cmd =", cmd
###################################################                
###################################################                
                timen = time.time() 
                global NTIME 
                timenow = timen - NTIME
                NTIME = timen
                print "In Rundefault 1 timenow", timenow
##                os.system(cmd)
#                       self.action(" ")
#                self.container.execute(cmd) 
                self.dtext = " "
                log("\n"+cmd)
                self.p = os.popen(cmd)
                self.timecount = 0
                self.updateTimer.start(self.timeint)

    
    def updateStatus(self):
         ncount = config.plugins.kodiplug.wait.value
         self.timecount = self.timecount + 1 
         print "In rundef updateStatus self.timecount =", self.timecount
         self.dtext = self.p.read()
         print "In rundef updateStatus self.dtext =", self.dtext
         global dtext1
         if len(self.dtext) > 0:
                dtext1 = dtext1 + self.dtext
         if "data B" in self.dtext:
                self.updateTimer.stop()
                self.action(" ")
         """
         if os.path.exists(self.dfile):
            b1 = os.path.getsize(self.dfile)
            if b1 > 0:
              print "In rundef b1 =", b1
              b = b1 / 1000
              print "In rundef b =", b
              try:
                  print "In rundef self.bLast =", self.bLast
                  if b == self.bLast:
                     self.updateTimer.stop()
                     self.action(" ")
              except:
                   pass      
              self.bLast = b
         """
         print "In rundef self.timecount =", self.timecount 
         if self.timecount > self.nct:     
              self.updateTimer.stop()
              f1=open("/tmp/e.log","a")
#              f1.write(dtext1)
              f1.close()
              self.action(" ")
              
#         elif self.timecount > 10:
#              print "No /tmp/data.txt", b
#              self.updateTimer.stop()
#              self.close()
              
              
    def callback(self,result):
        if result:
           self.stream()		
    def action(self,retval):
            print "In Rundefault action 1"
            if os.path.exists("/tmp/stopaddon"):
                   self.stoprun()
                   return    
            #######################
            str = self.data1
            print "In Rundefault action 2"
            ########################  
              
            self.data = []
            self.names = []
            self.urls = []
            self.pics = []
            self.names.append("Exit")
            self.urls.append(" ")
            if config.plugins.kodiplug.skinres.value == "fullhd":
                                exitpic = THISPLUG + "/skin/images/ExitL.png"
            else:
                                exitpic = THISPLUG + "/skin/images/Exit.png"
            self.pics.append(exitpic)
            self.tmppics = []
            self.lines = []
            self.vidinfo = []
            afile = open("/tmp/test.txt","w")       
            afile.write("\nin action=")
            datain =""
            parameters = []
            print "In Rundefault action 3"
            self.data = []
#            dtext = self.p.read()
            data = self.dtext.splitlines()
            for line in data:
                   print "In Rundefault line =", line
                   if not "data B" in line: continue
                   else: 
                         i1 = line.find("&", 0)
                         line1 = line[i1:]
                         self.data.append(line1)
            print "In Rundefault self.data =", self.data 
            ln = len(self.data)
            if ln == 0:
                 cmd = LAST + " > /tmp/error.log 2>&1 &"
                 os.system(cmd)
                 self.error=(_("Error! Try another item OR exit and submit log /tmp/e.log and /tmp/error.log"))
                 self.progressCallBack((_("Error! Try another item OR exit and submit log /tmp/e.log and /tmp/error.log")))
                 return
                    
            """           
            if not path.exists("/tmp/data.txt"):
                try:
                 self.lastcmd = self.lastcmd + " > /tmp/e1.log 2>&1"
                 os.system(self.lastcmd)
                 jointext("/tmp/e.log", "/tmp/e1.log")
                 self.error=(_("Error! Submit log /tmp/e.log. For more info use button 'Tips' in first screen"))
                 self.progressCallBack((_("Error! Submit log /tmp/e.log. For more info use button 'Tips' in first screen")))
                 return
                except:
                 return 
            else:
                 timen = time.time() 
                 global NTIME 
                 timenow = timen - NTIME
                 NTIME = timen
                 print"In Rundefault 2 timenow", timenow
                 print "In Rundefault action 4"
                 self.progressCallBack(_("Finished"))
                 if not path.exists("/tmp/vidinfo.txt"):
                       pass
                 else:
                       myfile = file(r"/tmp/vidinfo.txt")       
                       icount = 0
                       vinfo = myfile.read()
                       myfile.close()
                       self.vidinfo = vinfo.split("ITEM")
                 
                 myfile = open(r"/tmp/data.txt")       
                 icount = 0
                 self.error='Finished'
                 for line in myfile.readlines():
                        print "In rundef line =", line
                        n1 = line.find("name=", 0)
                        n2 = line.find("&name=", (n1+3))
#                        print "In rundef n1, n2 =", n1, n2
                        if n2 > -1:
                             line = line[n2:]
                        datain = line[:-1]
                        self.data.append(icount)
                        self.data[icount] = datain
                        icount = icount+1
                 myfile.close()
            """
            n1 = 0
            if n1==0:    
                 inum = len(self.data)
                 i = 0
                 while i < inum:
                        name = " "
                        url = " "
                        line = self.data[i]
                        if DEBUG == 1:
                               print "In rundef line B=", line
                        if line.startswith("&"):
                               line = line[1:]
#                        print "In rundef line C=", line       
                        params = parameters_string_to_dict(line)
                        if DEBUG == 1:
                               print "Rundefault params=", params
                        self.lines.append(line)
                        try:
                               name = params.get("name")
                               name = name.replace("AxNxD", "&")
                               name = name.replace("ExQ", "=")
                               if DEBUG == 1:
                                       print "Rundefault name=", name       
                        except:
                               pass
                        try:
                               url = params.get("url")
                               url = url.replace("AxNxD", "&")
                               url = url.replace("ExQ", "=")
                               if DEBUG == 1:
                                       print "Rundefault url=", url      
                        except:
                              pass
                        """      
                        try:
                              pic = params.get("thumbnailImage")
                              if (pic == "DefaultFolder.png"):
                                     pic = THISPLUG + "/skin/images/default.png"
                        except:
                              pic = THISPLUG + "/skin/images/default.png" 
                        """
                        thumbnailImage = params.get("thumbnailImage") 
                        print "Rundefault thumbnailImage=", thumbnailImage   
                        iconImage = params.get("iconImage") 
                        print "Rundefault iconImage=", iconImage
                        try:
                           if thumbnailImage.startswith("http"):
                               pic = thumbnailImage
                               print "Rundefault pic A=", pic
                           elif iconImage.startswith("http"):
                               pic = iconImage
                               print "Rundefault pic B=", pic
                           else:
                               pic = THISPLUG + "/skin/images/default.png"
                        except:
                               pic = THISPLUG + "/skin/images/default.png"
                        if DEBUG == 1:
                                       print "Rundefault pic=", pic              
                        self.names.append(name)
                        self.urls.append(url)
                        self.pics.append(pic)
                        i = i+1
                 if DEBUG == 1:
                        print "Rundefault self.names=", self.names
                        print "Rundefault self.urls=", self.urls
                        print "Rundefault self.pics=", self.pics
                 if (len(self.names) == 2) and (self.urls[1] is None) and (THISPLUG not in self.names[1]):
                        if "*download*" in self.names[1]:
                                url = self.names[1].replace("*download*", "")
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Getvid, name, url, desc)
                                self.close()
                        elif "*download2*" in self.names[1]:
                                url = self.names[1].replace("*download2*", "")
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Getvid2, name, url, desc)
                                self.close()
                        elif ("stack://" in self.names[1]):
                                stkurl = self.names[1]
                                self.playstack(stkurl)

                        elif ("rtmp" in self.names[1]):
                            if "live" in name:
                                name = self.name
                                desc = " "
                                url = self.names[1]
#                                self.session.open(Showrtmp2, name, url, desc)
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Playvid, name, url, desc)
                                self.close()
                           
                            else:
                                name = self.name
                                desc = " "
                                url = self.names[1]
#                                self.session.open(Showrtmp, name, url, desc)
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Playvid, name, url, desc)
                                self.close()        
                                
                        else:        
                                name = self.name                                
                                desc = " "
                                url = self.names[1]
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Playvid, name, url, desc)
                                self.close()
                 elif (len(self.names) == 2) and (self.urls[1] is not None) and (THISPLUG not in self.urls[1]):
                        url = self.urls[1]
                        if "*download*" in url:
                                url = url.replace("*download*", "")
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Getvid, name, url, desc)
                                self.close()
                        elif "*download2*" in url:
                                url = url.replace("*download2*", "")
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("")
                                self.updateTimer.stop()
                                self.session.open(Getvid2, name, url, desc)
                                self.close()
                                       
                        else:
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Playvid, name, url, desc)
                                self.close()    
#                 else:        
#                        self.tmppics = getpics(self.names, self.pics, self.tmpfold, self.picfold)
                        #if int(self.nextrun) == 2:
#                        self.progressCallBack("")
#                        self.session.open(XbmcPluginScreen,self.name,self.names, self.urls, self.tmppics,self.nextrun)
#                        self.close()
                        
                        
                        
                 else:  
                    inm = 0 
                    for name in self.names:
                                if name is None:
                                      self.names[inm] = "Video"
                                self.names[inm] = self.names[inm].replace(":", "-")
                                self.names[inm] = self.names[inm].replace("&", "-")
                                self.names[inm] = self.names[inm].replace("'", "-")
                                self.names[inm] = self.names[inm].replace("?", "-")
                                self.names[inm] = self.names[inm].replace("/", "-")
                                self.names[inm] = self.names[inm].replace("#", "-")
                                self.names[inm] = self.names[inm].replace("|", "-")
                                self.names[inm] = self.names[inm].replace("*", "")
                                inm = inm+1
                    ipic = 2 
                    npic = len(self.pics)
                    cpic = self.pics[1]
                    print "cpic =", cpic
                    print "self.pics A=", self.pics
                    while ipic < npic:
                          pic = self.pics[ipic]
                          if pic == cpic:
                                self.pics[ipic] = THISPLUG + "/skin/images/default.png"
                          ipic = ipic+1
                          
                    print "self.pics B=", self.pics
                    if config.plugins.kodiplug.thumb.value == "True":
                               self.tmppics = getpics(self.names, self.pics, self.tmpfold, self.picfold)
                               self.session.open(XbmcPluginScreen2,self.name,self.names, self.urls, self.tmppics,self.nextrun)
                    else:                       
                               self.tmppics = getpics(self.names, self.pics, self.tmpfold, self.picfold)
                               self.session.open(XbmcPluginScreen,self.name,self.names, self.urls, self.tmppics,self.nextrun)
                    """
                    else:                       
                        
                        timenow = time.time()
                        global NTIME
                        NTIME = timenow
                        timen = timenow - NTIME
                        print "Before getpics2 timen =", timen
                        namelist = ""
                        piclist = ""
                        self.tmppics = []
                        inm = 0 
                        for name in self.names:
                                if name is None:
                                      self.names[inm] = "Video"
                                self.names[inm] = self.names[inm].replace(":", "-")
                                self.names[inm] = self.names[inm].replace("&", "-")
                                self.names[inm] = self.names[inm].replace("'", "-")
                                self.names[inm] = self.names[inm].replace("?", "-")
                                self.names[inm] = self.names[inm].replace("/", "-")
                                self.names[inm] = self.names[inm].replace("#", "-")
                                self.names[inm] = self.names[inm].replace("|", "-")
                                inm = inm+1
                        for name in self.names:
                                namelist = namelist + "#####" + name
                                name1 = "/media/hdd/xbmc/pic/" + name + ".png"
                                self.tmppics.append(name1) 
                        for pic in self.pics:
                                if pic is None:
                                      pic = THISPLUG + "/skin/images/default.png"
                                piclist = piclist + "#####" + pic
                        tfold = self.tmpfold
                        pfold = self.picfold    
                        namelist = namelist[5:]
                        
                        print "Before getpics2 namelist =", namelist
                        piclist = piclist[5:]
                        piclist = piclist.replace("'", "$$$$")   
                        print "Before getpics2 piclist =", piclist
                        cmd = "python " + THISPLUG + "/Getpics.py '" + namelist + "' '" + piclist + "' '" + tfold + "' '" + pfold + "' &"
                        print "Before getpics2 cmd =", cmd
                        os.system(cmd)
                        
#                        self.tmppics = getpics2(self.names, self.pics, self.tmpfold, self.picfold)
                        timenow = time.time()
                        timen = timenow - NTIME
                        print "After getpics2 timen =", timen
#                        self.tmppics = getpics(self.names, self.pics, self.tmpfold, self.picfold)
#                        timenow = time.time()
#                        timen = timenow - NTIME
                        print "After getpics timen =", timen
                        #if int(self.nextrun) == 2:
                        self.progressCallBack("")
                        self.session.open(XbmcPluginScreen2,self.name,self.names, self.urls, self.tmppics,self.nextrun)
                        print "Here in rundef end"
                    """
              
    def playstack(self, urlFull):
          if DEBUG == 1:
                 print "urlFull =", urlFull 
          playlist = []
          names = []
          i = 0
          start = 0
          while i<20:
                 n1 = urlFull.find("http", start)
                 if n1 < 0:
                        break
                 n2 = urlFull.find("http", (n1+4))
                 if n2 < 0:
                        n2 = len(urlFull)
                 url1 = urlFull[n1:n2]
#                 print "url1 =", url1 
                 n3 = url1.find(".mp4", 0)
                 if n3<0:
                        n3 = url1.find(".flv", 0)
                        if n3<0:
                              break 
                 url1 = url1[0:(n3+4)]
#                 print "url1 B=", url1
                 name = "Video" + str(i)
                 playlist.append(url1)
                 names.append(name)
#                 print "n1, n2, n3 =", n1, n2, n3
#                 print "playlist[i] =", playlist[i]
                 start = n2-1
                 i = i+1
          idx = 0       
          self.session.open(Playlist, idx, names, playlist)

    def keyNumberGlobal(self, number):
		self["text"].number(number)

#########################
class XbmcPluginScreen2(Screen):

	def __init__(self, session, name, names, urls, tmppics,curr_run):
		self.skinName = "XbmcPluginScreen2"
		Screen.__init__(self, session)
		title = "KodiLite 3.0"
		self["title"] = Button(title)
		self["bild"] = startspinner()
		self.curr_run = curr_run
		self.nextrun=self.curr_run+1
		self.pos = []		
                if config.plugins.kodiplug.skinres.value == "fullhd": 
                       self.pos.append([35,80])
                       self.pos.append([395,80])
                       self.pos.append([755,80])
                       self.pos.append([1115,80])
                       self.pos.append([1475,80])
                       self.pos.append([35,530])
                       self.pos.append([395,530])
                       self.pos.append([755,530])
                       self.pos.append([1115,530])
                       self.pos.append([1475,530])
                else:       
                       self.pos.append([20,50])
                       self.pos.append([260,50])
                       self.pos.append([500,50])
                       self.pos.append([740,50])
                       self.pos.append([980,50])
                
                       self.pos.append([20,350])
                       self.pos.append([260,350])
                       self.pos.append([500,350])
                       self.pos.append([740,350])
                       self.pos.append([980,350])                       

                print " self.pos =", self.pos
		
		list = []
                self.name = name
		self.pics = tmppics
		self.mlist = names
		self.urls1 = urls
		self.names1 = names
		self["info"] = Label()
		
		self.curr_run=curr_run
		txt = str(SELECT[self.curr_run])
		print "In XbmcPluginScreen SELECT[self.curr_run] A=", SELECT[self.curr_run]
		self.nextrun=self.curr_run+1
	 	print "2028",txt	
		self.select=txt
		self.rundef=None
		self.plug=''
		self.keylock=False
		self.spinner_running=False

		
		print "self.mlist =", self.mlist
                list = names
                self["menu"] = List(list)
                
                for x in list:
                       print "x in list =", x

                ip = 0
                print "self.pics = ", self.pics

		self["frame"] = MovingPixmap()

                self["label1"] = StaticText()
                self["label2"] = StaticText()
                self["label3"] = StaticText()
                self["label4"] = StaticText()
                self["label5"] = StaticText()
                self["label6"] = StaticText()
                self["label7"] = StaticText()
                self["label8"] = StaticText()
                self["label9"] = StaticText()
                self["label10"] = StaticText()
                self["label11"] = StaticText()
                self["label12"] = StaticText()
                self["label13"] = StaticText()
                self["label14"] = StaticText()
                self["label15"] = StaticText()
                self["label16"] = StaticText()


                self["pixmap1"] = Pixmap()
                self["pixmap2"] = Pixmap()
                self["pixmap3"] = Pixmap()
                self["pixmap4"] = Pixmap()
                self["pixmap5"] = Pixmap()
                self["pixmap6"] = Pixmap()
                self["pixmap7"] = Pixmap()
                self["pixmap8"] = Pixmap()
                self["pixmap9"] = Pixmap()
                self["pixmap10"] = Pixmap()
                self["pixmap11"] = Pixmap()
                self["pixmap12"] = Pixmap()
                self["pixmap13"] = Pixmap()
                self["pixmap14"] = Pixmap()
                self["pixmap15"] = Pixmap()
                self["pixmap16"] = Pixmap()
                i = 0

                self["actions"] = NumberActionMap(["OkCancelActions", "MenuActions", "DirectionActions", "NumberActions"],
			{
				"ok": self.okClicked,
				"cancel": self.cancel,
				"left": self.key_left,
			        "right": self.key_right,
			        "up": self.key_up,
			        "down": self.key_down,
			})

                self.index = 0
                ln = len(self.names1)
                self.npage = int(float(ln/10)) + 1
                print "self.npage =", self.npage
                self.ipage = 1
                self.icount = 0
                print "Going in openTest"
                self.onLayoutFinish.append(self.openTest)
                
        def cancel(self):
                       self.close()
                             
        def startSpinner(self):
            if self.spinner_running==False:
                Bilder=buildBilder()
                self["bild"].start(Bilder)
                self.spinner_running=True
                return    
        def stopSpinner(self):
            if self.spinner_running==True:
                self["bild"].stop()
                self.spinner_running=False
                self['bild'].instance.setPixmap(gPixmapPtr())
            return            

        def exit(self):
          if self.spinner_running==True:
           self.stopSpinner()
           self.keylock=False
           
           afile=open("/tmp/stopaddon","w")
           afile.write("stop execution")
           afile.close()
           
           self.progressCallBack("Finished")           
           try:self.rundef.stoprun()
           except:pass
          else:
           self.stopSpinner()   
           #self['bild']=None 
#           dellog()
           self.close()          
           
        
        #self['bild']=None
        
        def progressCallBack(self,progress):
          try:
             if progress is not None:
                if progress.startswith("Error"):
                   self.keylock=False
                   self["info"].setText(progress)
                   self.stopSpinner() 
                   return       
                if  progress=="Finished":
                   self.keylock=False
                   self.selection_changed()
                   self.stopSpinner()
                   return
           
             self["info"].setText(progress)
          except:
                  pass  
        
        def selection_changed(self):
          self.keylock=False
          try:self["info"].setText(self.select)
          except:pass
    
        def showerror(self):
          try:
                 from Plugins.Extensions.KodiLite.lib.XBMCAddonsinfo import XBMCAddonsinfoScreen
          except:       
                 from lib.XBMCAddonsinfo import XBMCAddonsinfoScreen
          self.session.open(XBMCAddonsinfoScreen,None)
                 

        def paintFrame(self):
                print "In paintFrame self.index, self.minentry, self.maxentry =", self.index, self.minentry, self.maxentry
#		if self.maxentry < self.index or self.index < 0:
#			return
                ifr = self.index - (10*(self.ipage-1))
		ipos = self.pos[ifr]
		print "ifr, ipos =", ifr, ipos
		self["frame"].moveTo( ipos[0], ipos[1], 1)
		self["frame"].startMoving()

        def openTest(self):
#                coming in self.ipage=1, self.shortnms, self.pics
                 print "self.ipage, self.npage =", self.ipage, self.npage
		 if self.ipage < self.npage:
                        self.maxentry = (10*self.ipage)-1
                        self.minentry = (self.ipage-1)*10
                        #self.index 0-11
                        print "self.ipage , self.minentry, self.maxentry =", self.ipage, self.minentry, self.maxentry     

                 elif self.ipage == self.npage:
                        print "self.ipage , len(self.pics) =", self.ipage, len(self.pics)
                        self.maxentry = len(self.pics) - 1
                        self.minentry = (self.ipage-1)*10
                        print "self.ipage , self.minentry, self.maxentry B=", self.ipage, self.minentry, self.maxentry   
                        i1 = 0
                        blpic = THISPLUG + "/skin/images/Blank.png"
                        while i1 < 12:
                              self["label" + str(i1+1)].setText(" ")
                              self["pixmap" + str(i1+1)].instance.setPixmapFromFile(blpic)
                              i1 = i1+1
                 print "len(self.pics) , self.minentry, self.maxentry =", len(self.pics) , self.minentry, self.maxentry        

                 i = 0
                 i1 = 0
                 self.picnum = 0
                 print "doing pixmap"
                 ln = self.maxentry - (self.minentry-1)
                 """
                 while i1 < ln:
                    idx = self.minentry + i1 
                    print "i1, idx =", i1, idx
                    
                    if os.path.exists(self.pics[idx]):
                           self.picnum = self.picnum+1
                    i1 = i1+1
                 print "self.picnum  =", self.picnum 
                 print "self.icount A=", self.icount
                 if self.icount < 15:   
                      self.icount = self.icount+1
                      if (self.picnum < 9):
                           print "pic not ready self.icount =", self.icount
                           os.system("sleep 1")
                           self.openTest()
                      else:   
                           print "pics ready"
                           self.icount = 15
                           pass
                 """
                 while i < ln:
                    idx = self.minentry + i 
                    print "i, idx =", i, idx
##################################
                    print "self.names1[idx] B=", self.names1[idx]
                    self["label" + str(i+1)].setText(self.names1[idx])
#################################

                    print "idx, self.pics[idx]", idx, self.pics[idx]
                    pic = self.pics[idx]
                    if not os.path.exists(self.pics[idx]):
                           pic = THISPLUG + "/skin/images/default.png"
                    self["pixmap" + str(i+1)].instance.setPixmapFromFile(self.pics[idx])
                    i = i+1  
                 self.index = self.minentry
                 self.paintFrame()
                           
                 
        def key_left(self):
		self.index -= 1
		if self.index < 0:
			self.index = self.maxentry
		self.paintFrame()

        def key_right(self):
		self.index += 1
		if self.index > self.maxentry:
			self.index = 0
		self.paintFrame()

        def key_up(self):
		self.index = self.index - 5
#		if self.index < 0:
#			self.index = self.maxentry
#		self.paintFrame()
                print "keyup self.index, self.minentry = ", self.index, self.minentry
		if self.index < (self.minentry):
                    if self.ipage > 1:
                        self.ipage = self.ipage - 1
                        self.openTest()
                         
		    elif self.ipage == 1:	
                        self.close()
                else:
		        self.paintFrame()



        def key_down(self):
                self.index = self.index + 5
                print "keydown self.index, self.maxentry = ", self.index, self.maxentry
		if self.index > (self.maxentry):
                    if self.ipage < self.npage:
                        self.ipage = self.ipage + 1
                        self.openTest()
                         
		    elif self.ipage == self.npage:	
                        self.index = 0
                        self.ipage = 1
                        self.openTest()

                else:
		        self.paintFrame()


#########################
###############################	
        def okClicked(self):
          #self["bild"] = startspinner()
          
          if self.keylock:
                   return     
    
          if DEBUG == 1:
                print"screen number"+str(self.curr_run)+"okClicked"
          itype = self.index
          url = self.urls1[itype]
          name = self.names1[itype]
          self.name = name
          global SELECT
#          SELECT.append(self.name)
          print"screen number"+str(self.curr_run)+"okClicked SELECT[0]=", SELECT[0]
#          SELECT[self.curr_run] = SELECT[self.curr_run-1] + " -> " + self.name
          SELECT.append(SELECT[self.curr_run] + " -> " + self.name)
          self.next_select=SELECT[self.curr_run]
          print"In XbmcPluginScreen self.curr_run =", self.curr_run
          print"In XbmcPluginScreen SELECT[self.curr_run] =", SELECT[self.curr_run]
          print"In XbmcPluginScreen SELECT =", SELECT
          self.url = url
          print"In XbmcPluginScreen self.name =", self.name
          if ('search' in self.name.lower()) or ('insert' in self.name.lower()):
                     #ShowSearchDialog(self.session)
                     print "In XbmcPluginScreen search" 
#                     from  Screens.VirtualKeyBoard import VirtualKeyBoard
                     try:
                            from Plugins.Extensions.KodiLite.lib.VirtualKeyBoard import VirtualKeyBoard
                     except:       
                            from lib.VirtualKeyBoard import VirtualKeyBoard
#                     import os
                     try:
                        txt=open('/tmp/xbmc_search.txt','r').read()
                        #os.remove("/tmp/xbmc_search.txt") 
                     except:
       
                           txt=''
                     self.name=name
                     self.url=url      
                     self.session.openWithCallback(self.searchCallback, VirtualKeyBoard, title = (_("Enter your search term(s)")), text = txt)           

          else:
            if itype == 0:
                  self.close()
            elif itype == 1 and self.curr_run==1:
              if name == "Setup":###to generate e2 e2sett.py
                d = THISPLUG + "/plugins/" + self.plug
                settings_file=d+"/resources/settings.xml"
                
                import sys,os
                if not os.path.exists(settings_file):
                   self['info'].setText(_("No settings available"))
                   return
                
                try:
                       from Plugins.Extensions.KodiLite.lib.XBMCAddonsSetup import AddonsettScreen
                except:       
                       from lib.XBMCAddonsSetup import AddonsettScreen               
                
                self.session.open(AddonsettScreen,self.plug)
                
                return
            elif itype == 2 and self.name == "Favorites":

                
                favorites_xml="/etc/KodiLite/favorites.xml"
                import os
                if not os.path.exists(favorites_xml):
                       try:   
                        if not os.path.exists("/etc/KodiLite"):
                           os.makedirs("/etc/KodiLite")
                        copyfile(THISPLUG+"/lib/defaults/favorites.xml",favorites_xml)
                       except:
                        return 
                try:        
                       from Plugins.Extensions.KodiLite.lib.favorites import getfavorites
                except:       
                       from lib.favorites import getfavorites
                favlist=getfavorites(self.plug)
                names2=[]
                urls2=[]
                names2.append("Exit")
                urls2.append("")
                for fav in favlist:
                     names2.append(fav[0])
                     urls2.append(fav[1])
                self.session.open(Favorites, names2, urls2)
                return

                                         
                  
 #         elif 'search' in self.name.lower():
          
            else:
                  self["info"].setText("Please wait ...")
##                  self.keylock=True
                  self.startSpinner()
                  self.rundef = Rundefault(self.session, name, url, self.nextrun,self.progressCallBack)
                  self.rundef.start()
                  
                  
##################################                  
#    plugin://plugin.video.youtube/kodion/search/query/?q=adele             
        def searchCallback(self,search_txt): 
          if search_txt:
               print "In XbmcPluginScreen self.url 2=", self.url
               print "In XbmcPluginScreen search_txt 1=", search_txt
               n1 = self.url.find("?", 0)
               if "plugin.video.youtube" in THISADDON:
                       self.url = self.url[:(n1+1)] + "plugin://plugin.video.youtube/kodion/search/query/?q=" + search_txt
               
               else:
#                       print "In XbmcPluginScreen search_txt 2=", search_txt
                       file=open("/tmp/xbmc_search.txt",'w')
                       file.write(search_txt)
                       file.close()
                       self["info"].setText(_("Please wait.."))
##                       self.keylock=True 
               rundef = Rundefault(self.session, self.name, self.url, 2,self.progressCallBack)
               rundef.start() 
               if rundef.error:
                      self["info"].setText(_("Error:")+rundef.error)  
#################################### 
#######
class XbmcPluginScreen(Screen):


    def __init__(self, session, name, names, urls, tmppics,curr_run):
		Screen.__init__(self, session)
		if curr_run == 1:
		       self.skinName = "KodiMenusScreenB"
		else:
		       self.skinName = "KodiMenusScreen"
		self["bild"] = startspinner()
		title = "KodiLite 3.0"
		self["title"] = Button(title)
                self.session=session
		self.list = []                
                self["menu"] = List(self.list)
                self["menu"] = RSList([])
		self["info"] = Label()
		self.curr_run=curr_run
		txt = str(SELECT[self.curr_run])
		print "In XbmcPluginScreen SELECT[self.curr_run] A=", SELECT[self.curr_run]
		self.nextrun=self.curr_run+1
	 	print "2028",txt	
		self.select=txt
		self.rundef=None
		self.plug=''
		self.keylock=False
		self.spinner_running=False
		self["info"].setText(txt)
		self["pixmap"] = Pixmap()

	        self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))		
	
                self["actions"] = NumberActionMap(["OkCancelActions", "DirectionActions", "ColorActions", "EPGSelectActions"],{
                       "upRepeated": self.up,
                       "downRepeated": self.down,
                       "up": self.up,
                       "down": self.down,
                       "info":self.showerror,
                       "left": self.left,
                       "right":self.right,
		       "red": self.cancel,
		       "green": self.okClicked,                       
                       "ok": self.okClicked,                                            
                       "cancel": self.cancel,}, -1)
                self.plug = name
                self.handle = 1
                self.names1 = []
                for nam in names:
                       if nam is None:
                               nam = "Video"
                       self.names1.append(nam)        
#                self.names1 = names
                self.urls1 = urls
                self.tmppics1 = tmppics
                if DEBUG == 1:

                       print "screen number"+str(self.curr_run)+"self.names1 =", self.names1
                       print "screen number"+str(self.curr_run)+"self.urls1 =", self.urls1
                       print "screen number"+str(self.curr_run)+"self.tmppics1 =", self.tmppics1
                self.names = []
                self.urls = []
                self.pics = []
                self.tmppics = []
                self.sett = []
                self.lines = []
                self.vidinfo = []                
                self.data = []
                self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
                system("rm /tmp/data.txt")
                self.pos = 0
                self.missed = " "
                self.shlist = " "
                self["menu"].onSelectionChanged.append(self.selection_changed)
                self.onShown.append(self.selection_changed)
                self.onLayoutFinish.append(self.action)

    def cancel(self):
                       self.close()
                       
    def startSpinner(self):
        if self.spinner_running==False:
          
          #self["bild"] = startspinner()
          
          Bilder=buildBilder()
          self["bild"].start(Bilder)
          self.spinner_running=True
          return    
    def stopSpinner(self):
       if self.spinner_running==True:
          self["bild"].stop()
          self.spinner_running=False
          self['bild'].instance.setPixmap(gPixmapPtr())
          #self["bild"].instance=None
       #self["bild"]=None
       return            
    def exit(self):
        if self.spinner_running==True:
           self.stopSpinner()
           self.keylock=False
           
           afile=open("/tmp/stopaddon","w")
           afile.write("stop execution")
           afile.close()
           
           self.progressCallBack("Finished")           
           try:self.rundef.stoprun()
           except:pass
        else:
           self.stopSpinner()   
           #self['bild']=None 
#           dellog()
           self.close()          
           
        
        #self['bild']=None
        
    def progressCallBack(self,progress):
      try:
        if progress is not None:
          if progress.startswith("Error"):
              self.keylock=False
              self["info"].setText(progress)
              self.stopSpinner() 
              return       
          if  progress=="Finished":
              self.keylock=False
              self.selection_changed()
              self.stopSpinner()
              return
           
        self["info"].setText(progress)
      except:
        pass  
        
    def selection_changed(self):
        self.keylock=False
        try:self["info"].setText(self.select)
        except:pass
    
    def showerror(self):
       try:
              from Plugins.Extensions.KodiLite.lib.XBMCAddonsinfo import XBMCAddonsinfoScreen
       except:       
              from lib.XBMCAddonsinfo import XBMCAddonsinfoScreen
       self.session.open(XBMCAddonsinfoScreen,None)
    
    def home(self):
                
                self.session.open(StartPlugin)
                self.close()

    def action(self):
                       try:
                         if os.path.exists("/tmp/netstat.txt"):
                             os.remove("/tmp/netstat.txt")
                         os.system("netstat -np > /tmp/netstat.txt && sleep 1")
                         f1=open('/tmp/netstat.txt',"r+")
                         for line in f1.readlines():
                             if '55333' in line:
                                    n1 = line.find("/", 0)
                                    if n1<0:
                                           continue
                                    n2 = line.rfind(" ", 0, n1)
                                    pid = line[(n2+1):n1]
                                    print "In Rundefault pid =", pid
                                    cmdnet = "kill " + str(pid)
                                    self.container = eConsoleAppContainer()
#                                    self.container.appClosed.append(self.action)
#                                    self.container.dataAvail.append(self.dataAvail)
                                    self.container.execute(cmdnet)

                       except:
                                    pass

                       if config.plugins.kodiplug.thumb.value == "False":
		                picthumb = THISPLUG + "/skin/images/default.png"
#                                self["pixmap"].instance.setPixmapFromFile(picthumb)
#                        print "In XbmcPluginScreen self.names1 =", self.names1
                       showlist(self.names1, self["menu"])
#                        self.selection_changed()
                
    def up(self):
                if self.keylock:
                   return
                self.pos = up(self.names1, self.tmppics1, self.pos, self["menu"], self["pixmap"])

    def down(self):
                if self.keylock:
                   return    
    
                self.pos = down(self.names1, self.tmppics1, self.pos, self["menu"], self["pixmap"])
                
    def left(self):
                if self.keylock:
                   return    
    
                self.pos = left(self.names1, self.tmppics1, self.pos, self["menu"], self["pixmap"])

    def right(self):
                if self.keylock:
                   return    
                self.pos = right(self.names1, self.tmppics1, self.pos, self["menu"], self["pixmap"])

    def cancelX(self):
                self.keylock=False
                afile=open("/tmp/stopaddon","w")
                afile.write("stop execution")
                afile.close()
                self.close()  
	
    def keyRight(self):
                if self.keylock:
                   return     
    
		self["text"].right()


    def vidError(self, reply):
                return

    def okClicked(self):
          #self["bild"] = startspinner()

          if self.keylock:
                   return     
    
          if DEBUG == 1:
                print "screen number"+str(self.curr_run)+"okClicked"
          itype = self["menu"].getSelectionIndex()
          url = self.urls1[itype]
          name = self.names1[itype]
          self.name = name
          global SELECT
#          SELECT.append(self.name)
          print "screen number"+str(self.curr_run)+"okClicked SELECT[0]=", SELECT[0]
#          SELECT[self.curr_run] = SELECT[self.curr_run-1] + " -> " + self.name
          SELECT.append(SELECT[self.curr_run] + " -> " + self.name)
          self.next_select=SELECT[self.curr_run]
          print "In XbmcPluginScreen self.curr_run =", self.curr_run
          print "In XbmcPluginScreen SELECT[self.curr_run] =", SELECT[self.curr_run]
          print "In XbmcPluginScreen SELECT =", SELECT
          self.url = url
          self.url = url
          print "In XbmcPluginScreen self.name =", self.name
          if ('search' in self.name.lower()) or ('insert' in self.name.lower()):
                     #ShowSearchDialog(self.session)
                     print "In XbmcPluginScreen search" 
#                     from  Screens.VirtualKeyBoard import VirtualKeyBoard
                     try:
                            from Plugins.Extensions.KodiLite.lib.VirtualKeyBoard import VirtualKeyBoard
                     except:       
                            from lib.VirtualKeyBoard import VirtualKeyBoard
#                     import os
                     try:
                        txt=open('/tmp/xbmc_search.txt','r').read()
                        #os.remove("/tmp/xbmc_search.txt") 
                     except:
       
                           txt=''
                     self.name=name
                     self.url=url      
                     self.session.openWithCallback(self.searchCallback, VirtualKeyBoard, title = (_("Enter your search term(s)")), text = txt)           

          else:
            if itype == 0:
                  self.close()
            elif itype == 1 and self.curr_run==1:
              if name == "Setup":###to generate e2 e2sett.py
                d = THISPLUG + "/plugins/" + self.plug
                settings_file=d+"/resources/settings.xml"
                
                import sys,os
                if not os.path.exists(settings_file):
                   self['info'].setText(_("No settings available"))
                   return
                
                try:
                       from Plugins.Extensions.KodiLite.lib.XBMCAddonsSetup import AddonsettScreen
                except:
                       from lib.VirtualKeyBoard import VirtualKeyBoard
                self.session.open(AddonsettScreen,self.plug)
                
                return
            elif itype == 2 and self.name == "Favorites":

                
                favorites_xml="/etc/KodiLite/favorites.xml"
                import os
                if not os.path.exists(favorites_xml):
                       try:   
                        if not os.path.exists("/etc/KodiLite"):
                           os.makedirs("/etc/KodiLite")
                        copyfile(THISPLUG+"/lib/defaults/favorites.xml",favorites_xml)
                       except:
                        return 
                try:        
                       from Plugins.Extensions.KodiLite.lib.favorites import getfavorites
                except:       
                       from lib.favorites import getfavorites
                favlist=getfavorites(self.plug)
                names2=[]
                urls2=[]
                names2.append("Exit")
                urls2.append("")
                for fav in favlist:
                     names2.append(fav[0])
                     urls2.append(fav[1])
                self.session.open(Favorites, names2, urls2)
                return

                                         
                  
 #         elif 'search' in self.name.lower():
          
            else:
                  self["info"].setText("Please wait..")
                  self.keylock=True
                  self.startSpinner()
#                  dellog()
                  self.rundef = Rundefault(self.session, name, url, self.nextrun,self.progressCallBack)
                  self.rundef.start()
                  
                  
##################################                  
#    plugin://plugin.video.youtube/kodion/search/query/?q=adele             
    def searchCallback(self,search_txt): 
          if search_txt:
               print "In XbmcPluginScreen self.url 2=", self.url
               print "In XbmcPluginScreen search_txt 1=", search_txt
               n1 = self.url.find("?", 0)
               if "plugin.video.youtube" in THISADDON:
                       self.url = self.url[:(n1+1)] + "plugin://plugin.video.youtube/kodion/search/query/?q=" + search_txt
               
               else:
#                       print "In XbmcPluginScreen search_txt 2=", search_txt
                       file=open("/tmp/xbmc_search.txt",'w')
                       file.write(search_txt)
                       file.close()
                       self["info"].setText(_("Please wait.."))
                       self.keylock=True 
               rundef = Rundefault(self.session, self.name, self.url, 2,self.progressCallBack)
               rundef.start() 
               if rundef.error:
                      self["info"].setText(_("Error:")+rundef.error)  
####################################                                 

class Favorites(Screen): 

    def __init__(self, session, names, urls):
		Screen.__init__(self, session)
		self.skinName = "Favorites"
		title = (_("Favorites"))
		self["title"] = Button(title)
#############################################                
		self.list = []                
#                self["list"] = List(self.list)
#                self["list"] = RSList([])
                self["menu"] = List(self.list)
                self["menu"] = RSList([])
#############################################
		self["info"] = Label()
		self["pixmap"] = Pixmap()
		self["key_red"] = Button(_("Exit"))
		self["key_green"] = Button(_("Select"))
		self["key_yellow"] = Button(_("Delete favorite"))
#		self["key_blue"] = Button(_("More addons"))
                self["actions"] = NumberActionMap(["OkCancelActions", "ColorActions"],{
                       "red": self.close,
		       "green": self.okClicked,
		       "yellow": self.delete,
#		       "blue": self.addon,
                       "ok": self.okClicked,
                       "cancel": self.close,}, -1)

                self.names = names
                self.urls = urls
	        self.onLayoutFinish.append(self.source)
	        
        
    def source(self):	        
                pic = THISPLUG + "/skin/images/default.png"
                self["pixmap"].instance.setPixmapFromFile(pic)
                showlist(self.names, self["menu"])
    

    def okClicked(self):
           try:
	        idx = self["menu"].getSelectionIndex()
	        desc = " "
	        name = self.names[idx]
                url = self.urls[idx]
                self.session.open(Playvid, name, url, desc)
           except:
                self["info"].setText(_("No item selected !")) 
                
    def delete(self):
           import xml.etree.ElementTree as ET
           xmlfile = "/etc/KodiLite/favorites.xml"
           tree = ET.parse(xmlfile)

           idx = self["menu"].getSelectionIndex()
           name = self.names[idx]
           root = tree.getroot()
                
           i=0
           for addon in root.iter('addon'):   
                    for media in addon.iter('media'):
                            title = media.get('title')
                            if title == name:
                                   addon.remove(media)
                            tree.write(xmlfile)           
           self.close()

####################################
####################################
class StartPlugin_mainmenu(Screen):
    def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = "xbmc4A"
                title = (_("Addons"))
                print "In StartPlugin_mainmenu 1"
                self.setTitle(title)
                self.session=session
                self["bild"] = startspinner()
                self.spinner_running=False
                self["label1"] = StaticText("")
		self["label2"] = StaticText("")
		self["label20"] = StaticText("")
		self["label3"] = StaticText("")
		self["label30"] = StaticText("")
		self["label4"] = StaticText("")
		self["info"] = Label()
		global newstext
		news = newstext
		self.cancel=False
		self.data1=''
		self.keylock=False
		self.progress=(_(" "))
#		print "In StartPlugin_mainmenu newstext =", newstext

                self["info"].setText(" ")

		self["pixmap"] = Pixmap()
		self["pixmap1"] = Pixmap()
		self.list = []                
                self["menu"] = List(self.list)
                self["menu"] = RSList([])
#		self["info"] = Label()
		self["pixmap"] = Pixmap()
		self.progress=(_(" "))
		self["key_red"] = Button(_("Delete addons"))
		self["key_green"] = Button(_("Install addons"))
		self["key_yellow"] = Button(_("Config"))
		self["key_blue"] = Button(_("Tips"))
                system("rm /tmp/select.txt")
                
                
                self["menu"].onSelectionChanged.append(self.selection_changed)
                self.onShown.append(self.selection_changed)                
                self["actions"] = NumberActionMap(["OkCancelActions", "ColorActions", "DirectionActions","EPGSelectActions"],{
                       "upRepeated": self.up,
                       "downRepeated": self.down,
                       "up": self.up,
                       "down": self.down,
                       "left": self.left,
                       "right":self.right,
                       "red": self.delete,
		       "green": self.addon,
		       "yellow": self.conf,
		       "blue": self.close,
                       "ok": self.okClicked,
                       "info":self.close,                     
                       "cancel": self.exit,}, -1)
########################
                self.updateTimer = eTimer()
                try:
                      self.updateTimer_conn = self.updateTimer.timeout.connect(self.updateStatus)
                except AttributeError:
                      self.updateTimer.callback.append(self.updateStatus)
                self.timecount = 0
                ncount = config.plugins.kodiplug.wait.value 
                nc = int(ncount)*1000
                timeint = int(float(nc/120))
                print "timeint =", timeint
                self.timeint = 1000
                self.nct = int(float(nc/self.timeint))
                print "self.nct =", self.nct
########################                
                self.pos = 0
                self.num = 0
                self.urls = []
                self.names = []
                self.shortnms = []
                self.data = []
                self.missed = " "
                self.shlist = " "
                print "StartPlugin_mainmenu 2"
                self.onLayoutFinish.append(self.listplugs)
                        
    def exit(self):          
           self.close()          

    def delete(self):
                self.session.openWithCallback(self.listplugs, DelAdd)           

    def addon(self):
                self.session.openWithCallback(self.listplugs, Getaddons)           

            
    def conf(self):            
          self.session.open(XbmcConfigScreen)

    def selection_changed(self):
      self.keylock=False
      
      
      try:
        pos = self["menu"].getSelectionIndex()
        name = self.names[pos]    
      except:
        pass

    def up(self):
         if self.keylock:
                   return
         dedesc = " "
         endesc = " "
         itdesc = " "
         self["menu"].up()
         self.pos = self.pos - 1
         num = len(self.names)
         if self.pos == -1:
                self.pos = num - 1
                self["menu"].moveToIndex(self.pos) 
         name = self.names[self.pos]
         if self.pos > 0:
                pic1 = THISPLUG + "/plugins/" + name + "/icon.png"
                self["pixmap1"].instance.setPixmapFromFile(pic1)
                pname, version, prov, desc= self.getinfo(name)
                
                self["label1"].setText(pname)
                self["label20"].setText("Version :")
                self["label2"].setText(version)
                self["label30"].setText("Provider :")
                self["label3"].setText(prov)
                self["label4"].setText(desc)
         else:      
                if self.pos == 0:
                       if config.plugins.kodiplug.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitL.png"
                       else:
                                pic1 = THISPLUG + "/skin/images/Exit.png"
                       self["pixmap1"].instance.setPixmapFromFile(pic1)
                self["label1"].setText(" ")
                self["label20"].setText(" ")
                self["label2"].setText(" ")
                self["label30"].setText(" ")
                self["label3"].setText(" ")
                self["label4"].setText(" ")  
                
    def down(self):
         if self.keylock:
                   return    
    
         dedesc = " "
         endesc = " "
         itdesc = " "

         self["menu"].down()
         self.pos = self.pos + 1
         num = len(self.names)
         if self.pos == num:
                self.pos = 0
                self["menu"].moveToIndex(0)  
         name = self.names[self.pos]
         if DEBUG == 1:
                print "name =", name
         if self.pos > 0:
                pic1 = THISPLUG + "/plugins/" + name + "/icon.png"
                self["pixmap1"].instance.setPixmapFromFile(pic1)
                if DEBUG == 1:
                       print "name B=", name
                pname, version, prov, desc= self.getinfo(name)

                self["label1"].setText(pname)
                self["label20"].setText("Version :")
                self["label2"].setText(version)
                self["label30"].setText("Provider :")
                self["label3"].setText(prov)
                desc = desc.replace(":", "-")
                self["label4"].setText(desc)
         else:      
                if self.pos == 0:
                       if config.plugins.kodiplug.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitL.png"
                       else:
                                pic1 = THISPLUG + "/skin/images/Exit.png"
                       self["pixmap1"].instance.setPixmapFromFile(pic1)
                self["label1"].setText(" ")
                self["label20"].setText(" ")
                self["label2"].setText(" ")
                self["label30"].setText(" ")
                self["label3"].setText(" ")
                self["label4"].setText(" ")  
                
    def left(self):
         if self.keylock:
                   return
         self["menu"].pageUp()
         self.pos = self["menu"].getSelectionIndex()
         name = self.names[self.pos]
         if self.pos > 0:
                pic1 = THISPLUG + "/plugins/" + name + "/icon.png"
                self["pixmap1"].instance.setPixmapFromFile(pic1)
                pname, version, prov, desc = self.getinfo(name)
                
                self["label1"].setText(pname)
                self["label20"].setText("Version :")
                self["label2"].setText(version)
                self["label30"].setText("Provider :")
                self["label3"].setText(prov)
                self["label4"].setText(desc)
         else:      
                if self.pos == 0:
                       if config.plugins.kodiplug.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitL.png"
                       else:
                                pic1 = THISPLUG + "/skin/images/Exit.png"
                       self["pixmap1"].instance.setPixmapFromFile(pic1)
                self["label1"].setText(" ")
                self["label20"].setText(" ")
                self["label2"].setText(" ")
                self["label30"].setText(" ")
                self["label3"].setText(" ")
                self["label4"].setText(" ")                        
                self.error=None
    def right(self):
         if self.keylock:
                   return
         self["menu"].pageDown()
         self.pos = self["menu"].getSelectionIndex()
         name = self.names[self.pos]
         if self.pos > 0:
                pic1 = THISPLUG + "/plugins/" + name + "/icon.png"
                self["pixmap1"].instance.setPixmapFromFile(pic1)
                pname, version, prov, desc = self.getinfo(name)
                
                self["label1"].setText(pname)
                self["label20"].setText("Version :")
                self["label2"].setText(version)
                self["label30"].setText("Provider :")
                self["label3"].setText(prov)
                self["label4"].setText(desc)
         else:      
                if self.pos == 0:
                       if config.plugins.kodiplug.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitL.png"
                       else:
                                pic1 = THISPLUG + "/skin/images/Exit.png"
                       self["pixmap"].instance.setPixmapFromFile(pic1)
                self["label1"].setText(" ")
                self["label20"].setText(" ")
                self["label2"].setText(" ")
                self["label30"].setText(" ")
                self["label3"].setText(" ")
                self["label4"].setText(" ") 
                                      

    def getinfo(self, name):            
                xfile = THISPLUG + "/plugins/" + name + "/addon.xml"
                dedesc = ' '
                endesc = ' '
                itdesc = ' '
                try:tree = xml.etree.cElementTree.parse(xfile)
                except: return "", "", "", ""
                root = tree.getroot()
                pname = str(root.get('name'))
                version = str(root.get('version'))
                prov = str(root.get('provider-name'))
                try:
                    for description in root.iter('description'):
                        lang = description.get('lang')
                        desc = str(description.text)
                        if lang == "de":
                              dedesc = desc
                        elif lang == "it":
                              itdesc = desc      
                        else:      
                              endesc = desc
                except:
                    for description in root.getiterator('description'):
                        lang = description.get('lang')
                        desc = str(description.text)
                        if lang == "de":
                              dedesc = desc
                        elif lang == "it":
                              itdesc = desc      
                        else:      
                              endesc = desc
                              
                if config.osd.language.value == "de_DE":
                              desc2 = dedesc
                elif config.osd.language.value == "it_IT":
                              desc2 = itdesc                               
                else:
                              desc2 = endesc
                if desc2 == ' ':
                              desc2 = endesc               
                              
                return pname, version, prov, desc2
                
    def listplugs(self):
                print "In listplugs 1"
                self.urls = []
                self.names = []
                self.shortnms = []
                path = THISPLUG + "/plugins"
                self.names.append("Exit")
                self.shortnms.append("Exit")
                self.urls.append("0")
                i = 1
                for name in os.listdir(path):
                   
                    if "__init__" in name:
                       continue

                    if "plugin." not in name:
                       continue
                    elif "plugin.video.select" in name:
                       continue   
                    else:      
                              print "config.ParentalControl.configured.value =", config.ParentalControl.configured.value
                              print "In listplugs 2"
                              self.names.append(name)
                              name1 = name[13:]
                              self.shortnms.append(name1) 
                              self.urls.append(i)
                              i = i+1
                self.num = i
                showlist(self.shortnms, self["menu"])
##################################  
##################################               
    def checkUpd(self):           
                print "In checkUpd self.name = ", self.name
                tfile = THISPLUG + "/plugins/" + self.name + "/addon.xml"
                f = open(tfile, "r")       
                txt = f.read()
                print "In checkUpd txt = ", txt
                n1 = txt.find('<addon', 0)
                n11 = txt.find('id', n1)
                n2 = txt.find("version", n11)
                n3 = txt.find('"', n2)
                n4 = txt.find('"', (n3+2))
                version = txt[(n3+1):n4]
                print "In checkUpd version = ", version
                f.close()
                try:
                       file1 = THISPLUG + "/adlist.txt"
                       f1=open(file1,"r+")
                       fpage = f1.read()
                except:       
                       fpage = " "
                
                self.fpage = fpage
#                tfile2 = THISPLUG + "/adlist.txt"      
#                f2 = open(tfile2, "r")
#                fpage = f2.read()
                lines = fpage.splitlines()
                
#                f2.close()
                nlist = 0
                for line in lines: 
                       print "In checkUpd line =", line
                       print "In checkUpd self.name B=", self.name   
                       if line.startswith("#####"):
                             continue
                       elif "###" not in line:
                             continue  
#                       elif (not self.name in line) and (not "pelisalacarta" in line) and (not "tvalacarta" in line):
                       elif not self.name in line:
                             continue
                       else:        
                             nlist = 1 #addon in adlist.txt    
                             print "In checkUpd line B=", line
                             print "In checkUpd self.name c=", self.name   
                             items = line.split("###")
                             n = len(items)
                             print "In checkUpd items =", items
                             name = items[0]
                             url1 = items[1]
                             if items[2] != '': 
                                   url2 = items[2]
                                   self.checkLine(line, version) 
                                   break
                             else:      
                                   print "In checkUpd going in self.okClicked2 "
                                   self.okClicked2()

                if nlist == 0: # user added addon
                       self.okClicked2()


    def checkLine(self, line, version):
           print "In checkLine line =", line
           items = line.split("###")
           print "In checkLine items =", items
           name = items[0]
           url1 = items[1]
           url2 = items[2]
           if url2 == '':
                self.okClicked2()
           else:       
                url2 = items[2]
                n2 = url1.find(".zip", 0)
                n3 = url1.rfind(name, 0, n2)
                n4 = n3 + len(name) + 1
                url0 = url1[:n4] 
                print  "url0 =", url0
                xurl = url2
                xdest = "/tmp/down.txt"
                self.line = line
                self.version = version
                self.name = name
                self.url1 = url1
                self.url2 = url2
                self.url0 = url0 
#                fpage = urlopen(url2).read()
                downloadPage(xurl, xdest).addCallback(self.getdown).addErrback(self.showError)

    def showError(self, error):
                print "ERROR :", error

    def getdown(self, fplug):                
                fpage = open("/tmp/down.txt", "r").read()
                
                if self.url2.endswith(".xml"):
                        rx = 'addon id="' + self.name + '".*?version="(.*?)"'
                else:
                        rx = self.name + '-(.*?).zip'
                match = re.compile(rx,re.DOTALL).findall(fpage)
                print  "match =", match
                if len(match) == 0:
                        rx = self.name + '_(.*?).zip'
                        match = re.compile(rx,re.DOTALL).findall(fpage)
                        print  "match 2=", match
                try:        
                        latest = findmax(match)
                except:        
                        latest = max(match) 
                latest = latest.replace("%7E", "~")                       
                print  "latest =", latest
                print  "self.version =", self.version
                if latest != self.version:
#                    if not self.url1.endswith(".zip"):  #datadirectory zip false
#                        self.session.open(GetaddonsA3, self.line)           
#                    else:
                        self.xurl = self.url0 + latest + ".zip"
                        print  "self.xurl =", self.xurl
                        txt = _("New version ") + latest + _(" is available. Update Now ?")
                        print  "txt =", txt
                        self.session.openWithCallback(self.do_update, MessageBox, txt, type = 0)
                else:
                        self.okClicked2()
                               

    def do_update(self, answer):
                if answer is None:
                       self.okClicked2()
                else:
                       if answer is False:
                               self.okClicked2()
                       else:
                               xurl = self.xurl
                               print  "self.xurl=", self.xurl
                               xdest = "/tmp/plug.zip"
	                       downloadPage(xurl, xdest).addCallback(self.install).addErrback(self.showError)

    def install(self, fplug):
                fdest = THISPLUG + "/plugins"
                addon = THISPLUG + "/plugins/" + self.name
                cmd1 = "rm -rf '" + addon + "'" 
                cmd2 = " unzip -o -q '/tmp/plug.zip' -d '" + fdest + "'"
                cmd3 = " cp -f '" + THISPLUG + "/xpath.py' " + addon 
                cmd = cmd1 + " && " + cmd2 + " && " + cmd3
                print "cmd =", cmd
                title = _("Installing ") + self.name
#                self.session.open(Console,_(title),[cmd])
                print "self.session 1=", self.session
                self.session.openWithCallback(self.checkName,Console,_(title),[cmd])
                
    def checkName(self):
                path = THISPLUG + "/plugins"
                for name in os.listdir(path):
                       print "name =", name
                       if "plugin" not in name:
                           if "__init" in name:
                               continue
                           elif "E2" in name:
                               self.close()
                           else:    
                               newname = "plugin.video." + name
                               cmd = "mv " + path + "/" + name + " " + path + "/" + newname + " &"
                               os.system(cmd) 
                       if "-master" in name:
                               newname = name.replace("-master", "")
                               cmd = "mv " + path + "/" + name + " " + path + "/" + newname + " &"
                               os.system(cmd) 
                       if ("pelisalacarta" in name) or ("tvalacarta" in name):
                               cmd = "rm '" + path + "/" + name + "/fixed2'"        
                               os.system(cmd)
                               
#                self.close()
                self.checkfix()

    def checkfix(self):
                url ="http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Fix/list.txt"
                self.fixlist = urlopen(url).read()
                print "self.fixlist =", self.fixlist
                print "self.name =", self.name
                if self.name in self.fixlist:
                        plug = self.name + "-fix.1.0.0.zip"
                        xurl = "http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Fix/" + plug
                        print "xurl =", xurl
                        xdest = "/tmp/plug.zip"
	                downloadPage(xurl, xdest).addCallback(self.installB).addErrback(self.showError)
                else:
                        print "No fix to install"
                        self.close()
                                      
    def installB(self, fplug):
                fdest = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins"
                cmd = "unzip -o -q '/tmp/plug.zip' -d " + fdest
                
                print "In installB cmd =", cmd
                title = (_("Installing addon fix"))
                os.system(cmd)
                self.close()






################################## 
    def checkImports(self):
                xmfile = THISPLUG+"/plugins/"+self.id+"/resources/settings.xml"
                tmpfile = THISPLUG+"/ofile.xml"
                if os.path.exists(xmfile):
                       f = open(xmfile, "r")
                       f1 = open(tmpfile, "w")
                       ftxt = f.read()
                       ftxt = ftxt.decode("ISO-8859-1")
                       f1.write(ftxt)
                       f.close()
                       f1.close()
                       print "Here in checkImports copying /tmp/ofile.xml to ", xmfile 
                       cmd = "cp -f " + tmpfile + " " + xmfile + " && rm " + tmpfile
                       print "Here in checkImports cmd ", cmd 
                       os.system(cmd)
                


                self.shlist = " "
                self.plugins=" "
                scripts = THISPLUG + "/scripts"
                for name in os.listdir(scripts):
#                       if "script." in name:
                              self.shlist = self.shlist + name + " "
                              
                plugins = THISPLUG + "/plugins"
                for name in os.listdir(plugins):
#                       if "script." in name:
                              self.plugins = self.plugins + name + " "                              
                              
                import xbmcaddon
                try:
                  sys.argv[0]=THISPLUG+"/plugins/"+self.id+"/default.py"
                except:
                  import sys
                  sys.argv=[]
                  sys.argv.append(THISPLUG+"/plugins/"+self.id+"/default.py")
                update_xbmc_text(self.id)                  
                addon = xbmcaddon.Addon(self.id)
                path = addon.getAddonInfo("path")
                print "In checkImports self.id =", self.id 
                print "In checkImports path =", path            
                xfile = path + "/addon.xml" 
                tree = xml.etree.cElementTree.parse(xfile)
                root = tree.getroot()
                self.missed = ""
                i = 0
                try:
                  for x in root.iter('import'):
                    addon = x.get('addon') + " " #to get xbmcswift not xbmcswift2
                    if "xbmc.python" in addon:
                          continue
                    if "xbmc.addon" in addon:
                          continue   
                    if "repository." in addon:
                          continue
                    if "artwork" in addon:
                          continue               
                    if addon in self.shlist or addon in self.plugins:
                          continue
                    self.missed = self.missed + " " + addon
                    i = 1                 
                except:
                  for x in root.getiterator('import'):
                    addon = x.get('addon') + " "
                    if "xbmc.python" in addon:
                          continue
                    if "xbmc.addon" in addon:
                          continue          
                    if addon in self.shlist or addon in self.plugins:
                          continue
                    self.missed = self.missed + " " + addon
                    i = 1 
                if i == 1:
#                    self.session.openWithCallback(self.error, MessageBox, self.missed, type = 3, timeout = 20)
                    self.download(self.missed)

                else:
                    arg = "'" + THISPLUG.strip() + "/plugins/" + self.name.strip() + "/default.py' '1' ''"
                    self.arg = arg
                    self.stream()    

    def download(self, missed):
          print "missed 1= [", missed
          self.missed = missed
          url ="http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Script-modules/kodi/list.txt"
          self.sclist = urlopen(url).read()
          print "self.sclist =", self.sclist
          url1 ="http://mirrors.kodi.tv/addons/jarvis/addons.xml"
          getPage(url1).addCallback(self.gotPage).addErrback(self.getfeedError)
          
    def getfeedError(self, error=""):
		error = str(error)
		print "Download error =", error

    def gotPage(self, html):
          fdlist = html
          print "fdlist =", fdlist
          missed = self.missed
          print "missed = [", missed
          sclist = self.sclist
          items = missed.split(" ") 
          print "items =", items
          commands = []   
          for item in items:
             print "In download item =", item
             sitem = 'addon id="' + item
             n1 = fdlist.find(sitem, 0)
             if n1 < 0:
                  if item in sclist:
                             plug = item + ".zip"
                             fdest = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/scripts"
                             dest = "/tmp/" + plug
                             cmd1 = "wget -O '" + dest + "' 'http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Script-modules/kodi/" + plug + "'"
                             cmd2 = "unzip -o -q '/tmp/" + plug + "' -d " + fdest
                             cmd = cmd1 + " && " + cmd2
                             commands.append(cmd)
                  else:
                             txt = item + " not found"
                             self["info"].setText(txt)
#                             return

             if n1 > -1:
               n2 = fdlist.find('version="', n1)
               n3 = fdlist.find('"', (n2+10))
               ver = fdlist[(n2+9):n3]      
               itemurl = "http://mirrors.kodi.tv/addons/jarvis/" + item + "/" + item + "-" + ver + ".zip"
             
               if "script." in item:
                             plug = item
                             fdest = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/scripts"
                             dest = "/tmp/" + plug
                             cmd1 = "wget -O '" + dest + "' '" + itemurl + "'"
                             cmd2 = "unzip -o -q '/tmp/" + plug + "' -d " + fdest
                             cmd = cmd1 + " && " + cmd2
                             commands.append(cmd)
#                             print "cmd Sc=", cmd
               elif "plugin.video" in item:
                             plug = item
                             fdest = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins"
                             dest = "/tmp/" + plug
                             cmd1 = "wget -O '" + dest + "' '" + itemurl + "'"
                             cmd2 = "unzip -o -q '/tmp/" + plug + "' -d " + fdest
                             cmd = cmd1 + " && " + cmd2
                             commands.append(cmd)
#                             print "cmd Ad=", cmd
          title = (_("Installing addons ")) + missed
          print "commands= ", commands
          self.session.open(Console,_(title), commands)
          self.close()
#mmmmmmmmmmmmmmmmmmmmmmmmmm            
##################################

    def okClicked(self):
                if self.keylock:
                   return    
    
                print "In StartPlugin_mainmenu okClicked"
                idx = self["menu"].getSelectionIndex()
                if DEBUG == 1:
                       print "idx =", idx
                if idx == 0:
                       self.close()
#                elif "Get more" in self.names[idx]:       
#                       self.addon()
                else:       
                       self.name = self.names[idx]
                       self.nameplug = self.name
                       print "In StartPlugin_mainmenu okClicked B self.name =", self.name
########################################
                       if self.name.endswith("E2"):
                               self.runE2plug(self.name) 
                       else:        
                               self.checkUpd()

    def okClicked2(self):
############################################                           
                       global SELECT
                       SELECT=[]
                       SELECT.append(self.name)
                       SELECT.append("1")
                       SELECT[1] = self.name
                       print "In StartPlugin_mainmenu SELECT[0] =", SELECT[1]
		       self.id = self.nameplug
		       self.name = self.nameplug
		       f = open("/tmp/kodiplug.txt", "w")
		       tplug = self.id + "\n"
		       f.write(tplug)
		       f.close()
		       self.defaultpy()
		       #self.changepy()
		       self.checkImports()
#		       arg = "'" + THISPLUG.strip() + "/plugins/" + self.name.strip() + "/default.py' '1' ''"
#                       self.arg = arg
#                       self.stream() 
                       
###############################
    def defaultpy(self):
        global THISADDON
        THISADDON = THISPLUG + "/plugins/" + self.id
        print "In defaultpy THISADDON =", THISADDON
        dpath = THISADDON + "/default.py"
        if not os.path.exists(dpath):
               fmod = self.findmod()
               cmd = "mv " + THISADDON + "/" + fmod + " " + THISADDON + "/default.py"
               print "cmd =", cmd
               os.system(cmd)

        tfile = THISPLUG + "/added.txt"
        f = open(tfile, 'r')
        addtxt = f.read()
        f.close()

        fpath1 = THISPLUG + "/plugins/" + self.id 
        fpath2 = fpath1 + "/fixed2"
        if fileExists(fpath2):
            addtxt2 = "\nf = file('/tmp/e.log', 'a')\nsys.stdout = f\n"
            fpath = fpath1 + "/default.py"
            f = open(fpath, 'r')
            deftxt = f.read()
            f.close()
            if addtxt2 in deftxt:
               f1 = open('/tmp/default.txt', 'w')
               icount =0
               deftxt3 = deftxt.replace(addtxt2, "\n")
               f1.write(deftxt3)
               
               f.close()
               f1.close()
               cmd = "rm " + fpath + " && cp /tmp/default.txt " + fpath  
               os.system(cmd)
              
            else:
               pass  
               
        else:                   
            fpath = fpath1 + "/default.py"
            f = open(fpath, 'r')
            deftxt = f.read()
            print "In defaultpy deftxt =", deftxt
            x = ord(deftxt[0])
            x1 = ord(deftxt[1])
            x2 = ord(deftxt[2])
            x3 = ord(deftxt[3])
            xm = max([x,x1,x2,x3]) 
            print "In defaultpy nonasci xm =",  xm
            if xm > 127:
                   n1 = deftxt.find("#", 0)
                   if n1 == -1:
                          n1 = 1000
                   n2 = deftxt.find("import", 0)
                   if n2 == -1:
                          n2 = 1000
                   n3 = deftxt.find("from", 0)
                   if n3 == -1:
                          n3 = 1000
                   nmin = min(n1, n2, n3)
                   print "nmin =", nmin
                   deftxt = deftxt[nmin:]

            print "In defaultpy deftxt B=", deftxt
            data = []
            data = deftxt.splitlines()
            f.close()            
            if addtxt not in deftxt:
               cmdrm = "rm " + fpath1 + "/xpath.py"
               os.system(cmdrm)
               f1 = open('/tmp/default.txt', 'w')
               icount =0
#               f = open(fpath, 'r')
               for line in data:
                   line = line.decode("ISO-8859-1")
                   line = line + "\n"
                   if not (line.startswith("#")):
                       if icount==0:
                          f1.write(addtxt)
                          icount = 1
                       else:
                          pass   
                   f1.write(line)
               f.close()
               f1.close()
               cmd = "rm " + fpath + " && cp /tmp/default.txt " + fpath  
               os.system(cmd)
            cmd1 = "touch " + fpath2
            os.system(cmd1)


    def findmod(self):
                xfile = THISADDON + "/addon.xml"
                print "In plugin-py findmod xfile =", xfile
                f = open(xfile, "r")
                ftext = f.read()
                n1 = ftext.find("<extension", 0)
                n2 = ftext.find("library", n1)
                n3 = ftext.find('"', n2)
                n4 = ftext.find('"', (n3+1))
                fmod = ftext[(n3+1):n4]
                print "Newmod =", fmod
                return fmod



###############################
    def stream(self):

                self.picfold = config.plugins.kodiplug.cachefold.value+"/xbmc/pic"
                self.tmpfold = config.plugins.kodiplug.cachefold.value+"/xbmc/tmp"
                cmd = "rm " + self.tmpfold + "/*"
                system(cmd)
                system("rm /tmp/data.txt")
                system("rm /tmp/data.txt")
                system("rm /tmp/vidinfo.txt")
                system("rm /tmp/type.txt")
                if DEBUG == 1:
                       print "DEBUG =", DEBUG
                if DEBUG == 1:
                       print "StartPlugin_mainmenu self.arg =", self.arg
                cmd = "python " + self.arg
                cmd = cmd.replace("&", "\\&")
#                afile = file("/tmp/test.txt","w")       
#                afile.write("going in default.py")
#                afile.write(cmd)
                if DEBUG == 1:
                       print "going in default-py Now =", datetime.datetime.now()
#                system(cmd)
#######################################
                fdef ='default'# NEWDEFPY[:-3]
                arg1 = THISPLUG + "/plugins/" + self.name + "/default.py"
                arg2 = "1"
                arg3 = ""
                arg4=config.plugins.kodiplug.cachefold.value
                sys.argv = [arg1,arg2, arg3,arg4]
                d = THISPLUG + "/plugins/" + self.name
                global THISADDON
                THISADDON = d
                self.plugin_id=self.name
                
                
                sys.argv = [arg1,arg2, arg3,arg4]
                d = THISADDON
                
#                dellog()       
                ###############################
                xpath_file=THISPLUG+"/plugins/"+self.name+"/xpath.py"
                fixed2_file=THISPLUG+"/plugins/"+self.name+"/fixed2"
                default_file=THISPLUG+"/plugins/"+self.name+"/default.py"
#                if not os.path.exists(xpath_file): 
                os.system("cp -f "+THISPLUG+"/lib/xpath.py "+xpath_file)
                cmd='python '+default_file+' 1 '+"'"+arg3+"'" 
                print cmd 
#######################
                            
                    
                if os.path.exists("/tmp/data.txt"):
                   os.remove("/tmp/data.txt")                
                timen = time.time() 
                global NTIME 
                NTIME = timen
                timenow = timen - NTIME
                print "In StartPlugin_mainmenu timenow", timenow
                print "In StartPlugin_mainmenu cmd =", cmd
                self.dtext = " "
                self.lastcmd = cmd
                global LAST
                LAST = self.lastcmd
                log("\n"+cmd)
                self.p = os.popen(cmd)
                self.timecount = 0
                self.updateTimer.start(self.timeint)

              
    def updateStatus(self):
         ncount = config.plugins.kodiplug.wait.value
#         nct = int(ncount)/4
         self.timecount = self.timecount + 1
         print "In StartPlugin_mainmenu updateStatus self.timecount =", self.timecount
         self.dtext = self.p.read()
         print "In StartPlugin_mainmenu updateStatus self.dtext =", self.dtext
         global dtext1
         if len(self.dtext) > 0:
                dtext1 = dtext1 + self.dtext
         if "data B" in self.dtext:
                self.updateTimer.stop()
                self.action(" ")
         print "In StartPlugin_mainmenu self.timecount =", self.timecount 
         if self.timecount > self.nct:     
              self.updateTimer.stop()
              f1=open("/tmp/e.log","a")
#              f1.write(dtext1)
              f1.close()
              self.action(" ")
    
    def action(self,retval):
    
                            
            self.keylock=False
            self.names2 = []
            self.urls2 = []
            self.pics2 = []
            self.names2.append("Exit")
            self.urls2.append(" ")
            self.pics2.append(" ")
            self.names2.append("Setup")
            self.urls2.append(" ")
            self.pics2.append(" ")
            self.names2.append("Favorites")
            self.urls2.append(" ")
            self.pics2.append(" ")            
            
            
            self.tmppics2 = []
            self.lines = []
            self.vidinfo = []
            afile = open("/tmp/test.txt","w")       
            afile.write("\nin action=")
            datain = " "
            parameters = []
            self.data = []
            print "StartPlugin_mainmenu self.dtext =", self.dtext
            data = self.dtext.splitlines()
            for line in data:
                   print "StartPlugin_mainmenu line =", line
                   if not "data B" in line: continue
                   else: 
                         i1 = line.find("&", 0)
                         line1 = line[i1:]
                         self.data.append(line1)
            print "StartPlugin_mainmenu self.data =", self.data
            

            if len(self.data) == 0:
                 cmd = LAST + " > /tmp/error.log 2>&1 &"
                 os.system(cmd)
                 self.error=(_("Error! Submit logs /tmp/e.log and /tmp/error.log."))
                 self["info"].setText(self.error)
                 return
            inum = len(self.data)
            print "StartPlugin_mainmenu inum =", inum
            n1 = 0
            if n1 == 0:
                 i = 0
                 while i < inum:
                        name = " "
                        url = " "
                        line = self.data[i]
                        print "StartPlugin_mainmenu line =", line
                        params = parameters_string_to_dict(line)
                        self.lines.append(line)
                        try:
                               name = params.get("name")
                               name = name.replace("AxNxD", "&")
                               name = name.replace("ExQ", "=")
                        except:
                               pass
                        try:
                              url = params.get("url")
                              url = url.replace("AxNxD", "&")
                              url = url.replace("ExQ", "=")
                        except:
                              pass
                        try:
                              pic = params.get("thumbnailImage")
                              if (pic == "DefaultFolder.png"):
                                     pic = THISPLUG + "/skin/images/default.png"
                        except:
                              pic = THISPLUG + "/skin/images/default.png"
                        self.name = name
                        self.names2.append(name)
                        self.urls2.append(url)
                        self.pics2.append(pic)
                        i = i+1
                 if (len(self.names2) == 2) and (self.urls2[1] is None) and (THISPLUG not in self.names2[1]):
                        if ("rtmp" in self.names2[1]):
                            if "live" in name:
                                name = self.name
                                desc = " "
                                url = self.names2[1]
#                                self.session.open(Showrtmp2, name, url, desc)
                                self.progressCallBack("Finished")
                                self.session.open(Playvid, name, url, desc)
                                self.close()
                           
                            else:
                                name = self.name
                                desc = " "
                                url = self.names[1]
#                                self.session.open(Showrtmp, name, url, desc)
                                self.progressCallBack("Finished")
                                self.session.open(Playvid, name, url, desc)
                                self.close()  

                        else:        
                                name = self.name                                
                                desc = " "
                                url = self.names2[1]
                                self.progressCallBack("Finished")
                                self.session.open(Playvid, name, url, desc)
                                self.close()
                 elif (len(self.names2) == 2) and (self.urls2[1] is not None) and (THISPLUG not in self.urls2[1]):
                                name = self.name                                
                                desc = " "
                                url = self.urls2[1]
                                self.progressCallBack("Finished")
                                self.session.open(Playvid, name, url, desc)
                                self.close()
                 else:        
                        if DEBUG == 1:
                                print "StartPlugin_mainmenu self.names2 =", self.names2
                                print "StartPlugin_mainmenu self.urls2 =", self.urls2
                                print "StartPlugin_mainmenu self.pics2 =", self.pics2
                        self.tmppics2 = getpics(self.names2, self.pics2, self.tmpfold, self.picfold)
                        if self.cancel==True:
                           return
                        
                        if ("plugin.image" in self.id) or ("plugin.picture" in self.id):
                                from picture import XbmcPluginScreenP
                                self.session.open(XbmcPluginScreenP, self.id, self.names2, self.urls2, self.tmppics2,1, SELECT)
                        else:
                                self.session.open(XbmcPluginScreen, self.id, self.names2, self.urls2, self.tmppics2,1)

class DelAdd(Screen):

    def __init__(self, session):
		Screen.__init__(self, session)
                self.skinName = "KodiMenusScreen"
                self.session=session
                self["menu"] = RSList([])
		self["info"] = Label()
		self.info = " "
                self["info"].setText(self.info)
                self["bild"] = startspinner()
		self.list = []
                self["pixmap"] = Pixmap()
                self["list"] = List(self.list)
                self["list"] = RSList([])
                self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.okClicked,
			"back": self.close,
			"red": self.close,
			"green": self.okClicked,
		}, -1)
	        self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))
		title = "Select to delete"
		self["title"] = Button(title)		
                self.icount = 0
                self.errcount = 0
                self.addlist = []
                self.onLayoutFinish.append(self.openTest)

    def openTest(self):
                       pic1 = THISPLUG + "/skin/images/Delete.png"  
                       self["pixmap"].instance.setPixmapFromFile(pic1)
                       adds = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins"
                       for name in os.listdir(adds):
                              if "plugin.video.select" in name:
                                    continue
                              elif "script.module.extras" in name:
                                    continue
                              elif "script.module.main" in name:
                                    continue            
                              elif "script.module" in name:                              
                                    continue            
                              elif "__init" in name:                              
                                    continue    
                              self.addlist.append(name)                      

		       showlist(self.addlist, self["menu"])

    def okClicked(self):
                sel = self["menu"].getSelectionIndex()
                plug = self.addlist[sel]
                cmd = "rm -rf '/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins/" + plug + "'"
                title = _("Removing %s" %(plug))
                self.session.open(Console,_(title),[cmd])
                self.close()
                
    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()
	
    def keyNumberGlobal(self, number):
		self["text"].number(number)

####################################


class Getaddons(Screen):

    def __init__(self, session):
		Screen.__init__(self, session)
                self.session=session
                self.skinName = "KodiMenusScreenB"
#        	self["list"] = MenuList([])
                self["menu"] = RSList([])
		self["info"] = Label()
		self.info = (_("Please select category"))
                self["info"].setText(self.info)
                self["bild"] = startspinner()
		self.list = []
                self["pixmap"] = Pixmap()
                self["list"] = List(self.list)
                self["list"] = RSList([])
                self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.okClicked,
			"back": self.close,
			"red": self.close,
			"green": self.okClicked,
		}, -1)
	        self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))
		title = "KodiLite list"
		self["title"] = Button(title)		
                self.icount = 0
                self.errcount = 0
                self.onLayoutFinish.append(self.openTest)

    def openTest(self):
                if config.plugins.kodiplug.skinres.value == "fullhd":
                       pic1 = THISPLUG + "/skin/images/DownloadL.png"
                else:
                       pic1 = THISPLUG + "/skin/images/Download.png"
                self["pixmap"].instance.setPixmapFromFile(pic1)
                self.data = []
                cats = []
                file1 = THISPLUG + "/adlist.txt"
                myfile=open(file1,"r+")
                
                icount = 0
                for line in myfile.readlines(): 
                       if line.startswith("#####"):
                                     cat = line.replace("#####", "")
                                     cat = cat.replace("####", "")
                                     if "fix" in cat:
                                           continue
                                     cats.append(cat)
                                     self.data.append(line)
		showlist(cats, self["menu"])

    def okClicked(self):
          sel = self["menu"].getSelectionIndex()
	  if sel is None :
                self.close()
          else:      
                name = self.data[sel]
#                if "Frodo" in name:
#                       url = "http://mirrors.kodi.tv/addons/jarvis/"
#                       global HOST
#                       HOST = url
#                       self.session.open(Addons, url)
#                       self.close()
                if "Adult" in name:
                       self.catname = name
                       self.allow()
                else:       
                       self.session.open(GetaddonsA2, name)
                       self.close()

    def allow(self):	        
                perm = config.ParentalControl.configured.value
                #####pass#print "perm =", perm 
                
                if config.ParentalControl.configured.value:
			#####pass#print "Here Ad 1"
#                        from Screens.InputBox import InputBox, PinInput
			self.session.openWithCallback(self.pinEntered, PinInput, pinList = [config.ParentalControl.setuppin.value], triesEntry = config.ParentalControl.retries.servicepin, title = _("Please enter the parental control pin code"), windowTitle = _("Enter pin code"))

		else:
			#####pass#print "Here Ad 2"
                        self.pinEntered(True)
#		return
       
    def pinEntered(self, result):
		#####pass#print "Here Ad 3 result =", result
                if result:
                        self.session.open(GetaddonsA2, self.catname)
                        self.close()
		else:
			self.session.openWithCallback(self.close, MessageBox, _("The pin code you entered is wrong."), MessageBox.TYPE_ERROR)
         		self.close()
	        
                       
                       
                      

    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()
	
    def keyNumberGlobal(self, number):
		#pass#print "pressed", number
		self["text"].number(number)


class GetaddonsA2(Screen):

    def __init__(self, session, cat):
		Screen.__init__(self, session)
#		if config.plugins.polar.menutype.value == "icons1":
#                       self.skinName = "Downloads"
#                else:       
                self.session = session
                self.skinName = "KodiMenusScreenB"
#        	self["list"] = MenuList([])
                self["menu"] = RSList([])
		self["info"] = Label()
		self["bild"] = startspinner()
		self.cat = cat
		self.info = (_("     Please select addon to install"))
                self["info"].setText(self.info)
		self.list = []
                self["pixmap"] = Pixmap()
                self["list"] = List(self.list)
                self["list"] = RSList([])
                self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.okClicked,
			"back": self.close,
			"red": self.close,
			"green": self.okClicked,
		}, -1)
	        self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))
		title = "Please select to install"
		self["title"] = Button(title)		
                self.icount = 0
                self.errcount = 0
                self.names = []
                self.urls = []
                self.onLayoutFinish.append(self.openTest)

    def openTest(self):
                if config.plugins.kodiplug.skinres.value == "fullhd":
                       pic1 = THISPLUG + "/skin/images/DownloadL.png"
                else:
                       pic1 = THISPLUG + "/skin/images/Download.png"
                self["pixmap"].instance.setPixmapFromFile(pic1)
                self.data = []

                try:
                       file1 = THISPLUG + "/adlist.txt"
                       f1=open(file1,"r+")
                       fpage = f1.read()
                except:       
                       fpage = " "

                self.fpage = fpage
                n1 = fpage.find(self.cat)
                n2 = fpage.find("#####", (n1+10))
                fpage2 = fpage[n1:n2]
                lines = fpage2.splitlines()
                nms = []
                for line in lines: 
                       if line.startswith("#####"):
                             continue
                       elif "---" in line: 
                             nms.append(line)
                             self.names.append(" ")
                             self.urls.append(" ")
                       elif "###" not in line:
                             continue 
                       else:
#                             pass#print "In GetaddonsA2 line =", line
                             items = line.split("###")
#                             pass#print "In GetaddonsA2 items =", items
                             nm = items[0]
                             nm = nm.replace("plugin.video.", "")
                             nm = nm.replace("plugin.audio.", "")
                             nm = nm.replace("plugin.image.", "")
                             nm = nm.replace("plugin.picture.", "")
                             nms.append(nm)
                             self.names.append(items[0])
                             self.urls.append(line)
                             
		showlist(nms, self["menu"])

    def okClicked(self):
          sel = self["menu"].getSelectionIndex()
	  if sel is None :
                self.close()
          else:      
                line = self.urls[sel]
                self.name = self.names[sel]
                self.checkLine(line)
                
    def checkLine(self, line):
           pass#print "In checkLine line =", line
           items = line.split("###")
           pass#print "In checkLine items =", items
           name = items[0]
           url1 = items[1]
           url2 = items[2]
           if url2 == '':
                xurl = url1
                xdest = "/tmp/plug.zip"
                downloadPage(xurl, xdest).addCallback(self.install).addErrback(self.showError)
           elif not items[1].endswith(".zip"):  #datadirectory zip false
                self.session.open(GetaddonsA3, line) 
                self.close()
           else:       
                url2 = items[2]
                n2 = url1.find(".zip", 0)
                n3 = url1.rfind("-", 0, n2)
                if n3 < 0:
                       n3 = url1.rfind("_", 0, n2)
                n4 = n3 + 1
                url0 = url1[:n4] 
                pass#print  "url0 =", url0
                
#                fpage = urlopen(url2).read()
                xurl = url2
                xdest = "/tmp/down.txt"
                self.line = line
                self.name = name
                self.url1 = url1
                self.url2 = url2
                self.url0 = url0 
#                fpage = urlopen(url2).read()
                downloadPage(xurl, xdest).addCallback(self.getdown).addErrback(self.showError)

    def showError(self, error):
                pass#print "ERROR :", error

    def getdown(self, fplug):                
                fpage = open("/tmp/down.txt", "r").read()
                pass#print "In checkLine fpage =", fpage
                if self.url2.endswith(".xml"):
#                        rx = self.name + '.*?version="(.*?)"'
                        rx = 'addon id="' + self.name + '".*?version="(.*?)"'
                else:
                        rx = self.name + '-(.*?).zip'
                pass#print  "rx =", rx       
                match = re.compile(rx,re.DOTALL).findall(fpage)
                pass#print  "match =", match
                if len(match) == 0:
                        rx = self.name + '_(.*?).zip'
                        match = re.compile(rx,re.DOTALL).findall(fpage)
                        pass#print  "match 2=", match
                elif len(match) == 1: 
                        latest = match[0]
                else:               
                        latest = findmax(match) 
                if latest is not None:
                        xurl = self.url0 + latest + ".zip"
                        pass#print  "xurl =", xurl
                        xdest = "/tmp/plug.zip"
                        downloadPage(xurl, xdest).addCallback(self.install).addErrback(self.showError)
                else:
                        return               
   

    def showError(self, error):
                pass#print "ERROR :", error


    def install(self, fplug):
#                cmd1 = "wget -O '" + dest + "' '" + self.url + "'"
                fdest = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins"
                addon = THISPLUG + "/plugins/" + self.name
                cmd1 = "rm -rf '" + addon + "'" 
                cmd2 = "unzip -o -q '/tmp/plug.zip' -d " + fdest
                cmd = []
                cmd.append(cmd1)
                cmd.append(cmd2)
                pass#print "cmd =", cmd
                title = (_("Installing addon"))
                self.session.openWithCallback(self.checkName,Console,_(title),cmd)
#                self.close()

    def checkName(self):
                path = THISPLUG + "/plugins"
                for name in os.listdir(path):
                       pass#print "name =", name
                       if "plugin" not in name:
                           if "__init" in name:
                               continue
                           elif "E2" in name:
                               self.close()
                           else:    
                               newname = "plugin.video." + name
                               cmd = "mv " + path + "/" + name + " " + path + "/" + newname + " &"
                               os.system(cmd) 
                       if "-master" in name:
                               newname = name.replace("-master", "")
                               cmd = "mv " + path + "/" + name + " " + path + "/" + newname + " &"
                               os.system(cmd) 
                       if ("pelisalacarta" in name) or ("tvalacarta" in name):
                               cmd = "rm '" + path + "/" + name + "/fixed2'"        
                               os.system(cmd)
                               
                self.close()
                self.checkfix()

    def checkfix(self):
                url ="http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Fix/list.txt"
                self.fixlist = urlopen(url).read()
                print "self.fixlist =", self.fixlist
                print "self.name =", self.name
                if self.name in self.fixlist:
                        plug = self.name + "-fix.1.0.0.zip"
                        xurl = "http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Fix/" + plug
                        print "xurl =", xurl
                        xdest = "/tmp/plug.zip"
	                downloadPage(xurl, xdest).addCallback(self.installB).addErrback(self.showError)
                else:
                        print "No fix to install"
                        self.close()
                                      
    def installB(self, fplug):
                fdest = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins"
                cmd = "unzip -o -q '/tmp/plug.zip' -d " + fdest
                
                print "In installB cmd =", cmd
                title = (_("Installing addon fix"))
                os.system(cmd)
                self.close()


    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()
	
    def keyNumberGlobal(self, number):
		#pass#print "pressed", number
		self["text"].number(number)


################################
def main(session, **kwargs):
        if not os.path.exists("/etc/KodiLite"):
               system("mkdir -p /etc/KodiLite")
        if not os.path.exists("/etc/KodiLite/favorites.xml"):
               cmd = "cp " + THISPLUG + "/lib/defaults/favorites.xml /etc/KodiLite/"
               system(cmd)
        system("mkdir -p "+ config.plugins.kodiplug.cachefold.value+"/xbmc")
        system("mkdir -p "+ config.plugins.kodiplug.cachefold.value+"/xbmc/vid")
        system("mkdir -p "+ config.plugins.kodiplug.cachefold.value+"/xbmc/pic")
        system("mkdir -p "+ config.plugins.kodiplug.cachefold.value+"/xbmc/tmp")
        system("mkdir -p "+ config.plugins.kodiplug.cachefold.value+"/xbmc/home/")
        system("mkdir -p "+ config.plugins.kodiplug.cachefold.value+"/xbmc/database/")
        system("mkdir -p "+ config.plugins.kodiplug.cachefold.value+"/xbmc/home/addons/")
        system("mkdir -p "+ config.plugins.kodiplug.cachefold.value+"/xbmc/home/addons/packages")
        print "In def main 4"

        print "In def main 5"
        try:cachefolder=config.plugins.kodiplug.cachefold.value
        except:cachefolder="/media/hdd"
        afile=open("/etc/xbmc.txt",'w')
        afile.write(cachefolder)
        afile.close()
        print "In def main 6"
        try:
               from Update import updstart
               updstart()
        except:       
               log("Error updating some scripts")
        print "In def main 7"
        session.open(StartPlugin_mainmenu)
        
def mpanel(menuid, **kwargs):
	if menuid == "mainmenu":
		return [("KodiLite", main, "xbmc_addons", 12)]
	else:
		return []
        
def Plugins(**kwargs):
	loadPluginSkin(kwargs["path"])
        try:
          viewdownloads=config.plugins.kodiplug.viewdownloads.value
          mmenu=config.plugins.kodiplug.mmenu.value
	except:
          viewdownloads='disabled'
          mmenu=False
	list = []
	
        list.append(PluginDescriptor(icon="plugin.png",name="KodiLite", description="Kodi Addons for enigma2", where = PluginDescriptor.WHERE_MENU, fnc=mpanel))
        list.append(PluginDescriptor(icon="plugin.png",name="KodiLite", description="Kodi Addons for enigma2", where = PluginDescriptor.WHERE_PLUGINMENU, fnc=main))
        list.append(PluginDescriptor(icon="plugin.png",name="KodiLite", description="Kodi Addons for enigma2", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main))
        
        if not viewdownloads=="disabled":
           list.append(PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART,fnc=showjobviews))
        
	
        return list
def showjobviews(reason, **kwargs):    
	if reason == 0:
           try:
		  pjopviews.gotSession(kwargs["session"])
           except:
		  pass
class classJobManagerViews():
	def __init__(self):
		self.dialog = None

	def gotSession(self, session): 
              global _session
              _session = session
              try:
                
		jobmanagerviews_keymap = THISPLUG+"/lib/jobs_keymap.xml"
		self.session=session
                global globalActionMap
		readKeymap(jobmanagerviews_keymap)
		#self.dialog = session.instantiateDialog(ScreenGrabber.ScreenGrabberView)
		#self.dialog.show()
		globalActionMap.actions['JobManagerView'] = self.ShowHide
		#self.ShowHide()

              except:
                 return

        def ShowHide(self):                             
#            from  Plugins.Extensions.KodiLite.lib.download import viewdownloads
#            viewdownloads(self.session,THISPLUG) 
            try:
                   from Plugins.Extensions.KodiLite.lib.XBMCAddonsMediaExplorer import XBMCAddonsMediaExplorer
            except:       
                   from lib.XBMCAddonsMediaExplorer import XBMCAddonsMediaExplorer
            _session.open(XBMCAddonsMediaExplorer)          
                		
pjopviews = classJobManagerViews() 


