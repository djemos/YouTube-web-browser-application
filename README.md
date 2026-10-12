# YouTube web browser application
A YouTube web browser application (or YouTube browsing and management tool) is a type of specialized web application that allows users to search for, stream, and download YouTube content via an alternative, customized interface, separate from the platform's official website. You can see the application running here: [YouTube Browser App](https://meraklis.ddnsfree.com/ytapp/)

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


