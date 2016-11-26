/**
 * Created by hariharaselvam on 11/26/16.
 */
window[appName].controller('balance_controller', function ($rootScope, $scope, $state, http) {

    $rootScope.title = "Balance";



    $scope.call_data = function () {

        http.Requests("get", "/api/expense/balance/", "").success(function (response) {

            $scope.payments = response.payments;
            $scope.users = response.users;


        });
    };



    $scope.call_data();

});
