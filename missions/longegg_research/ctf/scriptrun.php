<?php
include("session.php");
$elevated = FALSE;
$output = "";
$err = "";
if (!file_exists($_SESSION["dir"] . "/script.cmd")) {
  $err = "No script found\nPlease upload a script first";
} else if (strcmp( md5_file($_SESSION["dir"] . "/script.cmd"), $_SESSION["hash"] ) == 0){
    $handle = fopen($_SESSION["dir"] . "/script.cmd", "r");
    if ($handle) {
        while (($line = fgets($handle)) !== false) {
            // Check for comments
            if (substr($line,0,1) != "#"){
                $cmd = preg_split('/\s+/', $line);
                switch ($cmd[0]) {
                    case "ECHO":
                        $output .= substr($line, 5);
                        break;
                    case "LISTDIR":
                          $output .= "flag.txt\nmail.mbox\nnotes.txt\n";
                          break;
                        break;
                    case "READ":
                        $readfile = trim(preg_replace("/[^a-zA-Z0-9\.]/", "", substr($line,5)));
                        switch ($readfile) {
                            case "flag.txt":
                                if ($elevated) {
                                    $output .= file_get_contents("flag.txt") . "\n";
                                } else {
                                    $err = "Insufficient permission for file \"flag.txt\". Elevation required";
                                }
                                break;
                            case "notes.txt":
                                $output .= "- Buy Milk\n- Buy Eggs\n- Buy Birthday Cake\n";
                                break;
                            case "mail.mbox":
                                $output .= "From: Admin <admin@lerc>\n";
                                $output .= "To:   All users\n\n";
                                $output .= "I have had several users report that their uploaded scripts had been corrupted\n";
                                $output .= "by unknown means resulting in unwanted changes. As a safety precaution, I have\n";
                                $output .= "begun requiring scripts to have their signatures checked before they can run.\n";
                                $output .= "If your script is blocked from running due to a bad signature, please notify\n";
                                $output .= "me and try re-uploading your script.\n";
                                break;
                            default:
                                $output .= "File not found\n";
                            }
                    case "ELEVATE":
                        $elevated = TRUE;
                        break;
                    case "DATE":
                        $output .= date("Y-m-d"). "\n";
                        break;
                    case "TIME":
                        $output .= date("h:i:s a") . "\n";
                        break;
                }
            }
        }
        fclose($handle);
    } else {
        $err =  "Could not open script";
    }
} else {
    $err = "Script signature differs from originally uploaded file\n". md5_file($_SESSION["dir"] . "/script.cmd") . " != " . $_SESSION["hash"];
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
    <h1>Run Command Script</h1>
    <div class="box">
      <div class="header">
        Console Output
      </div>
      <div class="console"><?php
          if ($err){
            echo "<div class=\"error\">[ERROR] ". htmlspecialchars($err, ENT_QUOTES, 'UTF-8') ."\nExecution aborted</div>";
          } else {
            echo htmlspecialchars($output, ENT_QUOTES, 'UTF-8');
          }
        ?></div>
      <p>
      <div class="smalltext center">
        <button onclick="location.reload();">Run Script Again</button>
      </div>
      </p>
      <p>
      <div class="header">
        Script Contents
      </div>
      </p>
      <p>
      <div class="console"><?php echo htmlspecialchars(file_get_contents($_SESSION["dir"] . "/script.cmd"), ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); ?></div>
      </p>
    </div>
  </div>
</div>
</body>
</html>

