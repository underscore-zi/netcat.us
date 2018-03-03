<?php

session_start();
$FLAG = 'FLAG{BUT_C4CHING_IS_G00D_4_PERFORMANCE}';

//Display the source
if(isset($_GET['source'])) {
	$content = isset($_GET['raw'])?'<pre>'.htmlentities(file_get_contents(__FILE__)).'</pre>':highlight_file(__FILE__, true);
	echo preg_replace('/FLAG{([a-z0-9_]+)}/i','FLAG{solve_to_see}', $content);
	die();
}


if(isset($_POST['captcha'])) {
	$errors = [];
	$time = $_SERVER["REQUEST_TIME_FLOAT"]-$_SESSION['captcha_time'];
	$input = $_POST['captcha'];
	if(strlen($input)!=5) $errors[] = 'Provided solution is too short.';
	if(!isset($_SESSION['captcha_file'])) $errors[] = 'You have not yet viewed a captcha to solve.';
	if($time > 0.5) $errors[] = 'You were too slow, you must solve the captcha in half a second or less.';
	
	//Only check the captcha itself if they have made it this far without errors.
	if(empty($errors)) {
		$captchas = json_decode(file_get_contents('./cache/captchas.json'),true);
		if($input != $captchas[$_SESSION['captcha_file']]) $errors[] = 'Incorrect captcha.';
		else {
			echo $FLAG;
			die();
		}
	}

	//$_SERVER["REQUEST_TIME_FLOAT"]
	foreach($errors as $e) {
		echo $e . '<br />';
	}

}


//Displays a random captcha image and sets the _SESSION appropiately
if(isset($_GET['image'])) {
	//Make sure the image doesn't get cached by the browser
	header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
	header("Cache-Control: no-store, no-cache, must-revalidate");
	header("Cache-Control: post-check=0, pre-check=0", false);
	header("Pragma: no-cache");
	header("Content-type: image/png");
	//Choose a random file out of the cache
	$files = glob('./cache/*.png');
	$fn = $files[array_rand($files)];
	$_SESSION['captcha_file'] = $fn;
	$_SESSION['captcha_time'] = microtime(true);
	echo file_get_contents($fn);
	die();
}


//Generating these captchas on the fly is too slow on the server
//Instead I just generate a big cache of them to serve from on first load
if(!file_exists('./cache/captchas.json')) {
	$captchas = [];
	if(!file_exists('./cache/')) {
		mkdir('./cache');
		file_put_contents('./cache/.htaccess', 'deny from all');
	}
	include_once('./captcha/classes/teabagFront.php');
	for($i=0;$i<100;$i++) {
		$c = chr(mt_rand(33,126)).chr(mt_rand(33,126)).chr(mt_rand(33,126)).chr(mt_rand(33,126)).chr(mt_rand(33,126));
		$captcha = new teabagFace();
		$captcha->setSavePath('./cache/');
		$captcha->setMethod('file');
		$captcha->setWidth(500);
		$captcha->setHeight(200);
		$captcha->setCode($c);
		$fn = $captcha->generate();
		$captchas['./cache/' . $fn] = $c;
	}
	file_put_contents('./cache/captchas.json',json_encode($captchas));
}

?>
<center>
<h1>3d Captcha</h1>
<form method="POST">
	<img src="?image" /><br />
	<input type="text" placeholder="captcha" name="captcha" />
	<input type="submit" value="Submit!" />
</form>
<a href="?source">Click here</a> to view the PHP source.
</center>