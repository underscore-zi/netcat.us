<?php include("session.php"); ?>

<!DOCTYPE html>
<html>
<head>
  <link href="style.css" rel="stylesheet" type="text/css" />
</head>
<body>
  <?php include("toolbar.php"); ?>
  <div class="page">
    <h1>Longegg Research Center</h1>
    <div class="box">
      <div class="header">
        Remote Lab Access
      </div>
      <br>
      <div class="smalltext">
        Select your command script to upload
      </div>
      <br>
      <form class="center" action="scriptupload.php" method="post" enctype="multipart/form-data">
        <input type="file" name="fileToUpload" id="fileToUpload">
        <input type="submit" value="Upload Script" name="submit">
      </form>
      <p>
      <div class="smalltext">
        Maximum file size: 10 KB
      </div>
      </p>
      <p>
      <div class="smalltext">
        To run your script, use the page <a href="scriptrun.php">here</a>
      </div>
      </p>
      <p>
      <div class="header">
        Available Commands
      </div>
      </p>
      <table class="commands center">
        <tr>
          <td><b>Command</b></td> <td><b>Arguments</b></td>  <td><b>Description</b></td>
        </tr><tr>
          <td>ECHO</td> <td>[string]</td> <td>Display a line of text</td>
        </tr><tr>
          <td>LISTDIR</td> <td></td>  <td>List files</td>
        </tr><tr>
          <td>READ</td> <td>[filename]</td> <td>Print the contents of a file</td>
        </tr><tr>
          <td>DATE</td> <td></td> <td>Print the current date</td>
        </tr><tr>
          <td>TIME</td> <td></td> <td>Print the current time</td>
        </tr><tr>
          <td>#</td> <td></td>  <td>Ignore this line (comment)</td>
        </tr><tr>
          <td>ELEVATE</td> <td></td>  <td>Elevate privelages (WARNING: Admin only)</td>
        </tr>
      </table>
    <div class="smalltext">
    <p>
      Command scripts should have one command per line, at the start of the line<br>
      All commands are case sensitive<br>
      Any invalid commands will be skipped during execution
    </p>
    </div>
  </div>
</div>
</body>
</html>

