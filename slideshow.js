(function() {
    
	var img_element;
    var image_list = ["ball.jpg","barbi.jpg","blocks.jpg","car.jpg","doll.jpg","jump.jpg","ninja.jpg", "transformers.jpg"];
    var current_image_index = 0;
    var interval = 2000;
	
	document.addEventListener('DOMContentLoaded', init, false);
	
	function init() {
		
		img_element = document.getElementById("slideshow");
		setInterval(goto_image,2000);
	}
    function goto_image() {
	    img_element.src = image_list[current_image_index++%image_list.length];
	}
	
        
})();
