angular.module('PantsParty')
    .controller('FAQCtrl', function($rootScope, $scope, $http, $auth, $state) {
        $http.get("/api/faq/")
            .success(function(data) { 
                $scope.faqs = data;
            });
    })
