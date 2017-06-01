/**
 * Created by lucas.menendez on 17/5/17.
 */

var app = angular.module('app');

app.controller('loginCtrl', function ($window, $rootScope, $scope, $state, service) {
	$scope.submitLoginForm = function() {
		var config	= {scope: "public_profile, email", return_scopes: !0},
			attrs	= {fields: 'name, email,picture'};

		FB.login(function (response) {
			if (response.authResponse !== null) {
				FB.api('/me', attrs, function(profile) {
					console.log(profile);
					var data = {
						id: profile.id,
						email: profile.email,
						name: profile.name,
						accesstoken: response.authResponse.accessToken,
						picture: profile.picture.data.url
					}

					service.request('POST', '/login', data, true).then(
						function () {
							$window.ga('send', 'event', 'auth', 'login', data.email);

							localStorage.setItem('id', data.id);
							localStorage.setItem('name', data.name);
							localStorage.setItem('email', data.email);
							localStorage.setItem('accesstoken', data.accesstoken);
							localStorage.setItem('picture', data.picture);

							$state.go('base.search');
						},
						function (error) {
							$rootScope.$broadcast('showNotification', error.data.message);
						}
					);
				});
			} else {
				$rootScope.$broadcast('showNotification', "Something was wrong on login. Please try again.");
			}
		}, config);
	}
});