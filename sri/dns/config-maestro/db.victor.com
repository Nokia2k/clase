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
@		IN	NS	admin.victor.com.
@		IN	NS	esclavo.victor.com.
admin		IN	A	192.168.0.2
server		IN	CNAME	admin.victor.com.
esclavo		IN	A	192.168.0.3	
pc2		IN	A	192.168.0.3	
pc3		IN	A	192.168.0.4
