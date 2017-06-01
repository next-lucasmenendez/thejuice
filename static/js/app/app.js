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
							$state.go('base.search');
						}
						result.resolve();
					});

					return result.promise;
				}
			}
		})
		.state('base', {
			url: '/',
			templateUrl: '/static/templates/base.html',
			resolve: {
				control: checkAccessToken
			}
		})
		.state('base.search', {
			url: 'search',
			templateUrl: '/static/templates/search.html',
			controller: 'searchCtrl',
			resolve: {
				control: checkAccessToken,
				onEnter: function ($rootScope) {
					$rootScope.steps = {
						previous: false,
						current: {
							name: "Search",
							uri: "base.search"
						},
						next: {
							name: "Review",
							uri: "base.review"
						}
					};
				}
			}
		})
		.state('base.review', {
			url: 'review/:query',
			templateUrl: '/static/templates/review.html',
			controller: 'reviewCtrl',
				onEnter: function ($rootScope) {
					$rootScope.step = "review";
					$rootScope.steps = {
						previous: {
							name: "Search",
							uri: "base.search"
						},
						current: {
							name: "Review",
							uri: "base.review"
						},
						next: {
							name: "Design",
							uri: "base.design"
						}
					};
				}
		})
		.state('base.design', {
			url: 'design/:query',
			templateUrl: '/static/templates/design.html',
			controller: 'designCtrl',
				onEnter: function ($rootScope) {
					$rootScope.steps = {
						previous: {
							name: "Review",
							uri: "base.review"
						},
						current: {
							name: "Design",
							uri: "base.design"
						},
						next: {
							name: "Download",
							uri: "base.download"
						}
					};
				}
		});
	$urlRouterProvider.otherwise('/search');
});