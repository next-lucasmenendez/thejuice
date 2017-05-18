/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module('app', ['ui.router']);

var checkAccessToken = function ($q, $state, $timeout) {
	var result = $q.defer();

	$timeout(function () {
		var accesstoken = localStorage.getItem('accesstoken');

		if (!Boolean(accesstoken)) {
			localStorage.clear();
			$state.go('login');
		}
		result.resolve();
	});

	return result.promise;
}

app.run(function($rootScope, $location, $window) {
	$window.ga('create', 'UA-92654268-2', 'auto');
});

app.config(function($stateProvider, $urlRouterProvider) {
	$stateProvider
		.state('login', {
			url: '/login',
			templateUrl: '/static/templates/login.html',
			controller: 'loginCtrl',
			resolve: {
				control: function ($q, $state, $timeout) {
					var result = $q.defer();

					$timeout(function () {
						var accesstoken = localStorage.getItem('accesstoken');

						if (Boolean(accesstoken)) {
							$state.go('search');
						}
						result.resolve();
					});

					return result.promise;
				}
			}
		})
		.state('search', {
			url: '/search',
			templateUrl: '/static/templates/search.html',
			controller: 'searchCtrl',
			resolve: {
				control: checkAccessToken
			}
		})
		.state('base', {
			url: '/',
			templateUrl: '/static/templates/base.html',
			resolve: {
				control: checkAccessToken
			}
		})
		.state('base.preview', {
			url: 'preview/:query',
			templateUrl: '/static/templates/preview.html',
			controller: 'previewCtrl'
		});
	$urlRouterProvider.otherwise('/search');
});