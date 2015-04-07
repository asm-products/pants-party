angular.module('PantsParty')
    .controller('BlogCtrl', function($scope, $http, $stateParams, $state) {
        if ($state.params.slug) {
            $http.get("/api/posts/" + $state.params.slug)
                .success(function(data) {
                    $scope.posts = data;
                })
        } else { 
            $http.get("/api/blogs/")
                .success(function(data) {
                    $scope.posts = data;
                })
        }
    })

    .controller('BlogDetailCtrl', function($scope, $http, $stateParams) {
        if($stateParams.slug) {
            $http.get("/api/blogs/" + $stateParams.slug)
                .success(function(data) {
                    $scope.post = data;
                })
        }
    })
