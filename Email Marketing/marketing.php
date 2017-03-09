<?php

$file_handle = fopen("email_list.csv", "r");

while (!feof($file_handle) ) {
$line_of_text = fgetcsv($file_handle, 1024);
print $line_of_text[0] . $line_of_text[1]. "<BR>";
}

fclose($file_handle);

?>