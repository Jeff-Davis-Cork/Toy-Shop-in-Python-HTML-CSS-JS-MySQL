(function() {
    
    var interval = 1000;
	
	document.addEventListener('DOMContentLoaded', init, false);
	
	function init() {
		
		setInterval(redirect,4000);
	}
    function redirect() {
	    window.location.href = "http://cs1.ucc.ie/~jd23/cgi-bin/lab7/index.html";

	}
	
        
})();
