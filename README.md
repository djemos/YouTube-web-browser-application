# YouTube web browser app
A YouTube web browser app (or YouTube browsing and management tool) is a type of specialized web application that allows users to search for, stream, and download YouTube content via an alternative, customized interface, separate from the platform's official website.  

These have to be installed locally  
to install  
sudo pip3 install fastapi uvicorn yt-dlp  
to uninstall  
sudo pip3 uninstall -y fastapi uvicorn yt-dlp  

Copy server.py and index.html in /srv/httpd/htdocs/ytapp/ folder 
type  
sudo chmod -R apache:apache /srv/httpd/htdocs/ytapp/ 

On apache need a virtual host with ssh listen to port 443 and these  
    
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
  
#############################
<img width="1918" height="1048" alt="Image" src="https://github.com/user-attachments/assets/b117d3bd-6222-47da-982d-dafb7b0315a2" />

<img width="1918" height="1048" alt="Image" src="https://github.com/user-attachments/assets/74116445-9a97-4f4f-ba7e-da0882f2fa51" />

<img width="1918" height="1048" alt="Image" src="https://github.com/user-attachments/assets/2a03516f-8c77-450d-8071-dd71ff649b2a" />
	
