/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module('app');

app.controller('searchCtrl', function ($window, $rootScope, $scope, $state, service, DataStorage) {
	$scope.submitSearchForm = function(forceSearch) {
		var query = $scope.query,
			force = Boolean(forceSearch);

		if (query) {
			$rootScope.$broadcast('showSpinner', 'Wait a second while we take the data out of Wikipedia...');
			$window.ga('send', 'event', 'index', 'search', query);

			service.request('POST', '/search', {query: query, force: force}).then(
				function (response) {
					if (response.success) {
						DataStorage.set("results", response.result);
						$state.go('base.preview', {query: query});
					} else {
						$scope.results = response.options;
					}
					$rootScope.$broadcast('hideSpinner');
				},
				function (error) {
					console.log(error);
					$rootScope.$broadcast('hideSpinner');
					$rootScope.$broadcast('showNotification', error.data.message);
				}
			);
		}
	}

});