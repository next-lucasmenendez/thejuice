/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.factory('DataStorage', function($rootScope) {
	var mem = {};

	return {
        set: function (key, value) {
            mem[key] = value;
        },
        get: function (key) {
            return mem[key];
        }
    };
});
