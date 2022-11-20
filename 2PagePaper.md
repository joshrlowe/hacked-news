Trevor Fagan
Josh Lowe
Python Project
Gitlab Link: https://gitlab.com/trevorfagan77/python-project
Website: https://www.hacked-news.com/
Zoom meeting sheet: https://docs.google.com/spreadsheets/d/1KNlvhTw1TmAgTb6RmmtveCS-q62Dzip6fsDflExQIpM/edit?usp=sharing
PyLint Score:
![Pylint Score](https://ibb.co/3sG8PjL)
Unit Test Coverage:
![Unit Test Coverage](https://ibb.co/523WZWm)
Tutorial Video Link: https://youtu.be/gjzH2Qnvuacs

Project Description: Tools that We Used in this Project
1. Cron - Cron was used to perform our updates on our database by fetching from the HackerNews API. We have it set up so that every minute the crontab asynchronously runs our update script that fetches new articles for the API and deletes any articles that are older than twenty-four hours old. 
2. NGINX - We configured NGINX as a reverse proxy, redirecting incoming traffic from port 80 to port 443 in an effort to make our web application more secure.
3. Gunicorn - Gunicorn was used to send data to Nginx so that it could be served to the browser. Gunicorn was responsible for updating all of our files and making sure the content on the page was up to date.
4. Flask - Flask was our backend for this project where we handled routing, database connections, and any other background processes necessary. Through Flask we also set up a connection to the HackerNews API and enabled users to login through Auth0.
5. Certbot - Certbot was used to obtain an SSL certificate to verify the authenticity of our site. Certbot was set to automatically renew and enabled our site to run on HTTPS, with a secure connection. 
6. Namecheap - We obtained our domain name (hacked-news.com) from namecheap.com. This was then redirected through an A record to point to our digital ocean Ubuntu server.
7. Digital Ocean - We used Digital Ocean to create a droplet, the server where we made our project. The server was an Ubuntu 22.04 server. We also used Digital Ocean to store a snapshot of our fully-functioning Ubuntu server so that it can be easily redeployed if necessary.
8. UFW - UFW is our firewall and it allows connections on port 22, 80, and 443.
9. SSH - SSH Key Authentication was used to grant users access to our Ubuntu 22.04 server.
The Ubuntu 22.04 server could only be connected to using keys, as password authentication was disabled.
10. SQLite3 - SQLite3 was used as the database for our project. SQLite3 is a sql based DBMS and writes to a file stored on our machine.
11. PyTest - PyTest was used to create functional and unit tests for our project. We also used the coverage package to generate the testing coverage of our website.
12. HackerNews API - This is the meat and potatoes of our site where we fetch news articles from. In the background of our site we are fetching 50 new news articles every minute and comparing them to what we already have in our database to have the most up to date news.
13. Auth0 - Auth0 was used for user authentication and logging in. We use the Auth0 session through the website to check if a user is logged in and to display user-specific results from the database depending on if the user is an admin or not.

