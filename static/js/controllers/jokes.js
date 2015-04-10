angular.module('PantsParty')
    .controller('JokeCtrl', function($rootScope, $scope, $http, $auth, $state) {
        $scope.isAuthenticated = function() { 
            return $auth.isAuthenticated();
        }

        $scope.showSubmit   = false;
        
        $scope.jokeModel = {}

        $scope.toggleSubmit = function() { 
            $scope.showSubmit = !$scope.showSubmit;
        }

        $scope.submitJoke = function() { 
            $http.post("/api/jokes/", $scope.jokeModel)
                .success(function(data) {
                    $scope.jokes.unshift(data);
                    $scope.jokeModel = {}
                    swal("Good job!", "Your joke is submitted!", "success")
                })
                .error(function(data) {
                    console.log(data);
                    swal("Error!", "So, this is embarrassing, but for some reason, your joke was not submitted.", "error")
                })
        }

        $scope.punchlineModel = {
            "joke" : null,
            "text" : "",
        }
        $scope.submitPunchline = function(joke_id) { 
            $http.post("/api/punchlines/", $scope.punchlineModel)
                .success(function(data) {
                    $scope.jokes[joke_id].punchlines.unshift(data);
                    $scope.punchlineModel = {}
                    swal("Good job!", "Your joke is submitted!", "success")
                })
                .error(function(data) {
                    console.log(data);
                })
        }

        $scope.plActive = 4;
        $scope.togglePunchlineToggle = function(joke_id) { 
            $scope.plActive = joke_id;
        }

        $http.get("/api/joke_categories/")
            .success(function(data) { 
                $scope.categories = data;
            });

        var base_url = "/api/jokes/";

        if($state.params.id)
            url = base_url + "?category=" + $state.params.id;
        else
            url = base_url;

        $http.get(url)
            .success(function(data) { 
                $scope.jokes = data;
                $scope.category_description = null;
                if($state.params.id) {
                    if($scope.jokes.length >= 1) {
                        $scope.category_description = $scope.jokes[0].category.description;
                    } else {
                        $scope.category_description = null;
                    }
                }
            });

        $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams){ 
            $scope.category_description = null;
            if($state.params.id)
                url = base_url + "?category=" + $state.params.id;
            else
                url = base_url;

            $http.get(url)
                .success(function(data) { 
                    $scope.category_description = null;
                    $scope.jokes = data;
                    if($state.params.id) {
                        if($scope.jokes.length >= 1)
                            $scope.category_description = $scope.jokes[0].category.description;
                    } else {
                        $scope.category_description = null;
                    }
                });
        })

    })
