/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module('app');


app.controller('searchCtrl', function ($window, $rootScope, $scope, $state, requests, tracker, route, DataStorage) {
	$scope.$on('$stateChangeSuccess', function () {
		var current = route.Link('Search', 'search', 'base.search');

		route.clear();
		route.setCurrent(current);
		route.apply();
		DataStorage.clear()
	});

	$scope.lang = "en";
	$scope.submitSearchForm = function() {
		tracker.all('index', 'search', $scope.query);
		$rootScope.$broadcast('showSpinner', 'Wait a second while we search on Wikipedia...');
		var uri = '/search/' + $scope.query;
		requests.call('GET', uri, {lang: $scope.lang}).then(
			function (response) {
				if (response.success) {
					$scope.results = response.results;
				} else {
					$scope.results = response.options;
				}
				$rootScope.$broadcast('hideSpinner');
			},
			function (error) {
				$rootScope.$broadcast('hideSpinner');
				$rootScope.$broadcast('showNotification', error.data.message);
				$state.go('base.search');
			}
		);
	}

	$scope.reviewPage = function(pageId) {
		$rootScope.$broadcast('showSpinner', 'Wait a second while we take the data out of Wikipedia...');

		var uri = '/review/' + pageId;
		requests.call('GET', uri, {lang: $scope.lang}).then(
			function (response) {
				if (response.success) {
					DataStorage.set(pageId, response.result);
					DataStorage.set("lang", $scope.lang);
					$state.go('base.review', {query: pageId});
				} else {
					$scope.results = response.options;
				}
				$rootScope.$broadcast('hideSpinner');
			},
			function (error) {
				$rootScope.$broadcast('hideSpinner');
				$rootScope.$broadcast('showNotification', error.data.message);
				$state.go('base.search');
			}
		);
	}

});
