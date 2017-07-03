(function () {
    if (window.addEventListener) {
        window.addEventListener('load', run, false);
    } else if (window.attachEvent) {
        window.attachEvent('onload', run);
    }

    function run() {
        var t = document.getElementById('myTable');
        t.onclick = function (event) {
            event = event || window.event; //IE8
            var target = event.target || event.srcElement;
            while (target && target.nodeName != 'TR') { // find TR
                target = target.parentElement;
            }
            var cells = target.cells; //cell collection - https://developer.mozilla.org/en-US/docs/Web/API/HTMLTableRowElement
          
            if (!cells.length || target.parentNode.nodeName == 'THEAD') {
                return;
            }
            var f1 = document.getElementById('midinput');
            f1.value = cells[0].innerHTML;
            //console.log(target.nodeName, event);
			
			//Prediction Result
			let url = "http://127.0.0.1:3001/prediction/";
		let input = document.getElementById("midinput");
		url = url + parseInt(input.value);

		console.debug(input.value);
		let xmlHttp = new XMLHttpRequest(); //ajax call to directly access the prediction api
		xmlHttp.open( "GET", url, false ); // false for synchronous request
		xmlHttp.send(null);

		result = JSON.parse(xmlHttp.responseText);
		document.getElementById('predictiondisplay').innerHTML = 
		result['name'] +" has a win percentage of " + result['prob'] + "%";
			
			
        };
    }

})();