/**
 * Created by lucas.menendez on 16/5/17.
 */
$(document).ready(function () {
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

						window.ga('send', 'event', 'auth', 'login', data.email);

						$('#userid-input').val(data.id);
						$('#accesstoken-input').val(data.accesstoken);
						$('#name-input').val(data.name);
						$('#email-input').val(data.email);
						$('form#login-form').submit();
					});
				}
			}, {scope: "public_profile, email", return_scopes: !0});
		});
	}
});
