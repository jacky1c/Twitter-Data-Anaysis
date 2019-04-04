function drawSentimentTimeSeries(){
    var data1 = [], data2 = [];
	var trumpKeys = Object.keys(Trump_ScoreByTime);
	var pelosiKeys = Object.keys(Pelosi_ScoreByTime);
    for (var i = 0; i < trumpKeys.length; i++) {
        data1.push([Date.parse(trumpKeys[i]), Trump_ScoreByTime[trumpKeys[i]]]);
    }
	for (var j = 0; j < pelosiKeys.length; j++) {
        data2.push([Date.parse(pelosiKeys[j]), Pelosi_ScoreByTime[pelosiKeys[j]]]);
    }

    data1.sort(function(a, b){
        return a[0]-b[0];
    })
	data2.sort(function(a, b){
        return a[0]-b[0];
    })

    var chart = {
        type: 'spline',
		backgroundColor: '#F1F1F1'
    };
    var title ={
        text: 'Twitter Sentiment Score'
    };
    var subtitle ={
        text: 'Trump vs Pelosi'
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
        min: -1,
		max: 1
    };
    var tooltip = {
        shared: true
    };

    var plotOptions = {
        spline: {
            marker: {
                enabled: true
            }
        }
    };

    var series = [{
        name: 'Trump Sentiment',
        data: data1,
        color: '#BF0A30'
    },{
        name: 'Pelosi Sentiment',
        data: data2,
        color: '#002868'
    }];

    var config = {};
    config.chart = chart;
    config.title = title;
    config.subtitle = subtitle;
    config.xAxis = xAxis;
    config.yAxis = yAxis;
    config.tooltip = tooltip;
    config.plotOptions = plotOptions;
    config.series = series;
    Highcharts.chart('time-series-chart-trump', config);
}
