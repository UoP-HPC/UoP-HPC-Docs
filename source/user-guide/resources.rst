.. include:: ../siteinclude.rst

Accessing Compute Resources
===========================

The Lovelace Cluster uses Slurm to schedule jobs and allocate resources.

Writing a submission script is typically the most convenient way to
submit your job to the job submission system. Example submission scripts
(with explanations) for the most common job types are provided below.

Interactive jobs are also available and can be particularly useful for
developing and debugging applications. More details are available below.

If you have any questions on how to run jobs on Lovelace do not hesitate
to contact the HPC Support at `hpcsupport@plymouth.ac.uk <mailto:hpcsupport@plymouth.ac.uk>`_.

Using Slurm
------------

You typically interact with Slurm by (1) specifying Slurm directives in job
submission scripts (see examples below) and (2) issuing Slurm commands
from the login nodes.

There are three key commands used to interact with the Slurm on the
command line:

-  :bash:`sbatch`
-  :bash:`squeue`
-  :bash:`scancel`

Check the Slurm :bash:`man` page for more advanced commands:

.. code-block:: bash

    man slurm

The sbatch command
~~~~~~~~~~~~~~~~~~

The sbatch command submits a job to Slurm:

.. code-block:: bash

    sbatch job_script

This will submit your job script :plaintext:`job_script` to the job-queues.
See the sections below for details on how to write job scripts.

The squeue command
~~~~~~~~~~~~~~~~~~

Use the command below to view the job queue. For example:

.. code-block:: bash

    squeue

will list all jobs on Lovelace.

You can view just your jobs by using:

.. code-block:: bash

    squeue --me

The scancel command
~~~~~~~~~~~~~~~~~~~~

Use this command to delete a job from Lovelace's job queue. For example:

.. code-block:: bash

    scancel <jobid>

will remove the job with ID :plaintext:`<jobid>` from the queue.


Queues
------------

Please note that Slurm job scheduler uses the term 'partitions' to
refer to queues, and therefore you may see the word partition used
interchangeably both here and on other sites.

There are multiple partitions available on the Lovelace cluster. These correspond to two sets of partiitons. These are the standard queues (:plaintext:`cpu_shared`, :plaintext:`cpu`, :plaintext:`cpu_longrun`, :plaintext:`cpu_highmem`, :plaintext:`gpu_h100`, :plaintext:`gpu_l40s`) and the billed queues (:plaintext:`cpu-billed`, :plaintext:`cpu_highmem-billed`, :plaintext:`gpu_h100-billed`, :plaintext:`gpu_l40s-billed`).

You may only schedule task on the billed queues if there is funding assosciated with your account. Jobs submitted to these queues will be prioritised over those submitted to the standard queue.

:plaintext:`cpu_shared`
~~~~~~~~~~~~~~~~~~~~~~~

This queue allows users to 'share' resources meaning that they can request parts of nodes (i.e. a specific number of CPU cores and a specific amount of memory -- if a specific amount of memory is not requested, memory will be allocated proportionally to the number of CPUs you request).

To run on the :plaintext:`cpu_shared` queue, add the following to the header of your
submission script:

.. code-block:: sbatch

   #SBATCH -p cpu_shared
   #SBATCH --cpus-per-task 1

This specifies that your job requires exactly one CPU core. If your workload supports multithreading/multiprocessing, you may request a higher number of cores by increasing the value of the :plaintext:`--cpus-per-task` parameter. For example, if your workload users three cores, you could specify :plaintext:`--cpus-per-task 3`. A value of up to 64 is supported on the Lovelace cluster.

:plaintext:`cpu`
~~~~~~~~~~~~~~~~

This queue will always allocate a full 64 core node exclusively to your job.

To run on the :plaintext:`cpu` queue, add the following to the header of your
submission script :

.. code-block:: sbatch

   #SBATCH -p cpu

:plaintext:`cpu_highmem`
~~~~~~~~~~~~~~~~~~~~~~~~

This queue will always allocate a full 64 core node with approximately 1.5 TiB of Memory exclusively to your job.

To run on the :plaintext:`cpu_highmem` queue add the following to the header of your
submission script :

.. code-block:: sbatch

   #SBATCH -p cpu_highmem

:plaintext:`cpu_longrun`
~~~~~~~~~~~~~~~~~~~~~~~~

This queue is the same as the :plaintext:`cpu_shared` queue except that it allows time limits of up to 14 days. Users must have permission and good justification to run on this queue. Please contact `hpcsupport@plymouth.ac.uk <mailto:hpcsupport@plymouth.ac.uk>`_ with your reasoning to request this.

To run on the :plaintext:`cpu_longrun` queue add the following to the header of your
submission script :

.. code-block:: sbatch

   #SBATCH -p cpu_longrun
   #SBATCH --cpus-per-task 1

.. _gpu_h100_job:

:plaintext:`gpu_h100`
~~~~~~~~~~~~~~~~~~~~~

This queue allows users to request one or multiple `NVIDIA H100 SXM <https://www.nvidia.com/en-gb/data-center/h100/>`_ GPUs.

To run on the :plaintext:`gpu_h100` queue add the following to the header of your
submission script :

.. code-block:: sbatch

   #SBATCH -p gpu_h100
   #SBATCH --gpus 1

Each job must request at least one GPU if running on this partition. The job will be allocated CPU cores proportionally to the number of GPUs they've requested -- this means 16 CPU cores per GPU. As such, please do not specify :plaintext:`--cpus-per-task` on this partition.

.. _gpu_l40s_job:

:plaintext:`gpu_l40s`
~~~~~~~~~~~~~~~~~~~~~

This queue allows users to request one or multiple `NVIDIA L40S <https://www.nvidia.com/en-gb/data-center/l40s/>`_ GPUs.

To run on the :plaintext:`gpu_l40s` queue add the following to the header of your
submission script :

.. code-block:: sbatch

   #SBATCH -p gpu_l40s
   #SBATCH --gpus 1

Each job must request at least one GPU if running on this partition. The job will be allocated CPU cores proportionally to the number of GPUs they've requested -- this means 8 CPU cores per GPU. As such, please do not specify :plaintext:`--cpus-per-task` on this partition.

Sometimes some nodes are "down" and less nodes are available.

If you have special request, contact `hpcsupport@plymouth.ac.uk
<mailto:hpcsupport@plymouth.ac.uk>`_.

Time Limits
-----------

Time limits will be applied to all jobs on the free queues (:plaintext:`cpu_shared`, :plaintext:`cpu`, :plaintext:`cpu_longrun`, :plaintext:`cpu_highmem`, :plaintext:`gpu_h100`, :plaintext:`gpu_l40s`) on the Lovelace cluster. By default, jobs will have a Time Limit of 1 hour. This means that, **by default**, if your job runs for longer than 1 hour, it will automatically be terminated. In the event that you require your job to run for more than 1 hour, you must add a header specifiying a time limit such as:

.. code-block:: sbatch

   #SBATCH --time "12:30:15"

This example increases the time limit from the default limit of 1 hour to a limit of 12 hours, 30 minutes, and 15 seconds.

You can specify a time limit of up to 3 days or, equivalently, 72 hours (on the :plaintext:`cpu_longrun` queue, you can specify a time limit of up to 14 days or, equivalently, 336 hours). The time limit is also used by the job scheduler to, when a reservation is scheduled (e.g. for a training event or for teaching), decide whether to schedule the job in advance of the reservation. As such, a job with a lower time limit specified may sometimes be scheduled more quickly than one that has a higher time limit specified.

Accounts
--------

Users are allocated to Slurm Accounts based on the projects they are part of. Users that are only part of a single project (and thus a single Slurm Account) will have jobs automatically allocated against this project for accounting purposes. Users that are part of multiple projects should include a line in their submission scripts that sets the account for the job as follows.

.. code-block:: sbatch

   #SBATCH --account=<account name>

Output from Slurm jobs
----------------------

Slurm produces the output of your job submission in a file with the format :plaintext:`slurm-<Job ID>.out`. This file will be created in the working directory from which you submitted the job with :bash:`sbatch`. You can view the job using the :bash:`less` utility as below:

.. code-block:: bash

   less -r slurm-<Job ID>.out

Examples of Job Submission Scripts
----------------------------------

Some examples are given below:

Run a Python Script using Numpy on a CPU Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The job submission below assumes that the script is called :plaintext:`myscript.py` and stored in your home folder.

.. code-block:: sbatch

   #!/bin/bash
   #SBATCH -p cpu

   cd
   module load py-numpy
   python3 myscript.py

If the submission script is called :plaintext:`py-numpy.sbatch`, you can submit it by running:

.. code-block:: bash

   sbatch py-numpy.sbatch

Run a GPU Application on a GPU Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This job runs the :plaintext:`nvidia-smi` utility on a GPU node with a GPU, returning details about the allocated GPU

.. code-block:: sbatch

   #!/bin/bash
   #SBATCH -p gpu_l40s
   #SBATCH --gpus 1

   nvidia-smi

Submitting Interactive Jobs
---------------------------

Interactive jobs can be submitted using the :bash:`srun` utility. For example, running the below will request an interactive shell session on a CPU node (using the :plaintext:`cpu_shared` partition):

.. code-block:: bash

   srun -p cpu_shared --pty bash

Similarly, you can request an interactive session on a GPU node. The example below also sets a time limit of one hour and uses the :plaintext:`gpu_l40s` partition.

.. code-block:: bash

   srun -p gpu_l40s --gpus 1 --time "1:00:00" --pty bash

Note that most arguments to :sbatch:`#SBATCH` as given above also apply to :bash:`srun`.
