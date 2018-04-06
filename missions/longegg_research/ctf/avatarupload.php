<?php
include("session.php");
$uploadOk = 1;

// Check file size
if ($_FILES["fileToUpload"]["size"] > 200000) {
    $err = "Sorry, your image is too large";
    $uploadOk = 0;
} else {
    if (!exif_imagetype($_FILES["fileToUpload"]["tmp_name"])) {
        $err = "Error: File not an image";
        $uploadOk = 0;
    }
}

if ($uploadOk){
    // Remove previous image
    unlink($_SESSION["dir"] . "/" . $_SESSION["img"]);
    $_SESSION["img"] = trim(preg_replace("/[^a-zA-Z0-9\.]/", "", basename($_FILES["fileToUpload"]["name"])));
    if (!move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $_SESSION["dir"] . "/" . $_SESSION["img"])) {
        $err = "Sorry, there was an error uploading your image";
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
            echo "<br>Click <a href=\"index.php\">here</a> to return to the main page";
          } else {
            echo "<div class=\"error\"><pre>";
            if ($err) {
              echo $err;
            } else {
              echo "Please try <a href=\"profile.php\">uploading</a> again";
            }
            echo "</pre></div>";
            echo "<br><div class=\"smalltext\">";
            echo "Click <a href=\"profile.php\">here</a> to try again";
          }
        ?>
      </div>
      <br>
    </div>
  </div>
</div>
</body>
</html>

