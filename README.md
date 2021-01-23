# r2d2

# Preliminary steps: installation and configuration of OS and environment

## Raspberry Pi Zero
### OS
Initially the Raspberry Pi Zero (from here referred to as "rasp0") was shipped with a Sandisk uSD EDGE Class10, with Raspbian pre-installed. Performances of this OS didn't thrilled me so I used another Sandisk uSD Class10 with Archlinux for ARM architecture (OS that I usually use for work and personal computer).
#### Configuration
I spent some time to configure the machine, in order to use it comfortably. These are not necessary steps, but the configuration I deployed is the following:
- Archlinux installation from [archlinuxarm.org](https://archlinuxarm.org/platforms/armv6/raspberry-pi)
- First configuration via direct access (keyboard and HDMI connected monitor) since there rasp0 has not RJ45 for ethernet connection. In this phase I
	- edited `/etc/vconsole.conf` and set `KEYMAP=it` (I'm used - shame on me :P - an italian layout keyboard)
	- configured wireless connection, following [this guide](https://raspberrypi.stackexchange.com/a/7992)
	- added `audit=0` to `/boot/cmdline.txt` as suggested [here](https://archlinuxarm.org/forum/viewtopic.php?f=60&t=13175#p59729) to disabling audit messages that were polluting my TTY (since I didn't installed any graphic interface it was quite annoying)
- Changed default passwords using `passwd` command (defaults are: `alarm:alarm` and `root:root`, new passwords..seh ;))
- Installation of utilities (zsh, oh-my-zsh, tmux, git, vim, vim-plugins, fuzzy-finder, autojump)
- Authorization of personal ssh keys to access via SSH without providing passwords
- Installation of [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

Those steps are optional, since they allow me to work as I'm used to, instead the following are needed
- Installation of python interpreter (python2 and python3)
- Installation of ipython console (ipython2 and ipython3)
- Installation of pip (pip2 and pip3)
