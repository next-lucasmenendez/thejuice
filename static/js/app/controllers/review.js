/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.controller('reviewCtrl', function ($window, $rootScope, $scope, $state, $stateParams, $timeout, service, tracker, route, DataStorage) {
	$scope.$on('$stateChangeSuccess', function () {
		var prev = route.Link('Search', 'search', 'base.search'),
			current = route.Link('Review', 'review', 'base.review'),
			next = route.Button('Create', 'download', $scope.download);

		route.clear();
		route.setPrev(prev);
		route.setCurrent(current);
		route.setNext(next);
		route.apply();
	});

	$scope.showEdit	= false;
	$scope.query = $stateParams.query;
	if ($scope.query) {
		$scope.result = DataStorage.get($scope.query);
		$scope.lang = DataStorage.get("lang") || 'en';
	} else {
        $rootScope.$broadcast('showNotification', 'An error ocurred. Please, try again.');
		$state.go('base.search');
	}

	$scope.edit = function (question) {
		var empty = !Boolean(question);
		if (empty) {
			$scope.current = {};
			$scope.current.answers = [
				{name: '', correct: false},
				{name: '', correct: false},
				{name: '', correct: false},
				{name: '', correct: true}
			]
		} else {
			$scope.current = question;
			$scope.current.first_question = question.question.split(/\s*_+\s*/)[0];
			$scope.current.second_question = question.question.split(/\s*_+\s*/)[1];
		}
		$scope.showEdit	= true;
	};

	$scope.closeEdit = function () {
		$scope.current	= null;
		$scope.showEdit	= false;
	};

	$scope.delete = function (question) {
		var index = $scope.result.questions.indexOf(question);
		$scope.result.questions.splice(index, 1);
	};

	$scope.save = function () {
		$scope.current.question = $scope.current.first_question.concat(' __________ ', $scope.current.second_question);

		if (!$scope.current.hasOwnProperty('$$hashKey')) {
			$scope.result.questions.push(angular.copy($scope.current));
			tracker.all('review', 'question', 'created');
		} else {
			tracker.all('review', 'question', 'edited');
		}
		$scope.showEdit	= false;
	};

	$scope.download = function() {
		if ($scope.result.questions) {
			tracker.all('review', 'submited', $scope.query);
			var email = sessionStorage.getItem('email');
			var result = angular.copy($scope.result);

			service.request("POST", "/download", {
				result: result,
				email: email
			}, true).then(
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
