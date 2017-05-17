/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.service('service', function ($rootScope, $q, $http) {
	this.request = function (method, url, data, as_json) {
		as_json = Boolean(as_json);

		var result = $q.defer();
		$http({
			method: method,
			url: url,
			data: (as_json) ? angular.toJson(data) : $.param(data),
			headers : {
				'Content-Type': (as_json) ? 'application/json' : 'application/x-www-form-urlencoded'
			}
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
