angular.module('PantsParty')
    .controller('HomeCtrl', function($scope, $http, $auth) {
        $scope.isAuthenticated = function() {
            return $auth.isAuthenticated();
        };

        $scope.isAuthenticated();

        $http.get("/static/images.json")
            .success(function(data) { 
                $scope.images = data;
            })

        $http.get("/api/jokes/")
            .success(function(data) { 
                $scope.jokes = data;
            });

    })

