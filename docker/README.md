# Description

This Dockerfile allows to build a Docker image with all the requirements for the development of the projects, serving also as a production environment to run the somatic variant exploration app.

# Docker build, run and exec commands

## Build a Docker image

```bash
$ cd <path/to/docker_folder>
$ docker build --tag <tag_name>:<image_name> -f Dockerfile .
```

## Docker image operations and commands

```bash
$ docker image ls #List available Docker images
$ docker image rm <image_name|image_id> #Remove a existing Docker image
```

## Create a Docker container

```bash
$ cd <path/to/docker_folder>
$ docker run -it -d -p <jupyterlab_localhost_port>:8888 --name <container_name> <tag_name>:<image_name>
```

`#[TODO] Add volumes`

## Docker container operations and commands

```bash
$ docker container ls #List available running Docker containers
$ docker container ls -a #List ALL available Docker containers (running and stopped)
$ docker container rm <container_name|container_id> #Remove a STOPPED existing Docker container
```

## How to start or stop a running container

- Start a stopped container:

```bash
$ docker start <container_name>
```

- Stop a running container:

```bash
$ docker stop <container_name>
```

## Execute a docker container with bash

```bash
$ docker exec -it <container_name> bash
```

# Run a JupyterLab Kernel from the Docker container

```bash
$ start_jupyterlab
```

**NOTE:** Press Ctrl+C and `Y` or `y` to shutdown the kernel
**NOTE:** It is recommended to run a kernel in a tmux session to prevent kernel shutdown during log out or exiting from the Docker container

