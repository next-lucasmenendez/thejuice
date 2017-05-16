/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.service('service', function ($q, $http) {
	this.request = function (method, url, data) {
		var result = $q.defer();
		$http({
			method: method,
			url: url,
			data: $.param(data),
			headers : {'Content-Type': 'application/x-www-form-urlencoded'}
		}).then(
			function (response) {
				if (response.status >= 200 && response.status <= 300) {
					result.resolve(response.data);
				} else {
					result.reject(response.data);
				}
			},
			function (error) {
				result.reject(error);
			}
		)
		return result.promise;
	};
});
