title: FindIT-Link
value: 1000
description: Just an easy chall you will given an admin password

Note: Solve at local first then try on remote, All traffic will be monitored if someone change the password, delete flag or any files on server will get punishment!!!!!!!

**Raise ticket for admin password if you solved on local already **

```
sudo apt install qemu-user-static
cd squashfs-root/
cp /usr/bin/qemu-arm-static ./usr/bin/
sudo mount --bind /dev ./dev && sudo mount --bind /proc ./proc
sudo chroot . /usr/bin/qemu-arm-static /sbin/ubusd &
sudo chroot . /usr/bin/qemu-arm-static /usr/sbin/uhttpd -f -h /www -r FindIT -x /cgi-bin -t 120 -T 30 -A 1 -n 3 -R -p 0.0.0.0:80
```

author: <span style="color:#f275a1;">Linz</span>