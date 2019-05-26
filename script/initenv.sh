#!/bin/bash
echo  'KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE:="0777", SYMLINK+="hldslidar"' >/etc/udev/rules.d/hldslidar.rules

echo  'KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE:="0777", GROUP:="dialout",  SYMLINK+="ydlidar"' >/etc/udev/rules.d/ydlidar.rules

echo  'KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE:="0777", GROUP:="dialout",  SYMLINK+="iiilidar"' >/etc/udev/rules.d/iiilidar.rules

echo  'KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE:="0777", GROUP:="dialout",  SYMLINK+="rplidar"' >/etc/udev/rules.d/rplidar.rules


service udev reload
sleep 1
service udev restart
