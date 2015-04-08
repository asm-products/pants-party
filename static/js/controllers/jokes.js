angular.module('PantsParty')
    .controller('JokeCtrl', function($rootScope, $scope, $http, $auth, $state) {
        $scope.isAuthenticated = function() { 
            return $auth.isAuthenticated();
        }

        $scope.addHeart = function(joke) { 
            console.log(joke);
            console.log("Adding heart!");
        };

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
            url = url;

        $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams){ 
            if($state.params.id)
                url = base_url + "?category=" + $state.params.id;

            $http.get(url)
                .success(function(data) { 
                    $scope.jokes = data;
                    console.log($scope.jokes);
                });
        })

        $http.get(url)
            .success(function(data) { 
                $scope.jokes = data;
                console.log($scope.jokes);
            });

    })
