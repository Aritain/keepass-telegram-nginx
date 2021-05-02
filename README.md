# KeePass with nginx and telegram

## General info

This is a simple keepass storage accessible via web. Additionally for backing up purposes there is an another container for sending you your database via telegram.

To get the general idea about KeePass - please read https://en.wikipedia.org/wiki/KeePass

Overall there are obvious security issues regarding sending your kdbx file over telegram (and exposing it over nginx I guess), so it's up to you to use telegram part or not. If you don't want it - just remove the section from docker-compose file and you'll be fine.

## How to 

To get everything running you need to do a few steps.

**Preparation**
0. Download the repo, also you'll need a docker engine on your host machine and TCP/80,443 ports exposed to the internet.
1. Create (or use your existing one) and upload .kdbx file to db/ directory inside repo. Default name of .kdbx file is main.kdbx, but you can change in docker-compose file - check "DB" env variable.
2. If you deside to use telegram part:
2.1. Add your telegram ID (you can find it via @username_to_id_bot bot) to compose file under "USER=" environment variable
2.2. Create a telegram bot via @BotFather and get its token
2.3. Add that token to compose file under "TOKEN=" environment variable
3. If you'll like to additionally protect your .kdbx exposed via nginx you can modify configs/access_lists file and add IP prefixed you'd like to permit each one starting with a new line with no additional separators. If you won't do that nginx will be able to give your file to pretty much everyone on the internet. So the formation should look like this:
    ```
    1.0.0.0/8
    2.0.0.0/16
    ```
    
**Getting the keys and making everything work**
Nginx here is using SSL certificates (it's adds a bit of security, yay), you can easily get LetsEncrypt certificates using this repo. To do this just launch all the containers using the following command
```
docker-compose up -d
```
After that you need to access the certbot container and receive a certificate:
```
docker exec -it certbot sh
certbot certonly
```
This will lead you to certificate creation dialogue, just enter your email and your server's domain name and this utility will generate everything you need and put it to the folder which nginx can access.
After this is done you need to shut down everything and relaunch it:
```
docker-compose down
docker-compose up -d
```

That's it. Now you have a fully working KeePass storage. You can access your KeePass file using the URL https://your-domain-here/keepass/your-keepass-file.kdbx, it's also works perfectly with windowns/linux/android clients.

## Notes
Just a few things you need to know about this storage in general:
* By default your db file will be sent to you every 24 hours via telegram, you can change this time via docker-compose file (search for TIMEOUT env variable)
* Nginx configuration file generated via jinja2 templating which just reads your access prefixes and domain name
* Certbot which is used here https://github.com/Aritain/certbot. It's just a slightly modified version to share process namespaces between nginx and certbot so the last one can restart nginx upon certificate renewal.
* Please expect bugs here, the whole thing was made for my personal usage mostly, but if you'll follow steps described above it should work on your machine too.
