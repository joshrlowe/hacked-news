# Readme File
## How to "curl hacked-news.com"
![Image](https://i.ibb.co/xzmDPVt/Screen-Shot-2022-10-16-at-3-14-42-PM.png)
Initially, curl will require an IP address. In this instance, we provided our domain name, "hacked-news.com". From here, the
domain name will need to be translated into the actual IP address of the server. This bring us to DNS. 
### DNS
1. A DNS request is made and it searches the DNS resolver for the IP address associated with hacked-news.com.
2. For us, the initial server is a Namecheap server that we have setup to redirect to our Ubuntu machine through an A record. This means that when we attempt to reach hacked-news.com, the request is redirected from the intial IP address to the Ubuntu machine IP address.
### Nginx
When this request reaches the Ubuntu server where we have Nginx installed, Nginx will handle this request. Nginx will communicate with Gunicorn in order to handle packet requests, communicate with multiple web servers, and react to many web requests and distribute the load if necessary. Gunicorn will then make a request to our Flask app, as defined in the config files.
### Flask -> App -> Endpoint py file
Flask will then provide the response to the curl request. It will find the entry point, which in our case is hackedNews.py. It will then server the contents of this file in response to the request corresponding to the proper route. 
