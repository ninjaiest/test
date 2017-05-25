select a.name "DB Name", 
       e.global_name "Global Name", 
       c.host_name "Host Name", 
       c.instance_name "Instance Name" , 
       DECODE(c.logins,'RESTRICTED','YES','NO') "Restricted Mode",
       a.log_mode  "Archive Log Mode"  
FROM v$database a, v$version b, v$instance c,global_name e  
WHERE b.banner LIKE '%Oracle%';