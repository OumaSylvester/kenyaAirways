// $(function() {
//     var print = function(msg) {
//       alert(msg);
//     };

//     var setInvisible = function(elem) {
//       elem.css('visibility', 'hidden');
//     };
//     var setVisible = function(elem) {
//       elem.css('visibility', 'visible');
//     };

//     var schedulesElem = $("#schedules");
//     var schedules = schedulesElem.children();

//     // Inserting Buttons
//     schedulesElem.prepend('<div id="right-button" class="" style="visibility: hidden;"><a href="#" id="a-right"><</a></div>');
//     schedulesElem.append('  <div id="left-button" class=""><a href="#" id="a-left">></a></div>');

//     // Inserting Inner
//     schedules.wrapAll('<div id="inner" />');

//     // Inserting Outer
//     // debugger;
//     schedulesElem.find('#inner').wrap('<div id="outer"/>');

//     var outer = $('#outer');

//     var updateUI = function() {
//       var maxWidth = outer.outerWidth(true);
//       var actualWidth = 0;
//       $.each($('#inner >'), function(i, item) {
//         actualWidth += $(item).outerWidth(true);
//       });

//       if (actualWidth <= maxWidth) {
//         setVisible($('#left-button'));
//       }
//     };
//     updateUI();



//     $('#right-button').click(function() {
//       var leftPos = outer.scrollLeft();
//       outer.animate({
//         scrollLeft: leftPos - 200
//       }, 800, function() {
//         // debugger;
//         if ($('#outer').scrollLeft() <= 0) {
//           setInvisible($('#right-button'));
//         }
//       });
//     });

//     $('#left-button').click(function() {
//       setVisible($('#right-button'));
//       var leftPos = outer.scrollLeft();
//       outer.animate({
//         scrollLeft: leftPos + 200
//       }, 800);
//     });

//     $(window).resize(function() {
//       updateUI();
//     });
//   });




const scrollableContainer = document.querySelector('.scrollable-container');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const itemWidth = 50; // Adjust this based on your item width and margin

prevBtn.addEventListener('click', () => {
  scrollableContainer.scrollBy({
      left: -itemWidth,
      behavior: 'smooth'
  });
  console.log("Scroll left")
});

nextBtn.addEventListener('click', () => {
  scrollableContainer.scrollBy({
      left: itemWidth,
      behavior: 'smooth'
  });
  console.log("Scroll right")
});


document.getElementById('schedules').addEventListener('click', displayTimes);

function displayTimes(e){
    let target = e.target;
    // let targetid = e.target.id;
    if(target.hasAttribute('data-schedule-id')){//className.includes('item') && (target.id.includes('date') || target.tagName == 'span')){
        let scheduleId = target.getAttribute('data-schedule-id')
        console.log('Schedule '+scheduleId);
        localStorage.setItem('scheduleId', scheduleId);
        let dateItem = document.getElementById('date'+scheduleId);
        dateItem.classList.remove('bg-white');
        dateItem.classList.add('active-2');

        // make a function to get all siblings of an element. Hint: use prevSibling, nextSibling
        let siblings = $('#date' + scheduleId).siblings();
        for(let i=0; i<siblings.length; i++){
          siblings[i].classList.remove('acive-2');
          siblings[i].classList.add('bg-white');
          console.log('sibling: ')
        }

        let scheduleElem = document.getElementById(scheduleId);
        console.log('Classes: ' + dateItem.classList);
        let dep_date = scheduleElem.getAttribute('data-date-dep');
        document.getElementById('side_dep_date').innerHTML = "Departure Date: " + dep_date;
        console.log("Date: " + dep_date);

        let schedules = document.getElementById('schedules-table')
        for(let i=0; i<schedules.children.length; i++){
            schedules.children[i].className = 'hide';
        }
        scheduleElem.className = 'show';
    }
   
}

document.getElementById('add_flight_details').addEventListener('click', add_pass_and_booking);
function add_pass_and_booking(e){
  // e.preventDefault();
  timeId = localStorage.getItem('timeId');
  seatClass = localStorage.getItem('seatClass');
  scheduleId = localStorage.getItem('scheduleId')
  console.log(JSON.stringify({'schedule_id': scheduleId, 'time_id': timeId, 'seat_class': seatClass}))
  fetch('http://127.0.0.1:8000/flight_details/', {
    method: 'POST',
    body: JSON.stringify({'schedule_id': scheduleId, 'time_id': timeId, 'seat_class': seatClass}),
    redirect: 'follow',
    headers: {
      'Content-type': 'application/json',
    }

  })
  .then(response =>{
    if (response.redirected) {
      window.location.href = response.url;
    }
  })

}
  // .then(()=>{
    // console.log(Response.body)
    // fetch('http://127.0.0.1:8000/passenger/')
    // .then(()=>{
    //   fetch('http://127.0.0.1:8000/pay/', {'method': 'POST'})
    //   .then(()=>{
    //     console.log("Smooth");
    //   })
    // })
  // })


document.getElementById('schedules-table').addEventListener('click', add_to_booking_store)

function add_to_booking_store(e){
  target = e.target
  console.log(target);
  if(!target.hasAttribute('data-time-id')){
    target = target.parentElement;
  }
  if(target.hasAttribute('data-time-id')){
    let timeId = target.getAttribute('data-time-id')
    let seatClass = target.children[0].innerHTML;
    let dep_time = target.getAttribute('data-time-dep');
    
    // Set chosen time, date and seatclass in the sidebar
   
    document.getElementById('side_dep_time').innerHTML ="Departue Time: " + dep_time;
    document.getElementById('side_seat_class').innerHTML = seatClass;
    localStorage.setItem('timeId', timeId);
    localStorage.setItem('seatClass', seatClass)
  }else{
    console.log('Not even close')
  }
}


