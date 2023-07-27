NetClock Client
===============

This module contains the client program for the ECE 4564 NetClock project.

To the Project Team:
--------------------

Another development team has created a cross-platform UI that simulates 
the clock display that will be used in the product, as well as a simple 
chronometer that keeps time based on an interval timer and a tick
counter. The chronometer is reasonably accurate over relatively short
time periods, but must be occasionally updated from a network date
and time source in order to remain accurate over longer periods of time.

In addition to the UI and chronometer, a `__main__.py` entry point has been
provided that includes an argument parser, logging configuration, and the 
setup for the main program.

Your team will need to implement the ClockClient class using the stub
provided in `client.py`. The client ClockClient class is responsible for
registering with the server as a subscriber, periodically renewing the
subscription, and processing the periodic date/time broadcasts from the
server to update the chronometer. 

See the comments in the file for the methods your client must implement 
in order to interface with the main program. Review the project design 
blueprint for additional guidance on how to implement your client 
communication module for the clock.

While your team doesn't need a detailed understanding of all of the 
components of the client program, you should familiarize yourselves with
the location and basic purpose of each of the components provided to you.

* `__main__.py` is the main entry point, which creates the component objects
  of the client program, starts the client communication module (which runs
  on a separate thread), and the calls the clock UI's `run` method to keep
  the simulated clock UI fresh.
* `chronometer.py` contains the Chronometer class which implements the
  timekeeping functions for the clock. The passage of time is measured using
  a thread to periodically sample a high resolution tick counter.
* `instant.py` is an object that represents an instant in time as a 
  set of related attributes (year, month, day, hour, minute, etc). An 
  Instant object has an `incr` method that can be used to produce a new 
  Instant by adding a number of microseconds to itself.
* `ui/` is the package that contains code for the client's clock user 
  interface. The clock display uses simulated common LED display units 
  consisting of 7 or 14 LED segments. The code in this module uses
  [pygame](https://pygame.org) to create a drawing surface on which it draws
  and fills polygons representing each LED segment of each display unit. The 
  main UI class is the ClockUI class found in `clock.py`. It sets up the clock
  display and runs the main loop that updates the clock. It gets a reference
  to the Chronometer's `read` method which it uses to poll the current date
  and time as it updates the display.


Running the Client Program
--------------------------

The client program is designed to be run as a Python runnable module.

Because the client program uses the [pygame](https://pygame.org) library
you'll need to install this library in order to run the client. 

The easiest approach is simply to install the pygame library directly into your Python enviroment. Another approach is to use a [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html). The instructions below take
the easier approach, but feel free to use a virtual environment if you prefer.

The instructions vary by plaform.

### Mac OS X

#### Install the required library

Open a terminal and set the shell's current directory to the base directory of
the project (the one containing `requirements.txt` and the `src` directory).

Run the following command to install the required library.
```
python3 -m pip install -r requirements.txt
```

When the command above has completed successfully, the library is installed and
you needn't perform this step again.

#### Run the client

Open a terminal and set the shell's current directory to the base directory of
the project (the one containing `requirements.txt` and the `src` directory).

Run the client using the following commands.
```
export PYTHONPATH=src
python3 -m clock_client 127.0.0.1
```

The client supports several different colors and sizes for the UI. To learn 
about all the options, run the same Python command with the `-h` (`--help`) 
option.

### Windows

#### Install the required library

Open a command prompt and set the current directory to the base directory of
the project (the one containing `requirements.txt` and the `src` directory).

Run the following command to install the required library.
```
python3 -m pip install -r requirements.txt
```

(depending on how you installed Python, you might need to omit the `3` from
the `python3` command)

When the command above has completed successfully, the library is installed and
you needn't perform this step again.

#### Run the client

Open a command prompt and set the current directory to the base directory of
the project (the one containing `requirements.txt` and the `src` directory).

Run the client using the following commands.
```
set PYTHONPATH=src
python3 -m clock_client 127.0.0.1
```

The client supports several different colors and sizes for the UI. To learn 
about all the options, run the same Python command with the `-h` (`--help`) 
option.

