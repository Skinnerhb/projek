function infor(eve, tabname) {
	var i, tabcon, tablin;
	
	tabcon = document.getElementsByClassName("tabcontent");
	for (i = 0; i< tabcon.length; i++) {
		tabcon[i].style.display = "none";
	}
	
	tablin = document.getElementsByClassName("tablinks");
	for (i = 0; i< tablin.length; i++) {
		tablin[i].className = tablin[i].className.replace(" active", "");
	}
	
	document.getElementById(tabname).style.display = "block";
	eve.currentTarget.className += " active";
	
}
