Containerisation
================

Containerisation is a software deployment process where an application and all of the software libraries it depends on are packed into a single object, known as a container. This container can then be executed on any Operating System that provides the necessary kernel (usually Linux) features and is running on a matching hardware architecture (usually x86). The performance cost of this process is near zero however, additional storage is used as often duplicate software libraries are stored.

This has the advantage that applications can be easily redistributed (e.g. an application designed for Red Hat Enterprise Linux 9 can be run on), applications can easily be updated (or downgraded) and this can use isolation features to improve security. This paradigm is also very good for maintainability.

The mechanisms that are provided on the cluster are included below alongside some examples.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   singularity
   podman
   mpi
