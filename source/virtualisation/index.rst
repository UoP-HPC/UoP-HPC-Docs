Virtualisation
================

Virtualisation is a technique where an operating system is ran, virtually, within another operating system. This is accomplished either by using software, called an emulator, or by using hardware features such as Intel VT-x or AMD-V. The latter case is known as hardware assisted virtualization. The virtualised operating system (also known as the guest operating system), can be aware that it is being virtualised, in which case certain features can be provided to the guest directly from the parent operating system (known as the host) -- this is called paravirtualization. When both hardware assisted virtualization and paravirtualization are used together, the guest operating system can perform almost as whell as it would if it were running directly on the physical hardware.

The is useful for running multiple operating systems on the same physical hardware (for example to support different workloads), to isolate different workloads from each other for security reasons, or to run operating systems on hardware that the operating system does not support (e.g. Android could run as a guest on Red Hat Enterprise Linux).

The QEMU emulator and virtual machine manager is available on Lovelace. Lovelace also supports KVM which is the Linux feature that provides hardware assisted virtualization. Examples of running specific operating systems are given below:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   windows
