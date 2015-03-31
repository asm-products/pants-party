angular.module('PantsParty')
    .controller('JokeCtrl', function($scope, $http, $auth) {
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

        $http.get("/api/jokes/")
            .success(function(data) { 
                $scope.jokes = data;
            });

    })
