# credits for original version to teeedubb
# http://forum.xbmc.org/showthread.php?tid=199579

import os
import json
import xbmc

jsonGetAudioDevice = '{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"audiooutput.audiodevice"},"id":1}'
jsonSetAudioDevice = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"audiooutput.audiodevice","value":"%s"},"id":1}'
jsonNotify = '{"jsonrpc":"2.0","method":"GUI.ShowNotification","params":{"title":"Audio Output","message":"%s","image":"info"},"id":1}'
audioDeviceHDMI = 'ALSA:hdmi:CARD=PCH,DEV=0'
#audioDeviceAnalog = 'ALSA:@'
audioDeviceAnalog = 'ALSA:@:CARD=PCH,DEV=0'

# Globals needed for writeLog()
LASTMSG = ''
MSGCOUNT = 0
#

#Constants
AUDIO_HDMI = 0
AUDIO_ANALOG = 1
AUDIO_TOGGLE = 2
ANALOG_AUDIO_STR = 'Analog'
HDMI_AUDIO_STR = 'HDMI'
DEFAULT_STR = 'Default'
LOG_ALL = 1

#path and icons
__path__ = os.path.dirname(os.path.abspath(__file__))
__filename__ = os.path.basename(os.path.abspath(__file__))

__IconStop__ = xbmc.translatePath(os.path.join( __path__,'resources', 'media', 'stop.png'))
__IconError__ = xbmc.translatePath(os.path.join( __path__,'resources', 'media', 'error.png'))
__IconSpeaker__ = xbmc.translatePath(os.path.join( __path__,'resources', 'media', 'speaker.png'))


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
        xbmc.log('%s: %s' % (__filename__, message.encode('utf-8')), level)  

def SwitchAudio(audioout):
    if audioout == AUDIO_ANALOG:
        xbmc.executeJSONRPC(jsonSetAudioDevice % audioDeviceAnalog)
    else:
        xbmc.executeJSONRPC(jsonSetAudioDevice % audioDeviceHDMI)

def GetCurrentAudio( ):
    audioDeviceCurrent = json.loads(xbmc.executeJSONRPC(jsonGetAudioDevice))['result']['value']
    if LOG_ALL == 1:
        writeLog('Current: %s' % (audioDeviceCurrent))
    if audioDeviceCurrent == audioDeviceAnalog:
        rv = AUDIO_ANALOG
    else: #if audioDeviceCurrent == audioDeviceHDMI:
        rv = AUDIO_HDMI
    return rv

def PrintableAudio( ):
    currentaudioout = GetCurrentAudio()
    if (currentaudioout == AUDIO_ANALOG):
	rv = "Analog Audio Output"
    else:
	rv = "HDMI Audio Output"
    return rv

def PrintableSelection(audioout):
    if (audioout == AUDIO_TOGGLE):
	rv = "[Toggled]"
    else:
	rv = "[Selected]"
    return rv   

def SelectAudio(audioout):
    currentaudioout = GetCurrentAudio()
    if (audioout == AUDIO_TOGGLE):
	if (currentaudioout == AUDIO_HDMI):
	    SwitchAudio(AUDIO_ANALOG)
	else:
	    SwitchAudio(AUDIO_HDMI)
    elif (audioout == AUDIO_ANALOG):
	if (currentaudioout != AUDIO_ANALOG):
	    SwitchAudio(AUDIO_ANALOG)
    else: #(audioout == AUDIO_HDMI):
	if (currentaudioout != AUDIO_HDMI):
	    SwitchAudio(AUDIO_HDMI)
    writeLog('Selected: %s %s' % (PrintableAudio(),PrintableSelection(audioout)))
    notifyOSD('AudioSwitch','Selected: %s %s' % (PrintableAudio(),PrintableSelection(audioout)),__IconSpeaker__);

####################################### START MAIN SERVICE #####################################

writeLog('Audioswitch Started ...')
writeLog('Current: %s' % PrintableAudio())

if len(sys.argv) > 1:
    writeLog("script parameters: %s" % sys.argv)
    if (sys.argv[1] == "toggle"):
    	SelectAudio(AUDIO_TOGGLE);
    elif (sys.argv[1] == "analog"):
        SelectAudio(AUDIO_ANALOG);
    elif (sys.argv[1] == "hdmi"):
        SelectAudio(AUDIO_HDMI);
    else:
	writeLog('Invalid Argument',xbmc.LOGERROR)
    	notifyOSD('AudioSwitch','Invalid Argument',__IconError__);
else: # allways toggle if no argument
    SelectAudio(AUDIO_TOGGLE);
writeLog('Audioswitch Ready ...')

