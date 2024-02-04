var textSpaceCount = 1;
var currPage = 1;

window.onload = function() {
  // Immediately go to recommended location
  console.log("JS Running");

  var textSpaceHeight = document.getElementById("text-space").offsetHeight;
  document.getElementById("text-space").style.height = textSpaceHeight + "px";

  for (var i = 0; i < pages.length; i++) {
    if (pages[i].length > 0) {
      newTextSpace(textSpaceCount);
      postMessage(pages[i], "Journey Guide", -1, "center", "text-space-item-" + textSpaceCount);
      if (currPage != textSpaceCount) {
        document.getElementById("text-space-item-" + textSpaceCount).style.display = "none";
      }
      textSpaceCount++;
    }
  }
}

console.log(textSpaceCount);
console.log(currPage);

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

  refreshTextSpace(currPage);
}

function prevPage() {
  if (!(currPage > 1)) return;
  currPage--;

  console.log(currPage);

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
