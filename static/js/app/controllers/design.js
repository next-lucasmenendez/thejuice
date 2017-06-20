/**
 * Created by lucas.menendez on 30/5/17.
 */

var app = angular.module('app');

app.controller('designCtrl', function ($window, $rootScope, $scope, $stateParams, $filter, requests, tracker, route, DataStorage) {
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

	$scope.result = DataStorage.get('article');

	$scope.design		= "simple";
	$scope.templates	= [
		{
			thumbnail: '/static/style/templates/default.jpg',
			value: 'simple',
			name: 'Simple',
			paid: false,
			price: "Free",
			avalible: true
		},
		{
			thumbnail: '/static/style/templates/bl4ck.jpg',
			value: 'emoji',
			name: 'Emoji',
			paid: false,
			price: "Free",
			avalible: true
		},
		{
			thumbnail: '/static/style/templates/chattemplate.jpg',
			value: 'iconic',
			name: 'Iconic',
			paid: false,
			price: "Free",
			avalible: true
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
		if ($scope.design && $scope.result) {
			tracker.all('design', 'template', $scope.design);
			tracker.all('design', 'article', $scope.result.title);

			var data = {
				design: $scope.design,
				title: $scope.result.title,
				sentences: $scope.result.sentences
			};
			requests.call("POST", "/download", data, true).then(
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
