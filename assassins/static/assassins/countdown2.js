var secsRemaining;
var timerInstance;

function countdown(seconds){
    document.getElementById("timer").innerHTML = secondsToOutputString(seconds);
    secsRemaining = seconds;
    timerInstance = setInterval(timer, 1000);
}

function timer()
{
    secsRemaining -= 1;
    if (secsRemaining < 0)
    {
	clearInterval(timerInstance);
     //counter ended, do something here
	return;
    }

    //Do code for showing the number of seconds here
    document.getElementById("timer").innerHTML=secondsToOutputString(secsRemaining);
}                                                                                  
function secondsToOutputString(seconds){
    secondsLeft = seconds;

    hours = Math.floor(secondsLeft / 3600);
    secondsLeft = secondsLeft % 3600;

    minutes = Math.floor(secondsLeft / 60);
    seconds = secondsLeft % 60;

    // Enforce each unit of time have at least two digits
    hoursStr = ("00" + hours).substr(-2);
    minutesStr = ("00" + minutes).substr(-2);
    secondsStr = ("00" + seconds).substr(-2);
    //secondsStr = ("00" + seconds).substr(2 - (""+seconds).length, 2);

    return hoursStr + ":" + minutesStr + ":" + secondsStr;
}