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

	$scope.submitSearchForm = function() {
		tracker.all('index', 'search', $scope.query);
		$rootScope.$broadcast('showSpinner', 'Wait a second while we search on Wikipedia...');
		var uri = '/link';
		requests.call('POST', uri, {url: $scope.query}).then(
			function (response) {
				if (response.success) {
					DataStorage.set('result', response.result);
					tracker.all('search', 'review', response.result.title);
					$state.go('base.review');
				}
				$rootScope.$broadcast('hideSpinner');
			},
			function (error) {
				$rootScope.$broadcast('hideSpinner');
				$rootScope.$broadcast('showNotification', error.data.message);
				$state.go('base.search');
			}
		);
	};
});
