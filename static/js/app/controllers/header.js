/**
 * Created by lucas.menendez on 29/5/17.
 */

var app = angular.module('app');

app.controller('headerCtrl', function($scope) {
	$scope.name = localStorage.getItem('name');
	$scope.picture = localStorage.getItem('picture');
});