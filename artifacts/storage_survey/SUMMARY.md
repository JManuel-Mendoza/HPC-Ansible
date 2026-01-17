# Storage Survey Summary
Generated: 2026-01-17T15:46:17-05:00

| Host | Kernel | Disks (nvme) | Disks (sata/other) | NFS export mount (master) | NFS mount (workers) | /scratch recommendation | /data recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| master | 5.14.0-611.16.1.el9_7.x86_64 | nvme0n1 disk 238.5G | sda     disk   3.6T<br>sr0     rom   1024M | Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/nvme0n1p3 xfs    80G   20G   60G  25% / | not mounted | nvme scratch | sata/other data |
| worker1 | 5.14.0-611.20.1.el9_7.x86_64 | nvme0n1 disk 238.5G | sda     disk   3.6T<br>sr0     rom   1024M |  | not mounted | nvme scratch | sata/other data |
| worker2 | 5.14.0-611.20.1.el9_7.x86_64 | nvme0n1 disk 238.5G | sda     disk   3.6T<br>sr0     rom   1024M |  | not mounted | nvme scratch | sata/other data |
