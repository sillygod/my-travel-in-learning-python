# Invisible Crawler

This is crawler run withou GUI in **eye**, actually there is still a gui run in background. Why do this? You may think we can just use chrome headless or phantomjs. Yes! You can. However, there are some issue when you run chrome headless or phantomjs. That Depends on your crawler's complexity. I know one of them is function alert in javascript.

For example, you will get error when you try to get the text in alert. Maybe you can try to use some trick to overwrite the alert behavior but remember this is just one of them...

So I try to run crawler in a invisible GUI service.

# Env

python 3.5
selenium
chromium


# How to Run

```sh
docker-compose up
```

just one line to run. You can customize docker-compose.yml if you want more function.