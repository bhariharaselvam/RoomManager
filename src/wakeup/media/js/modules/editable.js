/**
 * Created by hariharaselvam on 11/12/16.
 */
window[appName].controller('editable_controller', function ($rootScope, $scope, $state, http) {

    $rootScope.title = "My Expenses | Wakeup | RoomManager";

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        widgetPositioning: {
            horizontal: 'right',
            vertical: 'bottom'
        }
    });

    $scope.call_data = function () {

        http.Requests("get", "/api/expense/editable/", "").success(function (response) {

            $scope.expenses = response;
            for (i = 0; i < $scope.expenses.length; i++) {
                $scope.expenses[i]['edit'] = "edit";
                $scope.expenses[i]['index'] = i;
            }

        });
    };


    $scope.editable = function (i) {
        if ($scope.expenses[i]['edit'] == "edit") {
            $scope.expenses[i]['edit'] = "ok"
        }
        else {
            var url = "/api/expense/editable/" + $scope.expenses[i]['id'] + "/";
            var param = {"amount": $scope.expenses[i]['amount'],"name":$scope.expenses[i]['name'],"date":$scope.expenses[i]['date']}
            http.Requests("patch", url, param).success(function (response) {
                $scope.response = response.result;
                if (response.status) {
                    $scope.call_data();
                }
            });
            $scope.expenses[i]['edit'] = "edit"
        }
    };

    $scope.remove = function (i) {
        var url = "/api/expense/editable/" + $scope.expenses[i]['id'] + "/";
        http.Requests("delete", url, "").success(function (response) {
            $scope.response = response.result;
            if (response.status) {
                $scope.call_data();
            }
        });

    };

    $scope.call_data();

});