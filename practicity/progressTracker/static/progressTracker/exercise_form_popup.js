function openForm() {
    document.getElementById("executionForm").style.display = "block";
    let arg1 = event.target.getAttribute('data-arg1');
  
    var date = new Date();
    var currentDate = date.toISOString().slice(0,10);
    var currentTime = date.getHours() + ':' + date.getMinutes();
  
    // pre-fill form:
    document.getElementById("id_exercise").value = arg1;
    document.getElementById("id_start").value = currentDate + " " + currentTime;
  
    // Start Practice timer
    var h1 = seconds = 0, minutes = 0, hours = 0
  
    function add() {
      seconds++;
      if (seconds >= 60) {
          seconds = 0;
          minutes++;
          if (minutes >= 60) {
              minutes = 0;
              hours++;
          }
      }
  
      document.getElementById("id_timer").value = (hours ? (hours > 9 ? hours : "0" + hours) : "00") + ":" + (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds);
  
      timer();
      }
      function timer() {
          t = setTimeout(add, 1000);
      }
  
      timer();
  }
  
  function closeForm() {
    document.getElementById("executionForm").style.display = "none";
  }
  
  function getTime() {
    var date = new Date()
    var currentDate = date.toISOString().slice(0,10);
    var currentTime = date.getHours() + ':' + date.getMinutes();
  
    document.getElementById("id_end").value = currentDate + " " + currentTime;
  }