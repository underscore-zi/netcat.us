<?php

//Do not bruteforce this site, you can crack this with 100% accuracy.

function setck($name,$val) {
	setcookie($name, $val);
	$_COOKIE[$name] = $val;
}

function resetGame() {
	setck("rounds", 1);
	$_SESSION['c2_time'] = time();
	$_SESSION['c2_streak'] = 0;
	$_SESSION['c2_wrong'] = 0;
}

if(isset($_POST['source'])) {
	echo "<pre>";
	echo htmlentities(preg_replace('/FLAG{([a-z0-9_]+)}/i','FLAG{figure_it_out}', file_get_contents(__FILE__)));
	echo "</pre>";
	die();
}

session_start();
if(!isset($_SESSION['c2_time'])) $_SESSION['c2_time'] = time();
if(!isset($_SESSION['c2_streak'])) $_SESSION['c2_streak'] = 0;
if(!isset($_SESSION['c2_wrong']))  $_SESSION['c2_wrong'] = 0;
if(!isset($_COOKIE['rounds'])||!is_numeric($_COOKIE['rounds'])||$_COOKIE['rounds'] >= PHP_INT_MAX) {	
	setck("rounds", 1);
}
if($_SESSION['c2_streak'] >= $_COOKIE['rounds']) {
	$_SESSION['c2_streak'] = 0; //No cheating!
}

if(isset($_POST['reset'])) {
	//Give the poor unlucky players a way to restart after the game gets too hard
	resetGame();
}

if(time()-$_SESSION['c2_time'] > 600) {
	//You have to finish within 10minutes or the game restarts
	resetGame();
}



//Make it more difficult with every round
$rnd =  mt_rand(1, $_COOKIE['rounds']);
//Add some randomness
srand(time());
$rnd &= rand();
$CURRENT_CAPTCHA = $rnd;


//Create the new bot-readable CAPTCHA
$im = imagecreate(100, 15);
$bg = imagecolorallocate($im, 255, 255, 255);
$textcolor = imagecolorallocate($im, 0, 0, 0);
for($i=0;$i<50;$i++) {
	$color = ($i%2)?$bg:$textcolor;
	imagestring($im, rand(1,6), rand(1,6), 0, decbin($CURRENT_CAPTCHA), $color);
}
imagegif($im, 'captcha.gif');
imagedestroy($im);



if(isset($_POST['guess'])) { 
	$guess = (int)$_POST['guess'];
	setck("rounds", ++$_COOKIE['rounds']);
	
	if(md5($rnd) == md5($_POST['guess'])) {
		$_SESSION['c2_streak']++;
		echo "That was the correct answer.<br/><br/>";
	} else {
		$_SESSION['c2_streak']--;
		$_SESSION['c2_wrong']++;
		if($_SESSION['c2_wrong'] > 10) {
			resetGame();
		}
		echo "Incorrect.<br/><br/>";
		sleep(1);
	}
	if($_SESSION['c2_streak'] >= 100) {
		echo "FLAG{U_R_NOT_HUM4N}";
		die();
	}
}
echo '<h1>Robot Command Center</h1>';
echo 'Status: '. $_COOKIE['rounds'] . ':' . $_SESSION['c2_streak'] . ':' . $_SESSION['c2_wrong'] . '<hr/>';
?>
<style>
 .captcha {
 	border-width:1px;
 	border-style:solid;
 }
</style>

Please prove you are a robot by solving this captcha 100 times with atleast 90% success rate.
<form method="POST">
<img src="captcha.gif?id=<?=time()?>"/>
<input type="text" name="guess" /><input type="submit" value="Solve!"/>
</form>

<form method="POST">
<input type="submit" name="reset" value="Reset!"/>
</form>
<form method="POST">
<input type="submit" name="source" value="View Source!"/>
</form>

