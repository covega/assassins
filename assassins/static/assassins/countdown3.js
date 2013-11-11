function Countdown(seconds, elemID){
    var self = this;
    this.seconds = seconds;
    this.elemID = elemID;
    document.getElementById(elemID).innerHTML = this.secondsToOutputString();
    this.timerInstance = setInterval(function(){self.timer()}, 1000);
}

Countdown.prototype.timer = function(){
    // Decrement timer
    this.seconds -= 1;

    // Clear timer if finished
    if (this.seconds < 0)
    {
	clearInterval(this.timerInstance);
	return;
    }

    // Display time left
    document.getElementById(this.elemID).innerHTML=this.secondsToOutputString();
};

Countdown.prototype.secondsToOutputString = function(){
    var secondsLeft = this.seconds;

    var hours = Math.floor(secondsLeft / 3600);
    secondsLeft = secondsLeft % 3600;

    var minutes = Math.floor(secondsLeft / 60);
    var seconds = secondsLeft % 60;

    // Enforce each unit of time have at least two digits
    var hoursStr = ("00" + hours).substr(-2);
    var minutesStr = ("00" + minutes).substr(-2);
    var secondsStr = ("00" + seconds).substr(-2);

    return hoursStr + ":" + minutesStr + ":" + secondsStr;
};