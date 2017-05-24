/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.controller('previewCtrl', function ($window, $rootScope, $scope, $state, $stateParams, service, DataStorage) {
	$scope.results 	= DataStorage.get("results");
	$scope.format	= 'infographic';
	$scope.lang		= DataStorage.get("lang") || 'en';

	if (!Boolean($scope.results)) {
		var query = $stateParams.query;

		if (query) {
			$rootScope.$broadcast('showSpinner', 'Wait a second while we take the data out of Wikipedia...');
			$window.ga('send', 'event', 'index', 'search', query);

			service.request('POST', '/preview', {query: query, force: true, lang: $scope.lang}).then(
				function (response) {
					if (response.success) {
						$scope.results = response.result;
					} else {
						$state.go('search');
					}
					$rootScope.$broadcast('hideSpinner');
				},
				function (error) {
					$state.go('search');
					$rootScope.$broadcast('hideSpinner');
					$rootScope.$broadcast('showNotification', error.data.message);
				}
			);
		} else {
			$state.go('search');
		}
	}

	$scope.download = function() {
		if ($scope.format && $scope.results) {
			service.request("POST", "/download", {format: $scope.format, character: $scope.results}, true).then(
				function (response) {
					if (response.success) {
						$window.location.href = response.result;
					} else {
						$state.go('search');
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
