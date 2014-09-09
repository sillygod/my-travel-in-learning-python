Desc
----
This is a command line interface chatroom. Just a practice.
it simply create a socket server to listen any message from clients.


Implement
----
In order to get the control of cmd in Windows (my environment), I need to
use ctypes to call widnows api. Something like changing cursor position,
read/write console buffer etc.

now, everything is just a test...



### sturcture

console.lpy -- use windows api to control the console interface.

chatroom.py -- use python module socket to create a server to listen request from client multi user chatroom.

multiConsole.py -- implement some simple user interface for this project.





Preview
----
create a server and then connect to
![usage pic](http://i.imgur.com/Mmxx34i.png)

multiuser
![multiuser](http://i.imgur.com/s9QpRpi.png)


show a hint for someone leave the room
![leave room](http://i.imgur.com/W9hBcJz.png)



Reference:
----
http://msdn.microsoft.com/en-us/library/windows/desktop/ms684965%28v=vs.85%29.aspx

