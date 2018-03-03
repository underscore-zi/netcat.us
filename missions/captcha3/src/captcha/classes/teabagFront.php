<?php

class teabagFace {
	
	private $method = 'file' ;
	private $height = 150 ;
	private $width = 300 ;
	private $code = '' ;
	private $surface = '' ;
	private $font = '' ;
	private $basePath = '';
	private $savePath = '';
	private $bgColor = '';
	private $fgColor = '';
	
	
public function __construct ($cde='---') {
		//init code written on captcha
		$gc = 'AHKMNPSTXYZbdhkmstwxz2349' ;
		$l = strlen ( $gc ) - 1 ;
		if($cde=='---'||$cde='')$this->code = $gc [ rand ( 0, $l ) ] . $gc [ rand ( 0, $l ) ] . $gc [ rand ( 0, $l ) ] ;
		//include required files
		$this->basePath = dirname ( __FILE__ ) . '/..' ;
		
		require_once $this->basePath . '/classes/fontLoader.php' ;
		require_once $this->basePath . '/classes/imageMask.php' ;
		require_once $this->basePath . '/classes/surfaceCreator.php' ;
		require_once $this->basePath . '/classes/model.php' ;
		require_once $this->basePath . '/classes/point.php' ;
		require_once $this->basePath . '/classes/camera.php' ;
		require_once $this->basePath . '/classes/color.php' ;
		
		//init font
		$this->font = FontLoader::LoadFont ( $this->basePath . '/lib/fonts/' ) ;
		$this->bgColor = new Color(255, 255, 255);
	
	}
	
	public function generate () {
		$textmask = new MaskImage ( $this->code, $this->font ) ;
		
		$target = new Point ( $textmask->getIw () / 2, $textmask->getIh () / 2, 0 ) ;
		
		//@TODO make selection of surface generation method (future)
		//$surface = new FlatSurfaceCreator($textmask);
		$surface = new SimpleWaveSurfaceCreator ( $textmask ) ;
		//not implemented $surface = new StandardShapeSurfaceCreator($textmask);
		//not implemented $surface = new ComplexWaveSurfaceCreator($textmask);
		

		$model = $surface->getModel () ;
		
		$camera = new Camera ( $target ) ;
		$camera->setZoom(1.6);
		$camera->setSavePath ( $this->savePath ) ;
		$camera->setRandPosition ( $textmask ) ; //this is needed to place camera well
		$camera->makeProjection ( $model ) ;
		$camera->setFgColor($this->fgColor);
		$camera->setBgColor($this->bgColor);
		
		return $camera->makePicture ( $this->width, $this->height, $model, $this->method , $this->bgColor) ; //modes: file, stream, raw
	}
	
	
	/**
	 * @param unknown_type $fgColor
	 */
	public function setFgColor ( $fgColor ) {
		$this->fgColor = $fgColor ;
	}

	/**
	 * @param unknown_type $bgColor
	 */
	public function setBgColor ( $bgColor ) {
		$this->bgColor = $bgColor ;
	}
	/**
	 * @return string
	 */
	public function getCode () {
		return $this->code ;
	}
	/**
	 * @return string
	 */
	public function getBasePath () {
		return $this->basePath ;
	}
	/**
	 * @param string $savePath
	 */
	public function setSavePath ( $savePath ) {
		$this->savePath = $savePath ;
	}
	
	/**
	 * @param string $code
	 */
	public function setCode ( $code ) {
		$this->code = $code ;
	}
	
	/**
	 * @param int $height
	 */
	public function setHeight ( $height ) {
		$this->height = $height ;
	}
	
	/**
	 * @param int $method
	 */
	public function setMethod ( $method ) {
		$this->method = $method ;
	}
	
	/**
	 * @param string $surface
	 */
	public function setSurface ( $surface ) {
		//@TODO it will be implemented when more surfaces will be available
		$this->surface = $surface ;
	}
	
	/**
	 * @param int $width
	 */
	public function setWidth ( $width ) {
		$this->width = $width ;
	}
}

?>