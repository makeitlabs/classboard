/*
 
  displayboard/read/event {
  "color": "#777777",
  "eventcode": 1025,
  "eventstr": "Allowed Entry",
  "icon": ":white_check_mark:",
  "member": "Kevin Towers",
  "tool": "Cleanspace Front Door"
}
Client (null) received PUBLISH (d0, q0, r0, m0, 'displayboard/read/resource/post', ... (74 bytes))
displayboard/read/resource/post {
  "Message": "Kevin Towers was allowed entry at Cleanspace Front Door"
}

*/
var boxesHeight=4611;


function mqtt_init() {
	const mqttClient = mqtt.connect('ws://mqtt:8889/mqtt', {
	  clientId: 'classboard-frontdoor',
	});

	mqttClient.on('close', () => {
	  console.log('close from  to MQTT broker');
	});
	mqttClient.on('error', () => {
	  console.log('error from  to MQTT broker');
	});
	mqttClient.on('end', () => {
	  console.log('Reconnect from  to MQTT broker');
	});
	mqttClient.on('reconnect', () => {
	  console.log('Reconnect from  to MQTT broker');
	});
	mqttClient.on('disconnect', () => {
	  console.log('Disconnected from  to MQTT broker');
	});
	mqttClient.on('connect', () => {
	  console.log('Connected to MQTT broker');
	  mqttClient.subscribe('displayboard/read/event');
	  console.log('Connect Done');
	});

	mqttClient.on('message', (topic, message) => {
		  var j={};
		  console.log(`Received message on ${topic}: ${message.toJSON()}`);
		   try {
			  if (message.toString() != "") {
				j = JSON.parse(message.toString());
			  }
		   } catch (error) {
	 	 }
	if (topic == "displayboard/read/event")  {
		 if ((j["eventcode"]== 1025) && (j["tool"] == "Cleanspace Front Door")) {
			  var x = document.getElementById("alert");
				document.getElementById('alert_text').innerHTML=j["member"];
				console.log(j);
				x.classList.remove("hidealert");
				x.classList.add("showalert");
				if (alertTimer != null) {
					clearTimeout(alertTimer);
				}
				alertTimer = setTimeout(
					function() {
			  var x = document.getElementById("alert");
					x.classList.add("hidealert");
					x.classList.remove("showalert");
					alertTimer=null;
					},7*1000);
				}
			}
		}
	)

}



async function fetchData() {
    const url = 'upcomming_cal.cgi'; // Replace with your desired URL
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }
        const jsonData = await response.json();
	console.log("FETCHED DATA");
        console.log(jsonData); // Use the JSON data as needed
	var enclosingDiv = document.getElementById('calendar');
	var h4 = document.createElement('h4');
	h4.textContent="Upcomming Room Reservations";
	enclosingDiv.replaceChildren(h4);
	var first=true;
	for (var c in jsonData) {
		var e = jsonData[c];

		if (!first) {
			enclosingDiv.appendChild(document.createElement('hr'));
		}
		const div1 = document.createElement('div');
		div1.style.display = 'flex';
		div1.style.justifyContent = 'space-between';
		div1.innerHTML = '<div style="text-align:left"><b>'+e['ROOM']+'</b></div>' +
				 '<div style="text-align:right"><b>'+e['WHEN']+'</b></div>';

		enclosingDiv.appendChild(div1);

		const div2 = document.createElement('div');
		div2.style.display = 'flex';
		div2.style.justifyContent = 'space-between';
		div2.innerHTML = '<div style="text-align:left">'+e['SUMMARY']+'</div>' +
				 '<div style="text-align:right"><i>'+e['ORGANIZER']+'</i></div>';

		enclosingDiv.appendChild(div2);
		first = false;
	}
    } catch (error) {
        console.error('Error fetching data:', error);
    }

    setTimeout(function(){
	    fetchData();
    },1000*60*15);
}


function autoRefresh() {
        window.location.reload(true);
}

function loadinit() {
    // Get references to elements

    window.scrollTo(0,0);
    const scrollContainer = document.querySelector('.scroll-container');
    const boxesContainer = document.querySelector('.boxes-container');
    const boxesContainer2 = document.querySelector('.boxes-container2');

    // Calculate animation duration based on box count
    const boxHeight = boxesContainer.offsetHeight;
    const animationDuration = 5000 * (boxHeight * 2 / window.innerHeight);

    // Set animation duration dynamically
    boxesContainer.style.animationDuration = `${animationDuration}ms`;
    boxesContainer2.style.animationDuration = `${animationDuration}ms`;
    // Scroll to stored position if hash exists

    const boxesHeight = document.querySelector('.boxes-container').offsetHeight +20 ; // - window.innerHeight;
    const animationEnd = "translateY(-${boxesHeight}px)"; // Adjust depending on animation direction
    var secs = document.querySelector('.boxes-container').childElementCount;
    secs *= 6;

    //document.documentElement.style.setProperty('--scroll-end', animationEnd);
    document.documentElement.style.setProperty('--scroll-end', "-"+boxesHeight.toString()+"px");
    document.documentElement.style.setProperty('--scroll-end2', "-"+(boxesHeight*1).toString()+"px");
    document.documentElement.style.setProperty('--scroll-end3', boxesHeight.toString()+"px");
    document.documentElement.style.setProperty('--animation-time', secs.toString()+"s");
    boxesContainer.classList.toggle('animated');
    boxesContainer2.classList.toggle('animated');

    setTimeout(function(){
    window.scrollTo(0,0);
    },1000);


	console.log("PAGE RELOAD");
    setInterval('autoRefresh()', 1000*60*60*4); // Refresh every 4 hours

	fetchData();
}
