//Plot.ly Javascript plot used to display latest measurements
//Original sounced from "aqi" fork: https://github.com/jtme/aqi



var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        PlotGraph(myArr);
    }
};

//xmlhttp.open("GET", "http://192.168.0.170/aqi.json", true);
xmlhttp.open("GET", "aqi.json", true);
xmlhttp.send();


//<script type="text/javascript">
//function read_json() {
//    $.getJSON("/aqi.json", function(data) {
//        alert("My data: " + data["mydata"]);
//        $.each(data["prime"], function(idx,prime) {
//            alert("Prime number: " + prime);
//        });
//    });
//}
//    </script>

function PlotGraph(data) {
  read_json();
  let trace1 = {
    x: [],
    y: [],
    mode: "lines"
  };
  let trace2 = {
    x: [],
    y: [],
    mode: "lines"
  };
    data.forEach(function(val) {
    trace1.x.push(val["time"]);
    trace1.y.push(val["pm25"]);
    trace2.x.push(val["time"]);
    trace2.y.push(val["pm10"]);
    });
  Plotly.newPlot('AQIplot', [trace1, trace2]);
}; 