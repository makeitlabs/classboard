
    var boxesHeight=4611;

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
}
