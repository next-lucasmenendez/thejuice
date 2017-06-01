/**
 * Created by lucas.menendez on 29/5/17.
 */

var app = angular.module('app');

app.controller('headerCtrl', function($scope, $state) {
	$scope.name = sessionStorage.getItem('name');
	$scope.picture = sessionStorage.getItem('picture');

	$scope.logout = function () {
		sessionStorage.clear();
		$state.go('login');
	}
});