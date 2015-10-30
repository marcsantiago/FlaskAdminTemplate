var options = {
    series: {
        bars: {
          show: true,
          barWidth: 0.1,
          align: "center"
        }
    },
    xaxis: {
      mode: "categories",
      autoscaleMargin: 1,
      tickLength: 0,
      reserveSpace: true,
      axisLabelPadding: 10,
    },
    yaxis: {
      axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
      axisLabelPadding: 3,
    },
};


var plot = function(my_data){
  $.plot(placeholder,[
    {
      label: 'Daily Cost In Dollars',
      data: my_data,
    }
  ], 
    options);
};