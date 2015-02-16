# credits for original version to teeedubb
# http://forum.xbmc.org/showthread.php?tid=199579

import os
import json
import xbmc
import xbmcaddon
import xbmcgui
from xbmc import getCondVisibility as condition, translatePath as translate, log as xbmc_log
from subprocess import PIPE, Popen

__addon__      = xbmcaddon.Addon()
__addonname__  = __addon__.getAddonInfo('name')
__addonid__    = __addon__.getAddonInfo('id')
__cwd__        = __addon__.getAddonInfo('path').decode("utf-8")
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString

jsonGetAudioDevice = '{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"audiooutput.audiodevice"},"id":1}'
jsonSetAudioDevice = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"audiooutput.audiodevice","value":"%s"},"id":1}'
#audioDeviceHDMI = 'ALSA:hdmi:CARD=PCH,DEV=0'
#audioDeviceAnalog = 'ALSA:@'
#audioDeviceAnalog = 'ALSA:@:CARD=PCH,DEV=0'

# Globals needed for writeLog()
LASTMSG = ''
MSGCOUNT = 0
#

#Constants
AUDIO_OPTION1 = 0
AUDIO_OPTION2 = 1
AUDIO_TOGGLE = 2
OPTION1_STR = 'device_opt1'
OPTION2_STR = 'device_opt2'
NAME_STR = '_name'
LOG_ALL = 0

#path and icons
__path__ = os.path.dirname(os.path.abspath(__file__))
__filename__ = os.path.basename(os.path.abspath(__file__))

__IconStop__ = xbmc.translatePath(os.path.join( __path__,'resources', 'media', 'stop.png'))
__IconError__ = xbmc.translatePath(os.path.join( __path__,'resources', 'media', 'error.png'))
__IconSpeaker__ = xbmc.translatePath(os.path.join( __path__,'resources', 'media', 'speaker.png'))

__GETAUDIO__ = xbmc.translatePath(os.path.join( __path__,'resources', 'lib', 'getAudio.sh'))

####################################### GLOBAL FUNCTIONS #####################################

def notifyOSD(header, message, icon):
    xbmc.executebuiltin('XBMC.Notification(%s,%s,5000,%s)' % (header.encode('utf-8'), message.encode('utf-8'), icon))

def writeLog(message, level=xbmc.LOGNOTICE):
    global LASTMSG, MSGCOUNT
    if LASTMSG == message:
        MSGCOUNT = MSGCOUNT + 1
        return
    else:
        LASTMSG = message
        MSGCOUNT = 0
        xbmc.log('%s: %s' % (__addonid__, message.encode('utf-8')), level)  

####################################### AUDIOSWITCH FUNCTIONS #####################################

def SwitchAudio(audioout):
    if audioout == AUDIO_OPTION1:
        xbmc.executeJSONRPC(jsonSetAudioDevice % ("ALSA:" + __addon__.getSetting(OPTION1_STR)))
    else:
        xbmc.executeJSONRPC(jsonSetAudioDevice % ("ALSA:" + __addon__.getSetting(OPTION2_STR)))
    return audioout

def GetCurrentAudio( ):
    audioDeviceCurrent = json.loads(xbmc.executeJSONRPC(jsonGetAudioDevice))['result']['value']
    if LOG_ALL == 1:
        writeLog('Current: %s' % (audioDeviceCurrent))
    if audioDeviceCurrent == __addon__.getSetting(OPTION1_STR):
        rv = AUDIO_OPTION1
    else:
        rv = AUDIO_OPTION2
    return rv

def PrintableAudio(audioout):
    if (audioout == AUDIO_OPTION1):
	rv = __addon__.getSetting(OPTION1_STR+NAME_STR)
    else:
	rv = __addon__.getSetting(OPTION2_STR+NAME_STR)
    return rv

def PrintableSelection(audioout):
    if (audioout == AUDIO_TOGGLE):
	rv = "[Toggled]"
    else:
	rv = "[Selected]"
    return rv   

def SelectAudio(audioout):
    currentaudioout = GetCurrentAudio()
    writeLog('Current output: %s' % PrintableAudio(currentaudioout))
    if (audioout == AUDIO_TOGGLE):
	if (currentaudioout == AUDIO_OPTION1):
	    selaudio=SwitchAudio(AUDIO_OPTION2)
	else:
	    selaudio=SwitchAudio(AUDIO_OPTION1)
    elif (audioout == AUDIO_OPTION1):
	if (currentaudioout != AUDIO_OPTION1):
	    SwitchAudio(AUDIO_OPTION1)
        selaudio=audioout
    else:
	if (currentaudioout != AUDIO_OPTION2):
	    SwitchAudio(AUDIO_OPTION2)
        selaudio=audioout
    writeLog('Selected output: %s %s' % (PrintableAudio(selaudio),PrintableSelection(audioout)))
    notifyOSD('AudioSwitch','Selected: %s %s' % (PrintableAudio(selaudio),PrintableSelection(audioout)),__IconSpeaker__);

####################################### SETTINGS FUNCTIONS #####################################

def GetLogs( ):
    log_path = translate('special://logpath')
    log = os.path.join(log_path, 'kodi.log')
    return log

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def getAudioOptions(LogFile):
    devices = []
    names = []
    TheCommand = ('%s %s' % (__GETAUDIO__, LogFile))
    #writeLog(TheCommand)
    res = cmdline(TheCommand)
    for line in res.splitlines():
        data = line.split('\t')
        devices.append(data[0])
        names.append(data[1])
    if LOG_ALL == 1:
        for i in xrange(0,len(devices)):
            writeLog('%s | %s' % (devices[i],names[i]))
    return devices, names

def OptionSelector(SelOpt):
    #writeLog('Logfile: %s' % (GetLogs()))
    #writeLog('Option: %s ' % (SelOpt))
    devices, names = getAudioOptions(GetLogs())
    dialog = xbmcgui.Dialog()
    if names != []:
        selected = dialog.select("Select Audio Device %s" % SelOpt[-1:], names)
        if selected != -1:
            __addon__.setSetting(SelOpt, str(devices[selected]).strip())
            __addon__.setSetting(SelOpt + NAME_STR, str(names[selected]))
            if LOG_ALL == 1:
                writeLog('selected device: %s' % devices[selected])
                writeLog('selected name: %s' % names[selected])

####################################### START MAIN SERVICE #####################################

writeLog('Audioswitch Started ...')

if len(sys.argv) > 1:
    writeLog("script parameters: %s" % sys.argv[1])
    if (sys.argv[1] == "toggle"):
    	SelectAudio(AUDIO_TOGGLE);
    elif (sys.argv[1] == "1"):
        SelectAudio(AUDIO_OPTION1);
    elif (sys.argv[1] == "2"):
        SelectAudio(AUDIO_OPTION2);
    elif (sys.argv[1].startswith('device_opt')):
	OptionSelector(sys.argv[1]);
    else:
	writeLog('Invalid Argument',xbmc.LOGERROR)
    	notifyOSD('AudioSwitch','Invalid Argument',__IconError__);
else: # allways toggle if no argument
    SelectAudio(AUDIO_TOGGLE);
writeLog('Audioswitch Ready ...')

