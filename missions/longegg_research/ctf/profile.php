<?php include("session.php"); ?>
<!DOCTYPE html>
<html>
<head>
  <link href="style.css" rel="stylesheet" type="text/css" />
</head>
<body>
  <?php include("toolbar.php"); ?>
  <div class="page">
    <h1>Profile settings</h1>
    <div class="box">
      <div class="header">
        Set avatar image
      </div>
      <br>
      <div class="smalltext">
        Select a new profile image to upload
      </div>
      <br>
      <form action="avatarupload.php" method="post" enctype="multipart/form-data">
        <input type="file" name="fileToUpload" id="fileToUpload">
        <input type="submit" value="Upload image" name="submit">
      </form>
      <p>
      <div class="smalltext">
        Maximum filesize: 200 KB
      </div>
      </p>
    </p>
    </div>
  </div>
</div>
</body>
</html>

