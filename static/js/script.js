// import html2canvas from 'html2canvas';
// import { jsPDF } from "jspdf";

window.onload = function() {
  // Immediately go to recommended location
  console.log("JS Running");

  presentation = document.querySelector(".presentation");
  slides = document.querySelectorAll(".slide");
  currentSlide = document.querySelector(".slide.show");

  slideNumber = document.querySelector(".counter");
  toLeftBtn = document.querySelector("#left-btn");
  toRightBtn = document.querySelector("#right-btn");

  presentationController = document.querySelector("#presentation-area");
  toFullScreenBtn = document.querySelector("#full-screen");
  toSmallScreenBtn = document.querySelector("#small-screen");

  init();

  slideNumber.innerText = `1 of ${totalSlides}`;

  checkButtonPress();
}

// get elements
let presentation = document.querySelector(".presentation");
let slides = document.querySelectorAll(".slide");
let currentSlide = document.querySelector(".slide.show");

var slideNumber = document.querySelector(".counter");
var toLeftBtn = document.querySelector("#left-btn");
var toRightBtn = document.querySelector("#right-btn");

let presentationController = document.querySelector("#presentation-area");
var toFullScreenBtn = document.querySelector("#full-screen");
var toSmallScreenBtn = document.querySelector("#small-screen");

// initailize defualt values
var screenStatus = 0;
var currentSlideNo = 1;
var totalSlides = 0;
var scriptStatus = 0;

function init() {
  getCurrentSlideNo();
  totalSlides = slides.length;
  setSlideNo();
}

// handle clicks on left and right icons
toLeftBtn.addEventListener("click", moveToLeftSlide);
toRightBtn.addEventListener("click", moveToRightSlide);

// handle full screen and small screen modes
toFullScreenBtn.addEventListener("click", fullScreenMode);
toSmallScreenBtn.addEventListener("click", smallScreenMode);

// moves to left slide
function moveToLeftSlide() {
  if (currentSlideNo <= 1) return;
  var tempSlide = currentSlide;
  currentSlide = currentSlide.previousElementSibling;
  tempSlide.classList.remove("show");
  currentSlide.classList.add("show");

  tempSlide.classList.remove("downloadable");
  currentSlide.classList.add("downloadable");
  console.log("Moved Left");

  init();
  document.getElementById("scripts-content").innerText = document.getElementById("scripts-content-hidden").children[currentSlideNo+1].innerText;
  document.getElementById("scripts-index").innerText = "Slide " + String(currentSlideNo);
}

// moves to right slide
function moveToRightSlide() {
  if (currentSlideNo >= totalSlides) return;
  var tempSlide = currentSlide;
  currentSlide = currentSlide.nextElementSibling;
  tempSlide.classList.remove("show");
  currentSlide.classList.add("show");
  tempSlide.classList.remove("downloadable");
  currentSlide.classList.add("downloadable");

  console.log("Moved Right");

  init();
  document.getElementById("scripts-content").innerText = document.getElementById("scripts-content-hidden").children[currentSlideNo+1].innerText;
  document.getElementById("scripts-index").innerText = "Slide " + String(currentSlideNo);
}

// get current slide
function getCurrentSlideNo() {
  let counter = 0;

  slides.forEach((slide, i) => {
    counter++;

    if (slide.classList.contains("show")) {
      currentSlideNo = counter;
      if (currentSlideNo <= 1) {
        currentSlideNo = 1;
      } else if (currentSlideNo >= totalSlides) {
        currentSlideNo = totalSlides;
      }
    }
  });
}

// go full screen
function fullScreenMode() {
  if (screenStatus == 0) {
    presentationController.classList.add("full-screen");

    console.log("FullScreen On");
    screenStatus = 1;

    toFullScreenBtn.children[0].classList = "fas fa-compress";
  } else {
    presentationController.classList.remove("full-screen");

    console.log("FullScreen Off");

    screenStatus = 0;

    toFullScreenBtn.children[0].classList = "fas fa-expand";
  }
}

// update counter
function setSlideNo() {
  slideNumber.innerText = `${currentSlideNo} of ${totalSlides}`;
}

// key press
function checkButtonPress() {
  document.body.addEventListener("keydown",function(e){
      e = e || window.event;
      var key = e.which || e.keyCode; // keyCode detection
      var ctrl = e.ctrlKey ? e.ctrlKey : ((key === 17) ? true : false); // ctrl detection

      if ( key == 37 && screenStatus ) {
        moveToLeftSlide();
      } else if ( key == 39 && screenStatus ) {
        moveToRightSlide();
      } else if ( key == 27 && screenStatus) {
        fullScreenMode();
      }

  },false);
}

function downloadScreen() {
    var HTML_Width = $(".downloadable").width();
    var HTML_Height = $(".downloadable").height();
    // var PDF_Width = HTML_Width + (top_left_margin * 2);
    // var PDF_Height = (PDF_Width * 1.5) + (top_left_margin * 2);
    var canvas_image_width = HTML_Width;
    var canvas_image_height = HTML_Height;

    // var totalPDFPages = Math.ceil(HTML_Height / PDF_Height) - 1;
    var totalPDFPages = totalSlides;

    html2canvas($(".presentation")[0]).then(function (canvas) {
        var imgData = canvas.toDataURL("image/jpeg", 1.0);
        var pdf = new jsPDF('l', 'pt', [HTML_Width, HTML_Height]);
        pdf.addImage(imgData, 'JPG', 0, 0, canvas_image_width, canvas_image_height);
        // for (var i = 1; i <= totalPDFPages; i++) {
        //     pdf.addPage(HTML_Width, HTML_Height);
        //     pdf.addImage(imgData, 'JPG', top_left_margin, -(HTML_Height*i)+(top_left_margin*4),canvas_image_width,canvas_image_height);
        // }
        pdf.save("slide" + String(currentSlideNo) + ".pdf");
    });
}

function toggleScript() {
  if (scriptStatus == 0) {
    document.getElementById("scripts-toggle").style.right = "17.5vw";
    document.getElementById("scripts").style.display = "block";
    scriptStatus = 1;
  } else {
    document.getElementById("scripts-toggle").style.right = 0;
    document.getElementById("scripts").style.display = "none";
    scriptStatus = 0;
  }
}

function load(e) {
  console.log("loading");
  var error = 0;
  if (document.getElementById("prompt").value.replace(/\s/g, '') == "") {
    document.getElementById("prompt").style.borderStyle = "solid";
    document.getElementById("prompt").style.borderWidth = "4px";
    document.getElementById("prompt").style.borderColor = "#c10a28";
    error++;
    e.preventDefault();
  } else {
    document.getElementById("prompt").style.borderStyle = "none";
    document.getElementById("prompt").style.borderBottomStyle = "solid";
    document.getElementById("prompt").style.borderColor = "black";
    document.getElementById("prompt").style.borderWidth = "2px";
  }

  if (document.getElementById("logo").value.replace(/\s/g, '') == "") {
    document.getElementById("logo").style.borderStyle = "solid";
    document.getElementById("logo").style.borderWidth = "4px";
    document.getElementById("logo").style.borderColor = "#c10a28";
    error++;
    e.preventDefault();
  } else {
    document.getElementById("logo").style.borderStyle = "none";
    document.getElementById("logo").style.borderBottomStyle = "solid";
    document.getElementById("logo").style.borderColor = "black";
    document.getElementById("logo").style.borderWidth = "2px";
  }

  if (document.getElementById("length").value.replace(/\s/g, '') == "") {
    document.getElementById("length").style.borderStyle = "solid";
    document.getElementById("length").style.borderWidth = "4px";
    document.getElementById("length").style.borderColor = "#c10a28";
    error++;
    e.preventDefault();
  } else {
    document.getElementById("length").style.borderStyle = "none";
    document.getElementById("length").style.borderBottomStyle = "solid";
    document.getElementById("length").style.borderColor = "black";
    document.getElementById("length").style.borderWidth = "2px";
  }

  if (error == 0) {
    document.getElementById("loading").style.display = "block";
    console.log("Success! Generating!");
  }

  // e.preventDefault();
}
