/**
 * Created by lucas.menendez on 30/5/17.
 */

var app = angular.module('app');

app.controller('designCtrl', function ($window, $rootScope, $scope, $stateParams, $filter, service, tracker, route, DataStorage) {
	$scope.$on('$stateChangeSuccess', function () {
		var prev = route.Link('Review', 'review', 'base.review', {query: $stateParams.query}),
			current = route.Link('Design', 'design', 'base.design'),
			next = route.Button('Create', 'download', $scope.download);

		route.clear();
		route.setPrev(prev);
		route.setCurrent(current);
		route.setNext(next);
		route.apply();
	});

	var query = $stateParams.query;
	if (query) {
		$scope.results = DataStorage.get(query);
		$scope.lang = DataStorage.get("lang") || 'en';
	} else {
		$state.go('base.search');
	}

	$scope.design		= "default";
	$scope.templates	= [
		{
			thumbnail: '/static/style/templates/default.jpg',
			value: 'default',
			name: 'Default',
			paid: false,
			price: "Free",
			avalible: true
		},
		{
			thumbnail: '/static/style/templates/bl4ck.jpg',
			value: 'bl4ck',
			name: 'Bl4ck',
			paid: false,
			price: "Free",
			avalible: true
		},
		{
			thumbnail: '/static/style/templates/chattemplate.jpg',
			value: false,
			name: 'ChatTemplate',
			paid: true,
			price: "$ 0.99",
			avalible: false
		}
	]

	$scope.select = function(design) {
		$scope.design = design;
	}

	$scope.messageSoon = false;
	$scope.comingSoon = function () {
		$scope.messageSoon = !$scope.messageSoon;
		tracker.all('design', 'template', 'paid template');
	}


	$scope.download = function() {
		if ($scope.design && $scope.results) {
			tracker.all('design', 'template', $scope.design);
			tracker.all('design', 'query', $scope.results.title);

			var results = angular.copy($scope.results);
			results.hits.sort(function(a, b){
				return  new Date(a.date) - new Date(b.date);
			});

			service.request("POST", "/download", {design: $scope.design, character: results}, true).then(
				function (response) {
					if (response.success) {
						$window.location.href = response.result;
					} else {
						$state.go('base.search');
					}
					$rootScope.$broadcast('hideSpinner');
				},
				function (error) {
					$rootScope.$broadcast('hideSpinner');
					$rootScope.$broadcast('showNotification', error.data.message);
				}
			);
		}
	}
});