<?php 
if(@$_COOKIE['pass']=='OMGTHEWORLDISENDING') {
	$month = "";
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
			$month = $_POST["month"];
			if (strtolower($month) == "december") {
				echo "Your flag is FLAG{ayy_web_exploitation_can_be_fun}";
			} 
	}
}
?>