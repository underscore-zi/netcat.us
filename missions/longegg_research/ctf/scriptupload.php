<?php
include("session.php");
$uploadOk = 1;
$err = "";

// Check file size
if ($_FILES["fileToUpload"]["size"] > 10000) {
    $err = "Sorry, your file is too large.";
    $uploadOk = 0;
} else {
    $script = fopen($_FILES["fileToUpload"]["tmp_name"],"r");
    if ($script) {
        while (($line = fgets($script)) !== false) {
            $cmd = preg_split('/\s+/', $line);
            if (strcmp(trim($cmd[0]),"ELEVATE") == 0) {
                $err .= "Illegal command: ELEVATE\n";
                $err .= "You do not have the required permission level to use this command\n";
                $err .= "Your script was not uploaded";
                $uploadOk = 0;
                break;
            }
        }
    } else {
        $err = "Sorry, there was an error uploading your file.";
    }
}

if ($uploadOk){
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $_SESSION["dir"] . "/script.cmd" )) {
	// Script uploaded, now to save the hash for tamper checking
	$_SESSION["hash"] = md5_file($_SESSION["dir"] . "/script.cmd");
    } 
}
?>

<!DOCTYPE html>
<html>
<head>
  <link href="style.css" rel="stylesheet" type="text/css" />
</head>
<body>
  <?php include("toolbar.php"); ?>
  <div class="page">
    <div class="box">
      <div class="header">
        <?php
          if ($uploadOk) {
            echo "Upload successful";
          } else {
            if ($err) {
              echo "An error occured";
            } else {
              echo "An unknown error occured";
            }
          }
        ?>
      </div>
      <div class="smalltext">
        <?php
          if ($uploadOk) {
            echo "Click <a href=\"scriptrun.php\">here</a> to run your script";
          } else {
            echo "<div class=\"error\"><pre>";
            if ($err) {
              echo $err;
            } else {
              echo "Please try <a href=\"index.php\">uploading</a> again";
            }
            echo "</pre></div>";
            echo "<br><div class=\"smalltext\">";
            echo "Click <a href=\"index.php\">here</a> to try again";
          }
        ?>
      </div>
      <br>
    </div>
  </div>
</div>
</body>
</html>

