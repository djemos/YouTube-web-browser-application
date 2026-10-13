# YouTube web browser application
YouTube web browser application (or YouTube browsing and management tool) is a type of specialized web application that allows users to search for, stream, and download YouTube content via an alternative, customized interface, separate from the platform's official website.  

You can see the application running here: [YouTube Browser Appication](https://meraklis.ddnsfree.com/ytapp/) 💡 *(Hint: Right-click or Ctrl+Click to open in a new tab!)* 


These must be installed locally  
for installation  

	sudo pip3 install fastapi uvicorn yt-dlp  
	
for uninstallation  

	sudo pip3 uninstall -y fastapi uvicorn yt-dlp  


Copy server.py and index.html to the /srv/httpd/htdocs/ytapp/ folder,  

then type  
 

	sudo chmod -R apache:apache /srv/httpd/htdocs/ytapp/ 


In Apache, you need an SSH virtual host listening on port 443, as follows. Replace `your_dnsname.ddnsfree.com` with your own dnsfree domain name and use your own Let's Encrypt certificate keys.
    
	Listen 443  
	SSLCipherSuite HIGH:MEDIUM:!MD5:!RC4:!3DES  
	SSLProxyCipherSuite HIGH:MEDIUM:!MD5:!RC4:!3DES  
	SSLHonorCipherOrder on   
	SSLProtocol all -SSLv3  
	SSLProxyProtocol all -SSLv3  
	SSLPassPhraseDialog  builtin  
	SSLSessionCache        "shmcb:/var/run/ssl_scache(512000)"  
	SSLSessionCacheTimeout  300  
	  
	<VirtualHost *:443>  
	DocumentRoot "/srv/httpd/htdocs/"  
	ServerName your_dnsname.ddnsfree.com:443  
	ErrorLog "/var/log/httpd/your_dnsname.ddnsfree.com-error_log"  
	CustomLog "/var/log/httpd/your_dnsname.ddnsfree.com-access_log" common  
  
	Alias /.well-known/acme-challenge/ /var/www/dehydrated/  
	<Directory /var/www/dehydrated/>  
		Options None  
		AllowOverride None  
		Require all granted  
	</Directory>  
	
    SSLEngine on  
    SSLCertificateFile      /etc/dehydrated/certs-letsencrypt/your_dnsname.ddnsfree.com/cert.pem  
    SSLCertificateKeyFile   /etc/dehydrated/certs-letsencrypt/your_dnsname.ddnsfree.com/privkey.pem  
    SSLCertificateChainFile /etc/dehydrated/certs-letsencrypt/your_dnsname.ddnsfree.com/chain.pem  
	RewriteEngine On  
    RewriteRule ^/ytapp$ /ytapp/ [R=301,L]  
    <Location /ytapp>  
        ProxyPass http://127.0.0.1:8090  
        ProxyPassReverse http://127.0.0.1:8090  
    </Location>  
	</VirtualHost>  

Restart httpd  

	  sudo service restart httpd  

you must create this script in /etc/rc.d/rc.ytapp to be executed when system starts  

		#!/bin/sh  
		PIDFILE=/var/run/ytapp.pid  
		LOGFILE=/var/log/ytapp.log  
		PYTHON_SCRIPT=/var/www/htdocs/ytapp/server.py  
		  
		ytapp_start() {  
		  if [ -f $PIDFILE ]; then  
		    echo "The YTApp server is already running (PID: $(cat $PIDFILE))."  
		  else  
		    echo "Starting YTApp server..."  
		    # Change directory to the application folder so it can locate index.html properly  
		    cd /var/www/htdocs/ytapp  
		    nohup python3 $PYTHON_SCRIPT > $LOGFILE 2>&1 &  
		    echo $! > $PIDFILE  
		  fi  
		}  
		
		ytapp_stop() {  
		  if [ -f $PIDFILE ]; then  
		    echo "Stopping YTApp server..."  
		    kill $(cat $PIDFILE)  
		    rm -f $PIDFILE  
		  else  
		    echo "The YTApp server is not running."  
		  fi  
		}  
		  
		ytapp_restart() {  
		  ytapp_stop  
		  sleep 1  
		  ytapp_start  
		}  
		  
		case "$1" in  
		  'start')  
		    ytapp_start  
		    ;;  
		  'stop')  
		    ytapp_stop  
		    ;;  
		  'restart')  
		    ytapp_restart  
		    ;;  
		  *)  
		    echo "Usage: $0 {start|stop|restart}"  
		esac

	

An run rc.ytapp script which run the server.py
  

	sudo service restart ytapp 
  
	
<img width="1918" height="1048" alt="Image" src="https://github.com/user-attachments/assets/b117d3bd-6222-47da-982d-dafb7b0315a2" />  

   
<img width="1918" height="1048" alt="Image" src="https://github.com/user-attachments/assets/74116445-9a97-4f4f-ba7e-da0882f2fa51" />  


<img width="1918" height="1048" alt="Image" src="https://github.com/user-attachments/assets/2a03516f-8c77-450d-8071-dd71ff649b2a" />  


Copyright (C) 2026 Dimitris Tzemos <dijemos@gmail.com>
This program is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, 
either version 2 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License at <http://www.gnu.org/licenses/> for more details.


