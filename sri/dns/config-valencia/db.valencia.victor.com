;
; BIND data file for local loopback interface
;

$TTL	604800
@	IN	SOA	admin.victor.com. root.victor.com. (
			      2		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@			IN	NS	admin.valencia.victor.com.
@			IN	A	192.168.0.100
admin.valencia		IN	A	192.168.0.100

pc2		IN	A	192.168.0.3	
pc3		IN	A	192.168.0.4


