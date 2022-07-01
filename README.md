## Email the interface name and IP address after DHCP assignment

I got the idea and most of the code from [colonket
/
dhcp-beacon](https://github.com/colonket/dhcp-beacon).

I have a Raspbery Pi Zero W configured as a serial console. I got the idea and most of the code for it from [AirPiConsole Part One](https://www.ifconfig.it/hugo/2017/09/airpiconsole-part-one/)

I added a hat that has four USB-A ports and 100m Ethernet port. So, if I have Ethernet access close by (Usually not a problem for a network engineer installing equipment) I could use it instead of wireless. That allows me to use the Wireless on my laptop to connect to the customer network.

But that brings up the problem of figuring out what IP the console received from DHCP. I seldom have access to the customer's DHCP server so that is out. I can nmap looing for port 22 and the Pi MAC address but that can set off IDS systems. 

Then I found the repo for dhcp-beacon and problem solved! The only issue was setting up gmail to allow the Pi to send mail. I ended up using an "App Password" on the google site. It's probably not as secure as I would like but the console is only powered up while I'm configuring or troubleshooting so the attack window is small.

One other item I added to the Pi is a 1000mAH UPS. I bought it on Aliexpress.com for about $20. Here is the link [UPS Lite V1.2 UPS Power HAT Board for Raspberry Pi Zero Zero W](https://www.aliexpress.com/item/3256802455758560.html?spm=a2g0o.productlist.0.0.50c5db2fmf9N8p&algo_pvid=a09501ac-b0a1-4e3a-9d0f-413ff84ed702&algo_exp_id=a09501ac-b0a1-4e3a-9d0f-413ff84ed702-0)

It allows me to run the console from battery for a couple hours instead of having to connect a USB micro cable. I also have a PoE splitter that I can plug into a PoE switch port and power the console. 

One note on powering from a switch: DO NOT use a USB-A to micro cable and plug it into the switches USB port. Here is a blog I wrote about a Cisco 4500x that wouldn't start up after a reboot. It turns out that the Get Console was sourcing too much power - [Don't charge your Airconsole (or mobile phone) on your switch's USB port!](https://mwhubbard.blogspot.com/2018/02/)

## Installation
1. Copy dhcp-mail.py and creds.py to a directory on the PI
2. Edit creds.py to use your credentials
3. Follow the steps in the dhcp-beacon repo to create the cron job
4. Install netifaces - python3 -m pip install netifaces
