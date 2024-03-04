
    var boxesHeight=4611;


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
    function autoRefresh() {
        window.location.reload(true);
    }
    setInterval('autoRefresh()', 1000*60*60*4); // Refresh every 4 hours

	fetchData();
}
