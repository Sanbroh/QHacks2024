var textSpaceCount = 1;
var currPage = 1;
var charCount = 1;
var charSel = "Narrator";

window.onload = function() {
  // Immediately go to recommended location
  console.log("JS Running");

  var textSpaceHeight = document.getElementById("text-space").offsetHeight;
  document.getElementById("text-space").style.height = textSpaceHeight + "px";

  for (var i = 0; i < pages.length; i++) {
    if (pages[i].length > 0) {
      newTextSpace(textSpaceCount);
      postMessage(pages[i], "Journey Guide - Page " + textSpaceCount, -1, "center", "text-space-item-" + textSpaceCount);
      var hr = document.createElement('hr');
      document.getElementById("text-space-item-" + textSpaceCount).appendChild(hr);
      if (currPage != textSpaceCount) {
        document.getElementById("text-space-item-" + textSpaceCount).style.display = "none";
      }
      textSpaceCount++;
    }
  }

  // setBackground();
  resetChar();
}

function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

function textToSpeech(elm) {
  var char = elm.getElementsByClassName("text-bubble-txt")[0].children[0].innerHTML;
  try {
    char = char.split("(")[0];
  } catch {
    char = char.split("-")[0];
  }
  var mode = "audio";
  var msg = elm.getElementsByClassName("text-bubble-txt")[0].children[1].innerHTML;
  var filename = makeid(8);
  var character = char;

  var url = "/get_response?" + new URLSearchParams({filename, mode, msg, character});
  fetch(url, {
    "method": "GET"
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    new Audio('/static/audio/' + filename + '.mp3').play();
  });
}

function getChar() {
  var context = document.getElementById("text-space-item-" + currPage);
  for (let i = 0; i < context.children.length; i++) {
    if (context.children[i].style.display == "block") {
      context = context.children[i].children[0].children[1].innerHTML;
      break;
    }
  }
  var mode = "chars";
  var url = "/get_response?" + new URLSearchParams({context, mode});
  fetch(url, {
    "method": "GET"
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    var processData = data.split(",");
    for (var i = 0; i < processData.length; i++) {
      processData[i] = processData[i].replace(/[^a-z]/gi, '');
    }

    if (processData[processData.length-1].toLowerCase() == "true") {
      for (var i = 0; i < processData.length - 1; i++) {
        newChar(processData[i], "/static/images/Narrator.png");
      }
    }
  });
}

function selChar(elm) {
  for (let i = 0; i < document.getElementsByClassName(elm.className).length; i++) {
    document.getElementsByClassName(elm.className)[i].style.opacity = "50%";
  }
  elm.style.opacity = "100%";
  charSel = elm.children[0].children[1].innerHTML;
}

console.log(textSpaceCount);
console.log(currPage);

function newChar(name, img) {
  var selElm = document.getElementById("container-sel");
  var charElm = document.getElementById("default-char").cloneNode(true);

  charElm.id = "char-select-" + charCount;
  charCount++;

  charElm.children[0].children[0].backgroundImage = "url('" + img + "')";
  charElm.children[0].children[1].innerHTML = name;
  charElm.style.display = "block";
  charElm.style.opacity = "50%";

  selElm.appendChild(charElm);
}

function resetChar() {
  var selElm = document.getElementById("container-sel");
  var charElm = document.getElementById("default-char").cloneNode(true);
  selElm.innerHTML = '';
  selElm.appendChild(charElm);

  newChar("Narrator", "/static/images/Narrator.png");

  for (let i = 0; i < document.getElementsByClassName("char-selection").length; i++) {
    document.getElementsByClassName("char-selection")[i].style.opacity = "100%";
  }
}

function generateChar(list) {
  for (var i = 0; i < list.length; i++) {
    var character = list[i];
    newChar(character, "/static/images/Narrator.png");
  }
}

function sendMessage() {
  var textSpace = document.getElementById("text-space");
  var msg = document.getElementById("send-area").value;
  var character = charSel;

  document.getElementById("send-area").value = "";
  postMessage(msg, "You (to " + character + ")", -1, "right", "text-space-item-" + currPage);
  textSpace.scrollTop = textSpace.scrollHeight;

  var context = document.getElementById("text-space-item-" + currPage);
  for (let i = 0; i < context.children.length; i++) {
    if (context.children[i].style.display == "block") {
      context = context.children[i].children[0].children[1].innerHTML;
      break;
    }
  }

  var roleplaying = "User";

  var mode = "response"
  var url = "/get_response?" + new URLSearchParams({context, character, roleplaying, msg, mode})
  fetch(url, {
    "method": "GET"
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.json);
    var elm = postMessage(data, character + " (to You)", -1, "left", "text-space-item-" + currPage);
    textToSpeech(elm);
    textSpace.scrollTop = textSpace.scrollHeight;
  });
}

function postMessage(text, char, img, align, textspace) {
  var elm;
  var textSpace = document.getElementById(textspace);

  if (align == "left") {
    elm = document.getElementById("default-text-bubble-left").cloneNode(true);
    elm.children[1].children[0].innerHTML = char;
    elm.children[1].children[1].innerHTML = text;

    //IMG HERE
  } else if (align == "right") {
    elm = document.getElementById("default-text-bubble-right").cloneNode(true);
    elm.children[0].children[0].innerHTML = char;
    elm.children[0].children[1].innerHTML = text;

    //IMG HERE
  } else {
    elm = document.getElementById("default-text-bubble-center").cloneNode(true);
    elm.children[0].children[0].innerHTML = char;
    elm.children[0].children[1].innerHTML = text;
  }

  textSpace.appendChild(elm);
  elm.style.display = "block";

  textSpace.scrollTop = textSpace.scrollHeight;

  return elm;
}

function newTextSpace(textSpaceCount) {
  var textSpace = document.getElementById("text-space");

  var newTextSpace = document.getElementById("default-text-space-item").cloneNode(true);
  newTextSpace.id = "text-space-item-" + textSpaceCount;

  textSpace.appendChild(newTextSpace);
}

function nextPage() {
  if (!(currPage < textSpaceCount-1)) return;
  currPage++;

  console.log(currPage);

  setBackground();
  resetChar();
  getChar();
  refreshTextSpace(currPage);
}

function prevPage() {
  if (!(currPage > 1)) return;
  currPage--;

  console.log(currPage);

  setBackground();
  resetChar();
  getChar();
  refreshTextSpace(currPage);
}

function setBackground() {
  var context = document.getElementById("text-space-item-" + currPage);
  for (let i = 0; i < context.children.length; i++) {
    if (context.children[i].style.display == "block") {
      context = context.children[i].children[0].children[1].innerHTML;
      break;
    }
  }

  var mode = "background"
  var url = "/get_response?" + new URLSearchParams({context, mode})
  fetch(url, {
    "method": "GET"
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    var backgroundElm = document.getElementById("container-text");
    backgroundElm.style.backgroundImage = "url('" + data + "')";
  });
}

function selectPage() {
  let n = prompt("Please enter the page number:");
  if (n == null || n == "" || n < 1 || n > textSpaceCount) {
    alert("Page number not accepted, please try again!");
    return;
  }
  currPage = n;
  setBackground();
  resetChar();
  getChar();
  refreshTextSpace(currPage);
}

function refreshTextSpace(currPage) {
  var textSpace = document.getElementById("text-space");

  for (var i = 0; i < textSpace.children.length; i++) {
    if (textSpace.children[i].id == "text-space-item-" + currPage) {
      textSpace.children[i].style.display = "block";
    } else {
      textSpace.children[i].style.display = "none";
    }
  }
}
