<?php
	$uname = "";
	$pass = "";
	
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
		$uname = $_POST["uname2"];
		$pass = $_POST["pass2"];
		if(strtolower($uname) == "itzel" and $pass == "iloveyou") {
		if (isset($_POST['submitexploit'])) {
			$exploit = $_POST['exploit'];
			if (strpos($exploit, '../../index') !== false) {
				echo nl2br ("<strong>Stage 4 is located at /tgbyhnujmedc.php<hr> \n \n \n </strong>");
			}
		}
			?> 
			
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Static Code Analysis</title>
</head>
<body>
	<p>Hey, I have this PHP that should read the contents of a file. I think it's secure, can you check?</p>
	<p>Input how you'd read the contents of <?php echo $_SERVER['HTTP_HOST']?>/index.php</p>
	<code>$filetext = file_get_contents($_POST['filename'].'.php');</code><br><br>
	<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
		<input type="hidden" name="uname2" value="Itzel">
		<input type="hidden" name="pass2" value="iloveyou">
		<input type="text" name="exploit" />
		<input type="submit" value="Submit" name="submitexploit"/>
	</form>
</body>
</html>
			
			<?php
		}
	} 
?>