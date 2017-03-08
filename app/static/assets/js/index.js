$(document).ready(function () {
	function getCookie(key) {
		var cookies	= decodeURIComponent(document.cookie),
			decoded	= cookies.split("; ");

		var needle = key + "=";
		for (var i = 0; i < cookies.length; i++) {
			var cookie = decoded[i];

			if (cookie && cookie.startsWith(needle)) {
				return cookie.slice(needle.length);
			}
		}

		return false;
	}
	
	var username	= getCookie('name'),
		container	= $('span#username');

	if (username && container) {
		container.text(username.replace(/"/g, ''));
	}
});
