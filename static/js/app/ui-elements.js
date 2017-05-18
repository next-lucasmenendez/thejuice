/**
 * Created by lucas.menendez on 17/5/17.
 */

var app = angular.module('app');


/**
 * Spinner and Notification Controllers
 */
app.controller('spinnerCtrl', function ($scope) {
	$scope.show = function(e, msg) {
		$scope.spinner = {
			show: true,
			msg: msg
		}
	}

	$scope.hide = function() {
		$scope.spinner = {show: false}
	}

	$scope.$on('showSpinner', $scope.show);
	$scope.$on('hideSpinner', $scope.hide);
});

app.controller('notificationCtrl', function ($scope, $timeout) {
	$scope.show = function(e, msg) {
		$scope.notification = {
			show: true,
			msg: msg
		}

		$timeout(function () {
			$scope.notification.show = false;
		}, 2000);
	}

	$scope.$on('showNotification', $scope.show);
});


/**
 * Directives
 */
app.directive("contenteditable", function() {
	return {
		restrict: "A",
		require: "ngModel",
		link: function(scope, element, attrs, ngModel) {
			function read() {
				ngModel.$setViewValue(element.html());
			}

			ngModel.$render = function() {
				element.html(ngModel.$viewValue || "");
			};

			element.bind("blur keyup change", function() {
				scope.$apply(read);
			});
		}
	};
});