# Readme File
### COP 4521 - Python 
### Group Number: 23
### Josh Lowe (jrl19@fsu.edu) and Trevor Fagan (taf20@fsu.edu)

## How to "curl hacked-news.com"
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
### Security
The initial layer of security we have used to secure our application is by protecting our user accounts that can access the server. Both of our users have access to the server strictly through our SSH key authentication. Additionally, we have a firewall enabled to striclty allow the use of port 22 for SSH connections and port 443 for HTTPS connections. Also, we have configured our Nginx file to redirect and only allow HTTPS connections. 
