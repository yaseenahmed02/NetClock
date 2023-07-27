
# NetClock Project - ECE 4564

  

This repository contains resources for the NetClock project, a part of Professor Carl Harris' ECE 4564 class at Virginia Tech.

  

## Project Description

NetClock is a distributed clock system designed as a part of ECE 4564 coursework under the guidance of Professor Carl Harris. The goal of this project is to synchronize clocks across different devices connected to the same network. It utilizes Docker containers to isolate the server and client components for easy deployment and testing.

  

## Build Instructions

To build the NetClock image, execute the following command:

  

```
docker build -t net-clock .
``````

  

## Running the NetClock

To run the NetClock image, execute the following command:

  

```
docker run -it --rm net-clock
`````

## Running without Docker
 If you prefer to run the NetClock without Docker, you can individually run the client and server modules. Follow the instructions below: 

**Running the Client:** Open a terminal and set the shell's current directory to the base directory of the project (the one containing `requirements.txt` and the `src` directory). Run the client using the following commands:

```
export PYTHONPATH=src
python3 -m clock_client 127.0.0.1
```

**Running the Server:**  Open a terminal and  set the shell's current directory to the base directory of the project (the one containing `requirements.txt` and the `src` directory). Run the following commands:
  
```
export PYTHONPATH=src
python3 -m clock_server subscribers.json
```

  

There are lots of other command line options that can be specified; run the same Python command with the `-h` (`--help`) option for details.

More details for different environments can be found in the individual README files for both the client and the server.

## Authors

- Yaseen Ahmed
- Ahmed Fathi
- Ryan Phillips

  

## Credits

The NetClock project is a collaborative effort of the above authors. Special thanks to Professor Carl Harris for providing guidance and expertise throughout the development of this project.

  

For any questions or inquiries, please contact yahme02@gmail.com.

 