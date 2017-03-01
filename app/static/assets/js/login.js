$(document).ready(function () {
	var server = "http://localhost:5000";

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

						window.ga('set', 'dimension1', data.id);
						window.ga('set', 'dimension2', data.email);

						$('#userid-input').val(data.id);
						$('#accesstoken-input').val(data.accesstoken);
						$('#email-input').val(data.email);
						$('#login-form form').submit();
					});
				}
			}, {scope: "public_profile, email", return_scopes: !0});
		});
	}
});
