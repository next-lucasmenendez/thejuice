/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module('app');

app.controller('searchCtrl', function ($window, $rootScope, $scope, $state, service, DataStorage) {
	$scope.lang = "en";

	$scope.submitSearchForm = function(query) {
		if (query) {
			$rootScope.$broadcast('showSpinner', 'Wait a second while we take the data out of Wikipedia...');
			$window.ga('send', 'event', 'index', 'search', query);
			service.request('POST', '/search', {query: query, lang: $scope.lang}).then(
				function (response) {
					if (response.success) {
						DataStorage.set("results", response.result);
						DataStorage.set("lang", $scope.lang);
						$state.go('base.preview', {query: query});
					} else {
						$scope.results = response.options;
					}
					$rootScope.$broadcast('hideSpinner');
				},
				function (error) {
					$rootScope.$broadcast('hideSpinner');
					$rootScope.$broadcast('showNotification', error.data.message);
				}
			);

		} else if ($scope.query) {
			$window.ga('send', 'event', 'index', 'search', $scope.query);
			DataStorage.set("lang", $scope.lang);
			$state.go('base.preview', {query: $scope.query, lang: $scope.lang});
		}
	}

	$scope.forceSearchForm = function(query) {
		$scope.query = query;
		$scope.submitSearchForm(true);
	}
});