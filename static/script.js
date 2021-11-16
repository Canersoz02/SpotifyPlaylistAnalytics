var average;
function onReceiveData(data){
	console.log("RECEIVED RESULT", data)
	average = data;
	CanvasJS.addColorSet("greenShades",	["#2AF048"]);
	var chart = new CanvasJS.Chart("chartContainer", {
		theme: "dark1", // "light2", "dark1", "dark2"
		animationEnabled: false, // change to true
		backgroundColor: '#FFFFFF',
		colorSet: "greenShades",
		backgroundColor: "#110E2B",
			title:{ text: data.name },
			data: [{
					// Change type to "bar", "area", "spline", "pie",etc.
					type: "column",
					dataPoints: data.data
				}]
	});
	chart.render();
}

function onSubmit(){
	console.log("submit")
	input = document.getElementById("fn").value;
	console.log(input.value);
	$.ajax({
    url : "/prediction", // Url of backend (can be python, php, etc..)
    contentType: "application/json",
    dataType: "json",
    type: "POST", // data type (can be get, post, put, delete)
    data : JSON.stringify({"data":average.raw_data, "input": input}),// data in json format
    success: function(response, textStatus, jqXHR) {
    	console.log(response);
	    document.getElementById("result").innerHTML = response.result;
    },
    error: function (jqXHR, textStatus, errorThrown) {
		console.log(jqXHR);
      	console.log(textStatus);
      	console.log(errorThrown);
    }
	});
}

function deneme(ret){
	console.log(ret)
	console.log('returned')
}

function onLoad(){
	console.log("IMPORT EDILDIM", link)
	console.log("SENDING REQUEST")
	$.getJSON("/data/"+link, onReceiveData);
}

window.onload = onLoad;