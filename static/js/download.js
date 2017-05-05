(function () {
	var download_button		= document.getElementById("download"),
		download_section	= document.getElementById("downloadable");

	function canvas2png(canvas) {
    	var url = canvas.toDataURL('image/png');
    	window.open(url, "takethejuice_timeline.png");
	}

	download_button.addEventListener("click", function(e) {
		e.preventDefault();
		html2canvas(download_section, {
			background: "#ffffff",
			useCORS: true,
			onrendered: canvas2png
		});
	})
})();