angular.module('PantsParty', ['ui.router', 'ngCookies', 'satellizer', 'angularMoment', 'ngSanitize', 'btford.markdown', 'ngMessages', 'lr.upload', 'angulartics', 'angulartics.google.analytics', ])

    .config(function($stateProvider, $urlRouterProvider, $locationProvider, $authProvider) {
        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: '/static/partials/home.html',
                controller: 'HomeCtrl',
            })
            .state('blog', {
                url: '/blog',
                templateUrl: '/static/partials/blogs.html',
                controller: 'BlogCtrl',
            })
            .state('blog-detail', {
                url: '/blog/:slug',
                templateUrl: '/static/partials/blog.html',
                controller: 'BlogDetailCtrl',
            })
            .state('faq', {
                url: '/faq',
                templateUrl: '/static/partials/faq.html',
                controller: 'FAQCtrl',
            })
            .state('help', {
                url: '/help',
                templateUrl: '/static/partials/help.html',
            })
            .state('tos', {
                url: '/tos',
                templateUrl: '/static/partials/tos.html',
            })
            .state('about', {
                url: '/about',
                templateUrl: '/static/partials/about.html',
            })
            .state('team', {
                url: '/team',
                templateUrl: '/static/partials/team.html',
            })
            .state('beliefs', {
                url: '/beliefs',
                templateUrl: '/static/partials/beliefs.html',
            })
            .state('contact', {
                url: '/contact',
                templateUrl: '/static/partials/contact.html',
            })
            .state('jokes', {
                url: '/jokes',
                templateUrl: '/static/partials/jokes.html',
                controller: 'JokeCtrl',
            })
            .state('jokes.category', {
                url: '/:id',
            })
            .state('login', {
                url: '/login',
                templateUrl: '/static/partials/login.html',
                controller: 'LoginCtrl',
            })
            .state('logout', {
                url: '/logout',
                template: "",
                controller: 'LogoutCtrl',
            })
            .state('profile', {
                url: '/profile/:profileId',
                templateUrl: "/static/partials/profile.html",
                controller: 'ProfileCtrl',
            })
            .state('hello', {
                url: '/hello',
                templateUrl: "/static/partials/hello.html",
                controller: 'HelloCtrl',
            })

        $authProvider.loginUrl = '/rest-auth/login/';
        $authProvider.tokenName = 'key';
        $authProvider.loginRedirect = '/hello';
        $authProvider.facebook({
            url: '/auth/facebook/',
            clientId: '383981465065889',
            display: 'popup',
            authorizationEndpoint: 'https://www.facebook.com/dialog/oauth',
        });

        $authProvider.twitter({
            url: '/auth/twitter/',
        });

        $authProvider.google({
            clientId: "619194941129-08kmjd2nbt526kqmdhc5sgtkt669j2cg.apps.googleusercontent.com",
            redirectUri: "http://pants.party/auth/google/",
            url: '/auth/google/'
        });

        $authProvider.oauth2({
            name: 'reddit',
            url: '/auth/reddit',
            redirectUri: 'http://pants.party/auth/reddit/',
            scope: 'identity',
            defaultUrlParams: ['response_type', 'client_id', 'redirect_uri', 'state', ],
            clientId: '49kdmpOB_TXs8Q',
            authorizationEndpoint: 'https://ssl.reddit.com/api/v1/authorize',
        });

        $urlRouterProvider.otherwise('/');
        $locationProvider.html5Mode({
            hashPrefix: '!',
            enabled: false,
            requireBase: false
        });
    })

    .config(['$httpProvider', 'satellizer.config', function($httpProvider, config) {
        $httpProvider.interceptors.push(['$q', function($q) {
            var tokenName = config.tokenPrefix ? config.tokenPrefix + '_' + config.tokenName : config.tokenName;
                return {
                    request: function(httpConfig) {
                        if (localStorage.getItem(tokenName)) {
                            httpConfig.headers.Authorization = 'Token ' + localStorage.getItem(tokenName);
                        }
                        return httpConfig;
                    },
                    responseError: function(response) {
                        if (response.status === 401) {
                            localStorage.removeItem(tokenName);
                        }
                        return $q.reject(response);
                    }
                };
            }]);
        }])

    .run( function run($http, $cookies ){
        $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    })

    .directive('bottomfooter', function() {
        return {
            restrict: "E",
            transclude: true,
            templateUrl: "/static/partials/footer.html",
        };
    })

    .directive('topheader', [function($rootScope, $scope, $http, $auth) {
        return {
            restrict: "E",
            transclude: false,
            templateUrl: "/static/partials/header.html",
            controller: function($rootScope, $scope, $http, $auth, $analytics) {
                $scope.isAuthenticated = function() {
                    return $auth.isAuthenticated();
                };

                $rootScope.$on("avatarChanged", function(event, data) { 
                    $analytics.eventTrack("changed-avatar");
                    if(localStorage.getItem("avatar") !== null) 
                        $scope.avatar = localStorage.getItem("avatar");

                    if(localStorage.getItem("username") !== null) 
                        $scope.username = localStorage.getItem("username");
                });

                if(localStorage.getItem("avatar") !== null) 
                    $scope.avatar = localStorage.getItem("avatar");

                if(localStorage.getItem("username") !== null) 
                    $scope.username = localStorage.getItem("username");

            },
            link: function(scope, elem, attrs) {
            }
        }
    }])

    .directive('subscriber', [function($scope, $http) {
        return {
            restrict: "E", 
            transclude: false,
            templateUrl: "/static/partials/subscription.html",
            controller: function($scope, $http) {
                $scope.subscription = {
                    email : ""
                };

                $scope.submitSubscription = function() { 
                    console.log($scope.subscription);
                    $http.post("/api/subscription/", $scope.subscription)
                        .success(function(data) {
                            swal("Word 'em up.", "You're the lyrical gangster.  Oh wait, no you're not.  Either way, we'll keep you up to date on things.", "success");
                        })  
                        .error(function(data) {
                            if(data.message == "Duplicate.")
                                swal("Nice try", "Looks like we already had your email.", "error");
                            else
                                swal("Oh how sad.", "That didn't work.  Not even a little bit.", "error");
                        })  
                }   
            },
            link: function(scope, elem, attrs) {}
        }
    }])

    .directive('teaser', [function($scope) {
        return {
            restrict: "E",
            transclude: false,
            templateUrl: "/static/partials/teaser.html",
        }
    }])

    .directive('joke', [function($scope) {
        return {
            restrict: "A",
            scope: {
                "joke" : "=joke",
            },
            transclude: false,
            templateUrl: "/static/partials/_joke.html",
            controller: function($scope, $http, $analytics) { 
                $scope.addHeart = function(joke) { 
                    $analytics.eventTrack("added-heart", {joke: joke.id});
                    payload = {"vote": 1, "joke": joke.id}
                    $http.post("/api/votes/", payload)
                        .success(function(data) {
                            joke.user_has_voted = true;
                        })
                        .error(function(data) {
                            console.log(data);
                            alert("Error!");
                        })
                }

                $scope.removeHeart = function(joke) { 
                    $analytics.eventTrack("removed-heart", {joke: joke.id});
                    payload = {"vote": 1, "joke": joke.id}
                    $http.delete("/api/votes/" + joke.id)
                        .success(function(data) {
                            joke.user_has_voted = false;
                        })
                        .error(function(data) {
                            console.log(data);
                            alert("Error!!");
                        })
                }

                $scope.punchlineModel = { 
                    "joke_id" : null,
                    "text" : "", 
                }   
                $scope.submitPunchline = function(obj, joke_id) { 
                    $analytics.eventTrack("submitted-punchline", {joke: joke_id});
                    $scope.punchlineModel.joke_id = joke_id;
                    $http.post("/api/punchlines/", $scope.punchlineModel)
                        .success(function(data) {
                            $scope.punchlineModel = {}
                            swal("Good job!", "Your punchline is submitted!", "success")
                        })  
                        .error(function(data) {
                            console.log(data);
                        })  
                }   

                $scope.togglePunchlineSubmit = function(joke_id) { 
                    if(joke_id == $scope.plActive)
                        $scope.plActive = null;
                    else
                        $scope.plActive = joke_id;
                }   

            }
        }
    }])
