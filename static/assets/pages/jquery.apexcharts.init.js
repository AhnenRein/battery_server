/**
 * Theme: Frogetor - Responsive Bootstrap 4 Admin Dashboard
 * Author: Mannatthemes
 * Apexcharts Js
 */

// Mixed All
var options = {
    chart: {
        id: 'mixed_chart',
        height: 380,
        type: 'line',
        toolbar: {
            show: false
        },
        events: {
            dataPointSelection: function(event, chartContext, config) {
                alert('adfads')
              }
        },

    },


    stroke: {
        curve: 'smooth',
        width: 2
    },
    colors: ['#64a0d7', '#98d25a', '#f0975a'],
    series: [{
        name: '',
        type: 'line',
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }],
    fill: {
        type: 'solid',
        opacity: [0.35, 1],
    },
    markers: {
        size: 0
    },
    legend: {
        offsetY: -10,
    },
    yaxis: [
        {
            range: [0, 1],
            title: {
                text: 'KW',
            },
            min: -5,
            max: 1,
        },
        {
            title: {
                text: '',
            },
            show: false,
            min: -5,
            max: 1,
        },
        {
            opposite: true,
            title: {
                text: '',
            },
            min: -5,
            max: 1,
        },
    ],
    tooltip: {
        shared: true,
        intersect: false,
        y: {
            formatter: function (y) {
                return y;

            }
        }
    },
    grid: {
        borderColor: '#f1f3fa'
    },
    xaxis: {
        categories: ['0:00:00', '1:00:00', '2:00:00', '3:00:00', '4:00:00', '5:00:00', '6:00:00', '7:00:00', '8:00:00', '9:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00', '23:00:00', '24:00:00',],
      },
    responsive: [{
        breakpoint: 600,
        options: {
            yaxis: {
                show: false
            },
            legend: {
                show: false
            }
        }
    }]
}



var chart = new ApexCharts(
    document.querySelector("#apex_mixed3"),
    options
);

chart.render();

function selectExcelClick(select_value) {

    $.ajax({
        type: "GET",
        url: "chart",
        data: {
            'func': 'selectExcelClick',
            'excelfilename': select_value,
        },
        dataType: "json",
        success: function (datas) {

            data_array = datas['data_array'];
            serieses = [];
            var time_select = document.getElementById("time_select");
            if(time_select.length > 1){
                time_select.options.length=1; 
            }
            for (j = 0; j < data_array[0].length; j++) {
                time_select.options.add(new Option(data_array[0][j]));
            }

            for (i = 1; i < data_array.length; i++) {
                data_arr = data_array[i];
                series = {
                    type: data_arr.shift(),
                    name: data_arr.shift(),
                    data: new Array
                };

                for (j = 0; j < data_array[0].length; j++) {
                    series.data[j] = data_arr[j];
                }
                serieses.push(series);
            }
            chart.updateSeries(serieses);

        }
    });
}

function modelChanged(model) {
    $.ajax({
        type: "GET",
        url: "chart",
        data: {
            'func': 'modelChanged',
            'model': model,
        },
        dataType: "json",
        success: function (datas) {

            data_array = datas['data_array'];
            serieses = [];

            for (i = 1; i < data_array.length; i++) {
                data_arr = data_array[i];
                series = {
                    type: data_arr.shift(),
                    name: data_arr.shift(),
                    data: new Array
                };

                for (j = 0; j < data_array[0].length; j++) {
                    series.data[j] = data_arr[j];
                }
                serieses.push(series);
            }
            chart.updateSeries(serieses);

        }
    });
}





//  '0:00:00', '1:00:00', '2:00:00', '3:00:00', '4:00:00', '5:00:00', '6:00:00', '7:00:00', '8:00:00', '9:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00', '23:00:00', '23:00:00',

