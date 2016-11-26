/**
 * Created by hariharaselvam on 11/12/16.
 */

window.appName = "Wakeup";
window[appName] = angular.module(appName, ['ui.router', 'ngSanitize']);

window[appName].config(function ($stateProvider, $urlRouterProvider, $httpProvider) {


    $urlRouterProvider.otherwise('/');

    $stateProvider
        .state('dashboard', {
            url: '/',
            templateUrl: '/media/js/modules/dashboard.html',
            controller: 'dashboard_controller'
        });

    $stateProvider
        .state('expenses', {
            url: '/expenses',
            templateUrl: '/media/js/modules/expenses.html',
            controller: 'expenses_controller'
        });

    $stateProvider
        .state('editable', {
            url: '/editable',
            templateUrl: '/media/js/modules/editable.html',
            controller: 'editable_controller'
        });

    $stateProvider
        .state('payments', {
            url: '/payments',
            templateUrl: '/media/js/modules/payments.html',
            controller: 'payment_controller'
        });

    $stateProvider
        .state('balance', {
            url: '/balance',
            templateUrl: '/media/js/modules/balance.html',
            controller: 'balance_controller'
        });

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

window[appName].controller('wakeup_controller', function ($rootScope, $scope, $state, http ) {

    $rootScope.title = "Wakeup";

    http.Requests("get","/api/ui/session/","").success(function (response) {
        $rootScope.user = response;

    });


});
