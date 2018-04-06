  <div id="toolbar">
    <div class="userthing">
      <a href="profile.php">
      <img src="<?php
        echo $_SESSION["dir"] . "/" . $_SESSION["img"];
      ?>" height="48" width="48" alt="Failed to load image" title="Click to change profile image"></a>
      Logged in as user2708
    </div>
    <ul class="navtab">
        <li>
            <a <?php if(basename($_SERVER['PHP_SELF'])=='index.php'){ echo "id=\"curpage\"";} ?> href="index.php">Upload Script</a>
        </li>
        <li>
            <a <?php if(basename($_SERVER['PHP_SELF'])=='scriptrun.php'){ echo "id=\"curpage\"";} ?> href="scriptrun.php">Run Script</a>
        </li>
        <li>
           <a <?php if(basename($_SERVER['PHP_SELF'])=='profile.php'){ echo "id=\"curpage\"";} ?>href="profile.php">Profile</a>
        </li>
    </ul>
  </div>
