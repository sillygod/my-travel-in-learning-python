# Async Db Server

This is a practice about async db. I just read an article and 

# notes

`wire protocol` refers to the way of getting data from point to point

然後這篇作者講到他在如何傳送資料上，遇到點問題，不知道要如何做serialization @@? 我想大概是他不知道要怎麼去猜測redis client server之間的傳送，幸好redis 官網有提供[protocol 文檔](https://redis.io/topics/protocol)，需要注意的是文檔講到這個protocol，是只適用於client-server，若是redis cluster的話是用另外一種。

作者提出可以extend這個project

>To extend the project, you might consider:

>Add more commands!
>Use the protocol handler to implement an append-only command log
>More robust error handling
>Allow client to close connection and re-connect
>Logging
>Re-write to use the standard library's SocketServer and ThreadingMixin

有時間會來try try

# References

 - [article](http://charlesleifer.com/blog/building-a-simple-redis-server-with-python/)
 - [python socket doc](https://docs.python.org/3/howto/sockets.html#using-a-socket)
