/**
 * Created by lucas.menendez on 16/5/17.
 */

var api = {

}

var app = angular.module('app', ['ui.router']);

app.run(function($rootScope, $location, $window) {
	$window.ga('create', 'UA-92654268-2', 'auto');
});

app.config(function($stateProvider, $urlRouterProvider) {
	$stateProvider
		.state('search', {
			url: '/search',
			templateUrl: '/static/templates/search.html',
			controller: 'searchCtrl'
		})
		.state('base', {
			url: '/',
			templateUrl: '/static/templates/base.html'
		})
		.state('base.preview', {
			url: 'preview/:query',
			templateUrl: '/static/templates/preview.html',
			controller: 'previewCtrl'
		});
	$urlRouterProvider.otherwise('/search');
});