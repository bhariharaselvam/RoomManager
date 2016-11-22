/**
 * Created by hariharaselvam on 11/12/16.
 */
window[appName].controller('dashboard_controller', function ($rootScope, $scope, $state, http,message) {

    $rootScope.title = "Dashboard";
    $scope.dashboard = {
        "page": "Dashboard"
    };

    $('#date').datepicker({
        format: 'yyyy-mm-dd',
        widgetPositioning: {
            horizontal: 'right',
            vertical: 'bottom'
        }
    });

    $scope.add_amount = function () {
        var param = {"name": $scope.desc, "date": $scope.date, "amount": $scope.amount};
        http.Requests("post", "/api/expense/expense/", param).success(function (response) {
            $("#alert_box").html(message.alert(response.status,response.result));
            $scope.get_chart();

        });
    };

    $scope.get_chart = function () {
        http.Requests("get", "/api/expense/useramount/", "").success(function (response) {

            $scope.expenses = response;

            $(function () {
                // Create the chart
                Highcharts.chart('container', {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Aggregate of User Expenses'
                    },

                    xAxis: {
                        type: 'User'
                    },
                    yAxis: {
                        title: {
                            text: 'Total Rupees expended'
                        }

                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                format: '{point.y} Rs'
                            }
                        }
                    },

                    tooltip: {
                        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> Rs<br/>'
                    },

                    series: [{
                        name: 'User',
                        colorByPoint: true,
                        data: response
                    }],
                    credits:{enabled:false}
                });
            });


        });

    }
    $scope.get_chart();

});