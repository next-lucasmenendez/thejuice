/**
 * Created by lucas.menendez on 17/5/17.
 */

var app = angular.module('app');

app.controller('loginCtrl', function ($window, $rootScope, $scope, $state, requests, tracker) {
	$scope.submitLoginForm = function() {
		var config	= {scope: "public_profile, email", return_scopes: !0},
			attrs	= {fields: 'name, email,picture'};

		FB.login(function (response) {
			if (response.authResponse !== null) {
				FB.api('/me', attrs, function(profile) {
					var data = {
						id: profile.id,
						email: profile.email,
						name: profile.name,
						accesstoken: response.authResponse.accessToken,
						picture: profile.picture.data.url
					};
					requests.call('POST', '/login', data, true).then(
						function () {
							tracker.all('auth', 'login', data.email);

							sessionStorage.setItem('id', data.id);
							sessionStorage.setItem('name', data.name);
							sessionStorage.setItem('email', data.email);
							sessionStorage.setItem('accesstoken', data.accesstoken);
							sessionStorage.setItem('picture', data.picture);

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