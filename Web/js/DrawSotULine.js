function drawSotUTimeSeries(){
    var data1 = [], data2 = [], data3 = [], data4 = [];
	var SotUTrumpMentionKeys = Object.keys(SOTU_TrumpMention_ByTime);
	var SotUPelosiMentionKeys = Object.keys(SOTU_PelosiMention_ByTime);
	var SotUTrumpScoreKeys = Object.keys(SOTU_TrumpScore_ByTime);
	var SotUPelosiScoreKeys = Object.keys(SOTU_PelosiScore_ByTime);
    for (var i = 0; i < SotUTrumpMentionKeys.length; i++) {
        data1.push([Date.parse(SotUTrumpMentionKeys[i]), SOTU_TrumpMention_ByTime[SotUTrumpMentionKeys[i]]]);
    }
	for (var j = 0; j < SotUPelosiMentionKeys.length; j++) {
        data2.push([Date.parse(SotUPelosiMentionKeys[j]), SOTU_PelosiMention_ByTime[SotUPelosiMentionKeys[j]]]);
	}
	for (var k = 0; k < SotUTrumpScoreKeys.length; k++) {
        data3.push([Date.parse(SotUTrumpScoreKeys[k]), SOTU_TrumpScore_ByTime[SotUTrumpScoreKeys[k]]]);
    }
	for (var l = 0; l < SotUPelosiScoreKeys.length; l++) {
        data4.push([Date.parse(SotUPelosiScoreKeys[l]), SOTU_PelosiScore_ByTime[SotUPelosiScoreKeys[l]]]);
    }
    data1.sort(function(a, b){
        return a[0]-b[0];
    })
    data2.sort(function(a, b){
        return a[0]-b[0];
    })
	data3.sort(function(a, b){
        return a[0]-b[0];
    })
	data4.sort(function(a, b){
        return a[0]-b[0];
    })

    var chart = {
        type: 'spline',
		backgroundColor: '#F1F1F1'
    };

	var title = {
        text: 'Tweets Regarding State of the Union'
    };
    var subtitle = {
        text: 'Trump Sentiment & Mention vs. Pelosi Sentiment & Mention'
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
            text: 'Sentiment/Mention Score'
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
        name: 'Trump Mention',
        data: data1,
        tooltip: {
            pointFormatter: function(){
                return "Trump Mention: <b>" + Math.round(this.y*10000)/100 + "%</b><br>";
            }
        },
        color: '#F7B2AD'
    },{
        name: 'Pelosi Mention',
        data: data2,
        tooltip: {
            pointFormatter: function(){
                return "Pelosi Mention: <b>" + Math.round(this.y*10000)/100 + "%</b><br>";
            }
        },
        color: '#8FB8DE'
    },{
    	name: 'Sentiment Towards Trump',
    	data: data3,
        color: '#BF0A30'
    },{
    	name: 'Sentiment Towards Pelosi',
    	data: data4,
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
    Highcharts.chart('time-series-chart-SotU', config);
}
