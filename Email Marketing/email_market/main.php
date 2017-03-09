<?php
use \google\appengine\api\mail\Message;

$file_handle = fopen("email_list.csv", "r");
$i=0;
$body = file_get_contents('body.html');

while (!feof($file_handle) ) {
$emailadd = fgetcsv($file_handle, 1024);
$i++;
if($i!=1)
try
{
	$message = new Message();
	$message->setSender("vivekjwl@gmail.com");
	$message->addTo($emailadd[1]);
	$message->setSubject("Subject of mail");
	$message->setHtmlBody($body);
	$message->send();
} 
print_r("Mail Send");
catch (InvalidArgumentException $e) {
	print_r("Message cannot be send", $e);
}

}

fclose($file_handle);


?>