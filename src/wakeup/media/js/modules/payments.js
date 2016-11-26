/**
 * Created by hariharaselvam on 11/13/16.
 */
/**
 * Created by hariharaselvam on 11/12/16.
 */
window[appName].controller('payment_controller', function ($rootScope, $scope, $state, http) {

    $rootScope.title = "Static Payments | Wakeup | RoomManager";
    $scope.id = "0";
    $scope.payment = [];
    $scope.call_data = function () {

        http.Requests("get", "/api/expense/payment/", "").success(function (response) {

            $scope.payment = response;


        });
    };


    $scope.editable = function (id, desc, amt) {
        $scope.id = id;
        $scope.desc = desc;
        $scope.amount = amt;
    };

    $scope.remove = function (id) {
        var url = "/api/expense/payment/" + id.toString() + "/";
        http.Requests("delete", url, "").success(function (response) {
            $scope.response = response.result;
            if (response.status) {
                $scope.call_data();
            }
        });

    };

    $scope.update = function (id) {
        var param = {"name": $scope.desc, "amount": $scope.amount};
        if ($scope.id == "0") {

            http.Requests("post", "/api/expense/payment/", param).success(function (response) {

                $scope.response = response.result;

            });
        } else {
            var url = "/api/expense/payment/" + $scope.id + "/";

            http.Requests("patch", url, param).success(function (response) {
                $scope.response = response.result;

            });
            $scope.id = "0";
            $scope.desc = "";
            $scope.amount = 0;

        }

        $scope.call_data();


    };


    $scope.call_data();

});
