<?php if(@$_COOKIE['pass']=='OMGTHEWORLDISENDING') { ?>
<!DOCTYPE html>
<html>
	<head>
		<title>Final Stage</title>
	<head>
	<body>
		<p>Hey, it's Itzel again. I guess if you're reading this, you're pretty okay at web exploitation because my server was really secure. Before I give you this flag, answer this question.</p>
		<form action="finalauth.php" method="post" name="finalquestions">
            <div>
				<br>
                 If you're reading this and you're not me, I must have died, what month did I die? <input type="text" name="month" value="" />
                <input type="submit" value="Submit"/>
            </div>
        </form>
<?php } ?>