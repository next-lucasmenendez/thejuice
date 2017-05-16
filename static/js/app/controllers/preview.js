/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.controller('previewCtrl', function ($scope, $stateParams, DataStorage) {
	console.log($stateParams.query);
	$scope.results = DataStorage.get("results");
	console.log($scope.results)
});
