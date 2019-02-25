
function drawTimeSeries(){
    var data1 = [], data2 = [];
    for (var i in timeSeries) {
        data1.push([Date.parse(timeSeries[i].time), timeSeries[i].score1]);
        data2.push([Date.parse(timeSeries[i].time), timeSeries[i].score2]);
    }
    data1.sort(function(a, b){
        return a[0]-b[0];
    })
    data2.sort(function(a, b){
        return a[0]-b[0];
    })

    console.log(data1);
    console.log(data2);

    var chart = {
        type: 'spline'
    };

    var xAxis = {
        type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
        },
        title: {
            text: 'Date'
        }
    };
    var yAxis = {
        title: {
            text: 'Sentiment Score'
        },
        min: 0
    };
    var tooltip = {
        shared: true,
        formatter: function(){
            time = Date(this.x).toLocaleString('en-GB', { timeZone: 'UTC' });
            point1value = this.points[0].point.y;
            point1name = this.points[0].series.name;
            point2value = this.points[1].point.y;
            point2name = this.points[1].series.name;
            return time + '<br/>' +
            point1name + ': ' + Math.round(point1value * 10000) / 10000 + '<br/>' +
            point2name + ': ' + Math.round(point2value * 10000) / 10000;
        }
    };

    var plotOptions = {
        spline: {
            marker: {
                enabled: true
            }
        }
    };

    var series = [{
        name: 'Patriots',
        data: data1
    },{
        name: 'Ram',
        data: data2
    }];

    var config = {};
    config.chart = chart;
    config.title = false;
    config.xAxis = xAxis;
    config.yAxis = yAxis;
    config.tooltip = tooltip;
    config.plotOptions = plotOptions;
    config.series = series;
    Highcharts.chart('time-series-chart', config);
}
