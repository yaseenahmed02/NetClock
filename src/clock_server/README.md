NetClock Server
===============

This module contains the server program for the ECE 4564 NetClock project.

To the Project Team:
--------------------

The skeleton for this project has been provided to you to save you some
time effort and allow you to focus on those parts of the program that 
involve new concepts.

The server program is designed to run as a Python runnable module. As
such, this directory contains an empty `__init__.py` and a `__main__.py`.
In `__main__.py`, you'll find that an argument parser has been created
and configured with the options that you're likely to want/need when
implementing the server. The main entry point parses the command line,
and configures the logging framework first. It then creates the
SubscriberRepository and ClockServer objects and invokes the server's
`run` method.

In `server.py`, you'll find a stub for the ClockServer implementation.
The ClockServer is responsible for listening for client subscription
messages, periodically broadcasting date and time updates to all 
subscribers, and aging the collection of subscribers to detect and
remove subscriptions for clients that have not renewed their subscriptions.

The ClockServer object uses with the SubscriberRepository object
to keep a persistent record of all subscribers. In `repository.py` you'll
find a stub for your SubscriberRepository implementation. The repository
will use a Queue to accept requests to add and remove subscribers (from
the ClockServer). It will use a dedicated thread to service the queue, so
that the server is never delayed by the I/O needed to save the current
set of subscribers after each add or remove.

See the comments in the `server.py` and `repository.py` for the methods 
your team must implement. Review the project design blueprint for additional 
guidance on how to implement your server program.


Running the Server: Mac OS X
----------------------------

Open a terminal and set the shell's current directory to the base directory of
the project (the one containing `requirements.txt` and the `src` directory).

Run the following commands.
```
export PYTHONPATH=src
python3 -m clock_server subscribers.json
```

There are lots of other command line options that can be specified; run the
same Python command with the `-h` (`--help`) option for details.

Running the Server: Windows
---------------------------

Open a command prompt and set the current directory to the base directory of
the project (the one containing `requirements.txt` and the `src` directory).

Run the following commands.
```
set PYTHONPATH=src
python3 -m clock_server subscribers.json
```

(depending on how you installed Python, you might need to omit the `3` from
the `python3` command)

There are lots of other command line options that can be specified; run the
same Python command with the `-h` (`--help`) option for details.

### Windows Notes
* The server process doesn't always seem to respond to Ctrl-C on Windows. If
  necessary, use Task Manager to kill the server process.
* Windows seems to sporadically report "[WinError 10054] An existing connection 
  was forcibly by the remote host" on UDP sockets.
