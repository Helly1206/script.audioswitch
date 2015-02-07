Installation Notes for AudioSwitch:

     
1. Install this Addon from ZIP or if this fails copy the unpacked package
   to ~/.kodi/addons

2. Change your remote.xml to run AudioSwitch when a specific  on remote is pressed.
   If you don't have a remote control you can also define a special key on your keyboard as
   button (here as example F12)

create a remote.xml if it doesn't exists
[CODE]
	sudo mkdir /home/xbmc/.xbmc/userdata/keymaps
	cd /home/xbmc/.xbmc/userdata/keymaps
	sudo nano remote.xml
[/CODE]

and copy/paste following into the editor (or whatever button you like)
[CODE]
	<keymap>
	  <global>
            <keyboard>
              <f12>XBMC.RunScript(script.audioswitch)</f12>
            </keyboard>
	    <universalremote>
              <obc148>XBMC.RunScript(script.audioswitch)</obc148>
            </universalremote>
	  </global>
	</keymap>
[/CODE]

3. Enjoy!

Please send Comments and Bugreports to hellyrulez@home.nl
