/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module('app');

app.controller('searchCtrl', function ($window, $scope, $state, service, DataStorage) {

	$scope.submitSearchForm = function(forceSearch) {
		var query = $scope.query,
			force = Boolean(forceSearch);

		console.log(force);

		if (query) {
			$window.ga('send', 'event', 'index', 'search', query);

			service.request('POST', '/search', {query: query, force: force}).then(
				function (response) {
					console.log(response);
					if (response.success) {
						DataStorage.set("results", response.result);
						$state.go('base.preview', {query: query});
					} else {
						$scope.results = response.options;
					}
				},
				function (error) {
					console.log(error);
				}
			)
		}
	}

});