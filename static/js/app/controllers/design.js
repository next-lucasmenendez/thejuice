/**
 * Created by lucas.menendez on 30/5/17.
 */

var app = angular.module('app');

app.controller('designCtrl', function ($window, $rootScope, $scope, $stateParams, $filter, service, route, DataStorage) {
	$scope.$on('$stateChangeSuccess', function () {
		var prev = route.Link('Review', 'review', 'base.review', {query: $stateParams.query}),
			current = route.Link('Design', 'design', 'base.design'),
			next = route.Button('Download', 'download', $scope.download);

		route.clear();
		route.setPrev(prev);
		route.setCurrent(current);
		route.setNext(next);
		route.apply();
	});

	$scope.design		= "default";
	$scope.results 		= DataStorage.get("results");
	$scope.templates	= [
		{
			thumbnail: '/static/style/templates/default.jpg',
			value: 'default',
			name: 'Default'
		}
	]

	$scope.select = function(design) {
		$scope.design = design;
	}

	$scope.download = function() {
		if ($scope.design && $scope.results) {
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
