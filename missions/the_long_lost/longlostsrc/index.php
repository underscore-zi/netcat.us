<!DOCTYPE html>
<html>
	<head>
		<title>Stage 1</title>
		<script>
			var p455 = '%77%68%30%30%2c%30%62%66%75%35%63%34%37%31%30%6e%21';
			function check(){
				var 1npu7 = prompt('Gimme that pass: ');
				if (1npu7 == unescape(p455)) {
					alert('thats the one!');
				} else {
					alert('nope');
				}
			}	
		</script>
	<body>
		You've stumbled upon an ancient website from the previous human race to inhabit Earth. They've left this puzzle that seems to lead to some kind of "flag." See if you can log in.
		<form action="stage2.php" method="post" name="authform">
            <div>
				<br>
                <input disabled type="text" name="auth" value="" />
                <input disabled type="submit" value="Enter pass"/>
            </div>
        </form>
	</body>
</html>