.. include:: ../siteinclude.rst

Windows 11 (Bring Your Own Licence)
===================================

It is possible to run Microsoft Windows 11 on the Lovelace cluster. The HPC Admin Team does not provide a licence to use Windows so you must independently ensure that your installation is licensed. We also do not provide the installer for Microsoft Windows 11 -- you must download this from the Microsoft site.

Windows 11 introduces requirements that make virtualising it slightly trickier:

* It requires `Secure Boot <https://support.microsoft.com/en-gb/windows/windows-11-and-secure-boot-a8ff1202-c0d9-42f5-940f-843abef64fad>`_
* It requires `TPM 2.0 <https://support.microsoft.com/en-gb/windows/enable-tpm-2-0-on-your-pc-1fd5a332-360d-4f46-a1e7-ae6b0c90645c>`_

We will enable Secure Boot by using firmware that support Secure Boot. We will also enable TPM 2.0 by using :bash:`swtpm`, a TPM Emulator. We will also ensure that that the installation makes use of hardware assisted virtualisation and paravirtualisation features.

Desktop Session
---------------

As Windows 11 is primarily a GUI (Graphical User Interface) based product, we will start by opening a Desktop Session on JupyterHub. Please see `Using JupyterHub for Jupyter, Rstudio, Ansys Workbench and More on the Lovelace Cluster <https://docs.lovelace.plymouth.ac.uk/private/jupyterhub/>`__ for instructions on how to do this.

TPM 2.0
-------

Next, we will start the TPM Emulator to provided a backend for the TPM 2.0 device. Simply open a terminal and run the commands below:

.. code-block:: bash

   mkdir -p ~/swtpm/data
   swtpm socket --tpmstate dir=$HOME/swtpm/data --ctrl type=unixio,path=$HOME/swtpm/tpm-sock --log level=20 --tpm2

Do not close this terminal. :bash:`swtpm` must continue to be available.

Disk
----

We will create a QCOW2 image for the guest storage. Note that QCOW2 images grow as files are written but are initially small. In a new terminal, run the command below only if you do not already have an image.

.. code-block:: bash

   singularity run -B /users /scratch/software/shared_containers/qemu.sif qemu-img create -f qcow2 ~/windows.qcow2 1T

The example above uses the version of QEMU inside a singularity image to create a QCOW2 image called :plaintext:`windows.qcow2` in your home folder. :plaintext:`windows.qcow2` will have a maximum file size of 1 Terabyte.

Secure Boot
-----------

Here, we simply need to create a local copy of a file called :plaintext:`OVMF_VARS_4M.fd`. This file will contain the UEFI configuration of the guest. Run the command below only if you do not already have a local copy of this file:

.. code-block:: bash

   singularity run -B /users /scratch/software/shared_containers/qemu.sif cp /usr/share/OVMF/OVMF_VARS_4M.fd ~

Download Windows Installer
--------------------------

The Firefox browser is available in the desktop session. You can use it to download the Windows 11 installer from `Download Windows 11 <https://www.microsoft.com/en-us/software-download/windows11>`_. At time of writing, the installer is called :plaintext:`Win11_25H2_EnglishInternational_x64.iso` however, should the name change, you will need to update it in the command below.

Start the VM
------------

Now, we simply call QEMU to start the VM:

.. code-block:: bash

   singularity run -B /users,/scratch /scratch/software/shared_containers/qemu.sif qemu-system-x86_64 -smp cores=4 -m 20G -M q35,smm=on -cpu host,hv_relaxed,hv_frequencies,hv_vpindex,hv_ipi,hv_tlbflush,hv_spinlocks=0x1fff,hv_synic,hv_runtime,hv_time,hv_stimer,hv_vapic -accel kvm -drive media=cdrom,file=$HOME/Downloads/Win11_25H2_EnglishInternational_x64.iso -drive media=cdrom,file=/scratch/software/iso/virtio-win.iso -nic user,model=virtio -vga virtio -drive if=pflash,format=raw,unit=0,file=/usr/share/OVMF/OVMF_CODE_4M.secboot.fd,readonly=on -global driver=cfi.pflash01,property=secure,value=on -chardev socket,id=chrtpm,path=$HOME/swtpm/tpm-sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis,tpmdev=tpm0 -drive if=pflash,format=raw,unit=1,file=$HOME/OVMF_VARS_4M.fd -drive if=virtio,format=qcow2,file=$HOME/windows.qcow2 -boot order=cd,menu=on

.. note::

   For your convenience, the command above is stored on Lovelace in a file called :bash:`/scratch/software/startwindows.sh`. You can call that instead if you prefer.

Note that users are, in general, not expected to understand every aspect of the command above. Some things that are useful to note however are:

* :plaintext:`-smp cores=4 -m 20G` specifies how many cores and how much memory is available to the guest. This can be adjusted depending on what resources you have requested.
* :plaintext:`-accel kvm` specifies that KVM hardware assisted virtualisation should be used
* :plaintext:`-drive media=cdrom,file=/scratch/software/iso/virtio-win.iso` specifies to make an iso available to the guest. This contains drivers for paravirtualised devices.
* :plaintext:`-nic user,model=virtio -vga virtio` specifies to present Virtio paravirtualised network and graphics devices to the guest
* :plaintext:`-drive if=pflash,format=raw,unit=0,file=/usr/share/OVMF/OVMF_CODE_4M.secboot.fd,readonly=on` makes the guest use Secure Boot capable firmware
* :plaintext:`-chardev socket,id=chrtpm,path=$HOME/swtpm/tpm-sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis,tpmdev=tpm0` specifies to provide a TPM device using :bash:`swtpm`
* :plaintext:`-drive if=virtio,format=qcow2,file=$HOME/windows.qcow2` specifies to provide Virtio based paravirtualised storage. This is key to achieving good performance.

The guest interface will then pop up and the Windows installer will ask you to press any key to proceed. Simply click into the viewer, press any key (such as enter). If you want to escape the viewer, you can press Control+Alt+G.

Drivers
-------

You can now proceed with the installation as you would normally install a Windows system. Eventually, you will be prompted to 'Select location to install Windows 11' and given the option to 'Load Driver'. You will notice that no disks appear to be available initially. You must load drivers to be able to see the paravirtualised disk and install to it.

Click load drivers and, in the drop down, select the CD Drive labeled :plaintext:`virtio-win`, then the folder named :plaintext:`viostor`, then the folder named :plaintext:`w11`, then the folder named :plaintext:`amd64` then press OK. You will then see the option to install the 'Red Hat VirtIO SCSI Controller'. Simply select it and press install. Our storage drive will then appear.

Click load drivers once more and this time go to :plaintext:`virtio-win` > :plaintext:`NetKVM` > :plaintext:`w11` > :plaintext:`amd64` and install the 'Red Hat VirtIO Ethernet Adapter'.

Once the two drivers above are installed, simply select 'Disk 0 Unallocated Space' and proceed with Windows installation as normal. No further steps particular to virtualisation are needed. Congratulations in installing Windows 11 as a KVM Virtual Machine!
