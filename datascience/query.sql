alter view nameemailadd as
select substring_index(name,',','1')as nam ,substring_index(name,',','-1')as email ,SUBSTR(name, 
    LOCATE(',',name)+1, 
      (CHAR_LENGTH(name) - LOCATE(',',REVERSE(name)) - LOCATE(',',name)))as inbetweennameemails
FROM informs.author