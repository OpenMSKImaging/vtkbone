# vtkbone
VTK classes for processing of finite element models derived from micro-CT.
vtkbone was formerly vtkn88.

[![Build Status](https://dev.azure.com/babesler/n88/_apis/build/status/Numerics88.vtkbone?branchName=master)](https://dev.azure.com/babesler/n88/_build/latest?definitionId=9&branchName=master)
[![Anaconda-Server Badge](https://anaconda.org/numerics88/vtkbone/badges/installer/conda.svg)](https://anaconda.org/numerics88/vtkbone)

## Documentation

The API documentation for vtkbone can be found on-line at https://bonelab.github.io/n88/documentation/vtkbone/1.0/. Or, you can generate it yourself from the source code using DOxygen.

A manual exists for the Faim FE package that includes a chapter on using vtkbone,
and a chapter with tutorials. It can be found at http://numerics88.com/documentation/ .

## Installation 
Vtkbone is open-source and if you want you can download the source code from [https://github.com/Numerics88/] and compile them yourself it yourself (see below for compiling and linking). However, this is a hastle and the easiest way to install vtkbone is using Anaconda Python, which is supported on Linux, Windows, and macOS. 

You can install <mark>Anaconda</mark> Python from [here](https://www.anaconda.com/download). You can also install <mark>Miniconda</mark> [here](https://docs.conda.io/projects/miniconda/en/latest/index.html#quick-command-line-install), a free minimal installer for Conda. It is a small bootstrap version of Anaconda Python that only includes conda, Python, the packages they both depend on, and a small number of other useful packages (like pip, zlib, and a few others). If you want more packages, you can install them of course using the conda install command to install. 

Next, you need to create an Anaconda <mark>enviroment</mark> to run vtkbone. An environment is a folder or directory that contains a specific collection of conda packages and their dependencies. Creating an Anaconda environment is optional. However, creating an Anaconda environment prevents conflicts between packages and ensures that your projects are reproducible. You can read more about [Anaconoda environments](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-python) if you are interested. To create an Anaconda environment and install vtkbone all in one step, run the following command: 

```sh
conda create --name vtkbone --channel numerics88 --channel conda-forge python=3.7 n88tools numpy scipy
```

To use vtkbone, you simply activate the Anaconda environment. On Linux and macOS this is done through the following command: 

```sh
conda activate vtkbone
```
On Windows the command is 
```sh
activate vtkbone
```
You will have to activate the conda environment on each terminal (or Command Prompt) when you want to use vtkbone.

For problems with M1 mac:
To run Anaconda using the x86_64 (Intel) architecture on an Apple M1 (ARM64) Mac, you can use Rosetta 2, which is Apple's built-in compatibility layer for running Intel-based applications on ARM-based Macs. Here are the steps to run Anaconda using Rosetta 2:
1. Install Rosetta 2 (if not already installed). If you haven't already installed Rosetta 2, you can do so by running the following command in your terminal:
```sh
softwareupdate --install-rosetta 
```
2. Activate Rosetta 2 for terminal: To ensure that the terminal runs in Rosetta 2 mode (Intel mode), you can use the arch command to switch the terminal to use the x86_64 architecture. Open a new terminal window, and then run the following command:
```sh
arch -x86_64 /bin/zsh 
```
Replace bin/bash with the shell that you use if it's different. 


## Compiling and linking

vtkbone requires the following:

  * CMake: www.cmake.org
  * Boost: www.boost.org
  * n88util: https://github.com/Numerics88/n88util
  * AimIO: https://github.com/Numerics88/AimIO
  * pQCTIO: https://github.com/Numerics88/pQCTIO
  * Google test: https://github.com/google/googletest

To build and run the tests with cmake, on linux or macOS, something like the
following sequence of commands is required:

```sh
mkdir build
cd build
ccmake ..
make
ctest -V
```
On Windows the procedure is a rather different: refer to CMake documentation.

Class List
=================

Here is a list of some useful classes, structs, unions and interfaces with brief descriptions. 
For a full list, see [here](https://bonelab.github.io/n88/documentation/vtkbone/1.0/annotated.html). 

|Command|Description|
|:--------:|:--------:|
|  vtkboneAIMReader   |  read in a .AIM file   | 
|  vtkboneAIMWriter   |  writes a .AIM file   |  
|  vtkboneApplyBendingTest   |  generates a finite element mesh that corresponds to a bending test   |  
|  vtkboneApplyCompressionTest   |  generates a finite element mesh that corresponds to a compression test   | 
|  vtkboneApplyDirectionalShearTest   |  generates a finite element mesh that corresponds to a directional shear test   | 
|  vtkboneApplySymmetricShearTest   |  generates a finite element mesh that corresponds to a symmetric shear test   | 
|  vtkboneN88ModelReader   |  reads n88 model files   | 
|  vtkboneN88ModelWriter   |  writes an n88model file   | 
|  vtkboneSolverParameters   |  description of the finite element test   | 

## Authors and Contributors

vtkbone is maintained and supported by Numerics88
Solutions Ltd (http://numerics88.com). It was originally developed
at the University of Calgary
by Eric Nodwell (eric.nodwell@numerics88.com) and Steven K. Boyd
(https://bonelab.ucalgary.ca/).

## Licence

vtkbone is licensed under a MIT-style open source license. See the file LICENSE.
