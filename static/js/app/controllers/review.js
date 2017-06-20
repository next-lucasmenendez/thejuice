/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.controller('reviewCtrl', function ($window, $rootScope, $scope, $state, $stateParams, $timeout, requests, tracker, route, DataStorage) {
	$scope.$on('$stateChangeSuccess', function () {
		var prev = route.Link('Search', 'search', 'base.search'),
			current = route.Link('Review', 'review', 'base.review'),
			next = route.Button('Design', 'design', $scope.design);

		route.clear();
		route.setPrev(prev);
		route.setCurrent(current);
		route.setNext(next);
		route.apply();
	});

	$scope.showEdit	= false;
	$scope.result = DataStorage.get('result');
	console.log($scope.result);

	$scope.edit = function (sentence) {
		// $scope.current = {};
		$scope.current = sentence;
		// $scope.current.old = sentence;
		// $scope.current.new = sentence;
		$scope.showEdit	= true;
	};

	$scope.closeEdit = function () {
		$scope.current	= null;
		$scope.showEdit	= false;
	};

	$scope.delete = function (sentence) {
		var index = $scope.result.sentences.indexOf(sentence);
		$scope.result.sentences.splice(index, 1);
	};

	$scope.save = function () {
		$window.ga('send', 'event', 'review', 'event edited');
		tracker.all('review', 'event', 'edited');

		$scope.showEdit	= false;
	};

	$scope.design = function() {
		var query = $stateParams.query || $scope.query;
		tracker.all('review', 'submited', $scope.result.title);
		if ($scope.result) {
			DataStorage.set('article', $scope.result);
			$state.go('base.design');
		}
	};
});
