/**
 * Created by hariharaselvam on 11/12/16.
 */
window[appName].controller('expenses_controller', function ($rootScope, $scope, $state, http) {

    $rootScope.title = "Expenses | Wakeup | RoomManager";

    $scope.sort = "day";
    $scope.order = "asc";
    $scope.class = "glyphicon-arrow-down";
    $scope.get_data = function () {
        var url = "/api/expense/expense/?sort="+$scope.sort+"&order="+$scope.order;
        http.Requests("get", url, "").success(function (response) {

            $scope.expenses = response;

        });
    };

    $scope.column_sort = function(col){
        if($scope.order=="asc")
        {
            $scope.order="desc";
            $scope.class = "glyphicon-arrow-up";
        }else {
            $scope.order="asc";
            $scope.class = "glyphicon-arrow-down";
        }
        $scope.sort = col;
        $scope.get_data();
    }

    $scope.get_data();


});
