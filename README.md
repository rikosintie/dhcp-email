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
1. Copy dhcp-mail.py and creds.py to /home/pi/email on the PI
2. Edit creds.py to use your credentials
3. Follow the steps in the dhcp-beacon repo to create the cron job (See below)
4. Install netifaces - python3 -m pip install netifaces

You have to creaet an "App Password" on your gmail account for this to work.
[Sign in with App Passwords](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjapdTv0Mb9AhUgOkQIHclEB6UQFnoECA4QAw&url=https%3A%2F%2Fsupport.google.com%2Fmail%2Fanswer%2F185833%3Fhl%3Den&usg=AOvVaw2ngMBFcoBvxHCwMirWpPYY)

Here is what the email looks like:
```
Host: piconsole
Time: 2023-03-06 03:55:21.976743

lo - 127.0.0.1
eth0 - 192.168.10.109
wlan0 - 192.168.4.1
```

## Automating the Script (Run Script at Boot)

On Linux systems with Cron installed, you can have your system automatically run this script using cronjobs.

Add the following to the /etc/crontab file, substituting username with your username to have the script run when your computer reboots. This assumes you've cloned dhcp-beacon to your home directory

@reboot pi /usr/bin/python3 /home/pi/email/dhcp-mail.py

## Use IPv6 on the Ethernet interface

[How to enable/disable IPv6 on Raspberry PI (Nord VPN)](https://nordvpn.com/blog/ipv6-enable-or-disable/)

Log in with root privileges.
Add these three lines to the /etc/sysctl.conf file:
* net.ipv6.conf.all.disable_ipv6 = 1
* net.ipv6.conf.default.disable_ipv6 = 1
* net.ipv6.conf.lo.disable_ipv6 = 1
Save the file and reboot your computer with this command: “$ sudo reboot.”

Once IPv6 is working it generates a link local address. use `ip address` to view the Ethernet interface settings:
```
pi@piconsole:~ $ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:e0:4c:36:00:84 brd ff:ff:ff:ff:ff:ff
    inet 169.254.123.146/16 brd 169.254.255.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::a78e:35a9:8c19:176f/64 scope link
       valid_lft forever preferred_lft forever
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether b8:27:eb:92:88:ee brd ff:ff:ff:ff:ff:ff
    inet 192.168.4.1/24 brd 192.168.4.255 scope global noprefixroute wlan0
       valid_lft forever preferred_lft forever
    inet6 fe80::f1fd:ce5f:e53b:2ac8/64 scope link
       valid_lft forever preferred_lft forever
```

In this case, the IPv6 address is `fe80::a78e:35a9:8c19:176f` and it doesn't change.

Now you can connect to the PiConsole over Ethernet without a DHCP server assigning it an address. If you don't have an Ethernet hat you can do the same thing with the wireless interface.

On Mac enter `ifconfig` in the terminal and determine what interface you are connected to.
On Linux enter `ip add` in the terminal and determine what interface you are connected to.

In this case I am using a Mac and the Ethernet interface is en12.

`ssh pi@fe80::a78e:35a9:8c19:176f%en12`

Notice that you have to add `%en12` after the address.

Open a terminal and enter:

## References
* https://www.instructables.com/LLDPi/
* https://pimylifeup.com/raspberry-pi-network-scanner/
* [Login with IP v6](https://riptutorial.com/raspberry-pi/example/24491/login-with-ipv6)
