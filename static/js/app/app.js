/**
 * Created by lucas.menendez on 16/5/17.
 */
var app = angular.module("app", ['ui.router']);

app.config(function($stateProvider, $urlRouterProvider) {
	$stateProvider
		.state('search', {
			url: '/search',
			templateUrl: '/templates/search.html',
			controller: function() {
				console.log("SEARCH");
			}
		})
		.state('base', {
			url: '/',
			templateUrl: '/templates/base.html'
		})
		.state('base.preview', {
			url: '/app/preview',
			templateUrl: '/templates/preview.html'
		});

	$urlRouterProvider.otherwise('/');
});