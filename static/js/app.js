angular.module('PantsParty', ['ui.router', 'ngCookies', 'satellizer', 'angularMoment', 'ngSanitize', 'btford.markdown', ])

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

        $authProvider.loginUrl = '/rest-auth/login/';
        $authProvider.tokenName = 'key';
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

    .directive('topheader', [function($scope, $auth) {
        return {
            restrict: "E",
            transclude: false,
            templateUrl: "/static/partials/header.html",
            controller: function($scope, $http, $auth) {
                $scope.isAuthenticated = function() {
                    return $auth.isAuthenticated();
                };
            },
            link: function(scope, elem, attrs) {
            }
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
            controller: function($scope, $http) { 
                $scope.punchlineModel = { 
                    "joke_id" : null,
                    "text" : "", 
                }   
                $scope.submitPunchline = function(obj, joke_id) { 
                    console.log($scope.jokes);
                    $scope.punchlineModel.joke_id = joke_id;
                    console.log($scope.punchlineModel);
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
