<?php 
if(!isset($_COOKIE['pass'])) {
	setcookie('pass', 'set me');
}
if($_COOKIE['pass']=='OMGTHEWORLDISENDING') {
	?>
	
<!DOCTYPE html>
<html>
	<head>
		<title>Mah Lounge</title>
	</head>

	<body>
		<p>With the world about the end and all, I've been slacking on my PHP. I think the flag is in final.php or something. Cheers!</p>
		
	</body>
</html> <?php
}
?>

