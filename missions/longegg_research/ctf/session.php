<?php
  session_start();
  if (!file_exists($_SESSION["dir"])){
    $_SESSION["dir"] =  "data/" . md5(session_id());
    mkdir($_SESSION["dir"]);
    copy("data/script.cmd",$_SESSION["dir"] . "/script.cmd");
    copy("data/userimage.jpg",$_SESSION["dir"] . "/userimage.jpg");
    $_SESSION["img"] = "userimage.jpg";
    $_SESSION["hash"] = "84e1e7dc935a639bf01fed48c4bbed94";
  }
?>
