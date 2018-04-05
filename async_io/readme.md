This will contain some practice about python asyncio and do some comparison for callback style between async 

非同步編程在python中最近是越來越受歡迎，在python中有著許多libraries是用來做非同步的，其中之一是asyncio而且這也是讓python在async編程受歡迎的主因，在開始正題前，我們先來理解一些歷史緣由。

在普遍的程式，執行順序都是一行一行執行，每次要繼續往下執行前，都會等著上一行完成，也就是俗稱的Sequential programming