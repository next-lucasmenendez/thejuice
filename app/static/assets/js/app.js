$(document).ready(function () {
	var server = "http://localhost:5000";

	window.fbAsyncInit = function() {
		FB.init({ 
			appId: '197401140741778',
			xfbml: true,
			version: 'v2.5'
		});
	};

	(function(d, s, id){
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) {return;}
		js = d.createElement(s); js.id = id;
		js.src = "//connect.facebook.net/en_US/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));

	var deleteCookies = function() {
		var cookies = document.cookie.split(";");

		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i];
			var eqPos = cookie.indexOf("=");
			var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;

			document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
		}
	}

	var login_btn = $("#login-btn");
	if (login_btn) {
		login_btn.on('click', function(event) {
			event.preventDefault();
			FB.login(function (response) {
				if (response.authResponse !== null) {
					FB.api('/me', {fields: 'name, email'}, function(profile) {
						var data = {
							id: profile.id,
							email: profile.email,
							name: profile.name,
							accesstoken: response.authResponse.accessToken
						}

						$('#userid-input').val(data.id);
						$('#accesstoken-input').val(data.accesstoken);
						$('#login-form form').submit();
					});
				}
			}, {scope: "public_profile, email", return_scopes: !0});
		});
	}
});
