angular.module('PantsParty')
    .controller('LoginCtrl', function($scope, $auth) {
        $scope.login = function() {
            $auth.login({ username: $scope.username, password: $scope.password })
                .then(function() {
                    console.log("Successful login");
                })
                .catch(function(response) {
                    console.log(response.data.message);
                });
        }

        $scope.authenticate = function(provider) {
            $auth.authenticate(provider)
                .then(function() {
                    $scope.$broadcast("loginout", "on!");
                })
                .catch(function(response) {
                    console.log(response.data ? response.data.message : response);
                });
        };
    })

    .controller('ProfileCtrl', function($scope, $auth, $http, $stateParams) {
        if($stateParams.profileId) {
            console.log($stateParams.profileId);
            $scope.isAuthenticated = function() {
                return $auth.isAuthenticated();
            }


            $http.get("/api/users/" + $stateParams.profileId)
                .success(function(data) { 
                    $scope.profile = data;
                })
                .error(function(data) { 
                    swal("404", "This user does not exist.", "error");
                })
        } else { 
            swal("404", "This user does not exist.", "error");
        }
    })
