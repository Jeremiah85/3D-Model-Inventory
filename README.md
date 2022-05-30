# 3D Model Inventory

Simple inventory app for 3D Models written using Python and SQLite

## Table of Contents

* [General Info](#general-info)
* [Technologies](#technologies)
* [Requirements](#requirements)
    * [Source](#source)
    * [Executables](#executables)
* [Tested Operating Systems](#tested-operating-systems)
* [Setup](#setup)
    * [Source](#source-1)
    * [Executables](#executable)
* [Status](#status)
* [License](#license)

## General Info

This is a simple application to help manage my 3D model collection.
Previously I kept my list of models in a spreadsheet and so I thought an
actual dedicated application would be more sustainable in the long run.
I am taking the opportunity to teach myself Python and SQLite in the process
since my only other experience with writing code is with Powershell.

## Technologies

* Python 3.10
* SQLite 3
* Tkinter
* Pyinstaller

## Requirements

### Source

* Python > 3.10.4
* Tkinter 

### Executables

* None

## Tested Operating Systems

* Windows 10 Pro
* Windows 11 Pro
* Ubuntu 22.04
* Fedora 36

## Setup

### Source

To run this project, navigate to the application's directory and execute
model_inv.py:

```
$ py model_inv.py
```

If  you are running Linux you may need to install tkinter. On Ubuntu, run:

```
$ sudo apt-get install python3-tk
$ python3 model_inv.py

```

On Fedora, run:
```
$ sudo dnf install python3-tkinter
$ python3 model_inv.py
```
### Executable

Windows:
```
> model_inv.exe
```

```
$ ./model_inv
```

## Status

This is a hobby project and I am releasing it on the off chance someone else
may find it useful. If you do find any part useful, I'd love to hear about it.

## License

See [License](https://github.com/Jeremiah85/3D-Model-Inventory/blob/main/LICENSE.md)
