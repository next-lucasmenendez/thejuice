/**
 * Created by lucas.menendez on 16/5/17.
 */
var app = angular.module("app", ['ui.router']);

app.config(function($stateProvider, $urlRouterProvider) {
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
});