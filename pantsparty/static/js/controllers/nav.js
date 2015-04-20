angular.module('PantsParty')
    .controller('LogoutCtrl', function($scope, $state, $auth) {
    })

    .controller('NavCtrl', function($scope, $auth, $state) {
        $scope.isAuthenticated = function() {
            return $auth.isAuthenticated();
        };

        $scope.logout = function() { 
            $auth.logout()
                .then(function() {
                    console.log("Logged out!");
                    $scope.$broadcast("loginout", "off!");
                });
        };
    })
