<?php

class MaskImage{

	private $iw;
	private $ih;
	private $image;
	
	private $fontSize = 70;//you can play with this
	
	private $wHalfBorder = 30;
	private $hHalfBorder = 30;

	public function MaskImage($code, $font){
		$maskcolor= 0; //black
		
		//60 - is a magic fontsize, 0 - means no rotation
		$bbox=imagettfbbox ($this->fontSize, 0, $font, $code);

		$this->image = imagecreatetruecolor ($bbox[2]+2*$this->hHalfBorder, -$bbox[5]+2*$this->wHalfBorder);
		
		//bg is blue....
		imagefill ($this->image, 10 , 10, 16777215 );
		
		//write it down
		imagettftext ($this->image, $this->fontSize, 0, $this->hHalfBorder, -$bbox[5]+$this->wHalfBorder, 0, $font, $code);

		//borders arounf the image
		$this->iw = $bbox[2]+2*$this->hHalfBorder;
		$this->ih = -$bbox[5]+2*$this->wHalfBorder;
		
	}
	
	public function getIw(){
		return $this->iw;
	}
	
	public function getIh(){
		return $this->ih;
	}

	public function getImage(){
		return $this->image;
	}
}



?>