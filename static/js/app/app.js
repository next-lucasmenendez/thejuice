/**
 * Created by lucas.menendez on 16/5/17.
 */
var app = angular.module("app", ['ui.router']);

app.config(function($stateProvider, $urlRouterProvider) {
<<<<<<< HEAD
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
=======
	$urlRouterProvider.otherwise('/');
	$stateProvider
		.state('base', {
			url: '',
			templateUrl: '/templates/base.html'
		})
		.state('search', {
			url: '/',
			templateUrl: '/templates/search.html'
		})
		.state('base.preview', {
			url: '/preview',
			templateUrl: '/templates/preview.html'
		})
>>>>>>> 77eaa8fa3298fdf63f76fdc16ac3eaa1722d4ae0
});