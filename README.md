# Readme File
__COP 4521 - Secure, Parallel, and Distributed Computing in Python__ 

__Group Number__: 23

__Josh Lowe__ (_jrl19@fsu.edu_) & __Trevor Fagan__ (_taf20@fsu.edu_)

## Note
Our pylint score was not a 10. The reason behind this is that we implemented security headers into our project to make our system more secure. These headers needed to be shortened to increase our pylint score. We had to make a choice and chose better security over a higher pylint score. We could have tried to implement the security headers in our nginx configuration file, but we ran out of time.

## Description of this Repository
Hacked News is a website for accessing the latest news powered by the Hacker News API. User authentication is powered by Auth0 and user information, articles, and likes are stored in a SQLite3 database. This website was built from the ground up- SSL certification, security, database setup, automated updating, recurring database updates with cron, and more all built around Flask.

## How to clone this repository into a server and host it with Nginx, Gunicorn, Auth0 and Flask
1. Create a DigitalOcean Droplet with Ubuntu 20.04 LTS. Add your ssh key (~/.ssh/id_rsa.pub) to allowed keys.
2. On a command line interface, enter the following command to access the server: ssh root@<server_ip_address>
3. Once in the server, create a new user (__adduser newuser__), and give the new user superuser privileges (__sudo usermod -aG sudo newuser__). This will create a home directory for the new user, where we can store this repository.
4. As root user, redirect to the path ~/../home/newuser. Make a new directory called hackedNews.
5. Install nginx: sudo apt install nginx
6. Create a virtual environment to install flask and gunicorn.
7. In the virtual environment, install flask: pip install flask
8. Install gunicorn: pip install gunicorn
9. Clone the repository into the hackedNews directory mentioned in step 4
10. Update the nginx conf files and the wsgi.py file (gunicorn worker) with your domain name
11. Use an A record on your domain name to point to your digitalocean VM IP address if you are hosting on the web
12. Restart nginx (__sudo systemctl restart nginx__). Then restart gunicorn (__systemctl restart hackedNews.service__) to restart those components of your system that you edited.


## Configuration Files (11/03/2022)
All configuration files are found in config.
hackedNews is our nginx server block including our ssl certificate.
hackedNews.service is our gunicorn worker process.
nginx.conf is our nginx configuration file.
sshd_conf is our ssh configuration.

### Updates & Upgrades
We configured unattended updates and upgrades to automatically happen and the configuration file for updates and upgrades is ../../etc/apt/apt.conf.d/50unattended-upgrades from the python user login point or from /etc/apt/apt.conf.d/50unattended-upgrades in the project home directory.

## Homework 1
## What happens with the command "_curl hacked-news.com_"
![Curl img](https://i.ibb.co/xzmDPVt/Screen-Shot-2022-10-16-at-3-14-42-PM.png)
Initially, curl will require an IP address. In this instance, we provided our domain name, "hacked-news.com". From here, the
domain name will need to be translated into the actual IP address of the server. Initially, curl will use the port 443. This bring us to DNS.
### DNS
1. A DNS request is made and it searches the DNS resolver for the IP address associated with hacked-news.com.
2. For us, the initial server is a Namecheap server that we have setup to redirect to our Ubuntu machine through an A record. This means that when we attempt to reach hacked-news.com, the request is redirected from the intial IP address to the Ubuntu machine IP address. The port 443 (for HTTPS) is used here.
![DNS lookup](https://i.ibb.co/GJD305C/Screen-Shot-2022-10-16-at-3-33-10-PM.png)
### SSL Certificate
1. The SSL certificate is used to keep data secure and verify that we are the owners of hacked-news.com, which helps prevent attackers from creating a fake version of our site.
2. After we have the IP address from the DNS lookup, the browser makes a request for the SSL certificate from the server. If the browser trusts the certificate, it connects to the server.
### Nginx
When this request reaches the Ubuntu server where we have Nginx installed, Nginx will handle this request and verify that it is being done on port 443. If the port is not 443, we have set it up to redirect to port 443 as to not allow HTTP requests. Nginx will communicate with Gunicorn in order to handle packet requests, communicate with multiple web servers, and react to many web requests and distribute the load if necessary. Gunicorn will then make a request to our Flask app, as defined in the config files.
### Flask -> App -> Endpoint py file
Flask will then provide the response to the curl request. It will find the entry point, which in our case is hackedNews.py. It will then server the contents of this file in response to the request corresponding to the proper route. 
![Site image](https://i.ibb.co/HX7hMQ5/Screen-Shot-2022-10-19-at-10-35-52-AM.png)
### Security (updated)
The initial layer of security we have used to secure our application is by protecting our user accounts that can access the server. Both of our users have access to the server strictly through our SSH key authentication. Additionally, we have a firewall enabled to striclty allow the use of port 22 for SSH connections and port 443 for HTTPS connections. Also, we have configured nginx to redirect and only allow HTTPS connections. We have implemented multiple security features into our project thanks to reccomendations from Mozilla Observatory. We implemented a content security policy, cookie prevention, disallowed cross-origin resource sharing, redirect all traffic from HTTP to HTTPS, among other tests. Our score on Mozilla Observatory is a 110/100.

