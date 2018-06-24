# my-travel-in-learning-python


This repository may contain some small projects or practices I want to take a note. It is just like a traveler to take a snap shot of everything everywhere. Python is my favorite programming language and it has lots of amazing merits and something shock.


### Intention

In order to learning python, I think some projects to implement and try hard to complete them. Bascially, there are some librarys or frameworks I want to be familiar with

 - pygame
 - pyqt
 - django
 - asyncio

Recently, I will put some practice about python standard lib, programming concepts or notes about some blogs or posts.

# projecct-list

 - 2d collision
 - django_zoo
 - cli_chatroom
 - imageCropper
 - imageDisplayer
 - ...maybe more


# structure

Once I complete some projects, I will make every project structured like..

ex.

```
proj/
    some src files or folder..
    requirement.txt
    readme.md

```

Everything you need just `pip install` or `docker-compose` if provided `docker-compose.yml` 

# Future

In the future, I consider to use docker to encapsulate the env.

# Interesting usage

we can run a gui application in docker and forward x11 in mac to display gui.

ex.

install `XQuartz`

```sh
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
xhost + $IP

docker run -d --name firefox -e DISPLAY=$IP:0 -v /tmp/.X11-unix:/tmp/.X11-unix jess/firefox

```

then you will see the magic..
