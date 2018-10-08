"use strict";

var searchbox = document.querySelector(".symbol-search > input");
var popup = document.getElementById("search-popup");
var suggestions = document.getElementById("search-suggestions");
var hint = document.getElementById("search-hint");
var exitButton = document.getElementById("exit-search");

document.querySelectorAll(".symbol-search").forEach(function(element) {
  element.addEventListener("submit", function(element) {
    element.preventDefault();
  });
});

searchbox.addEventListener("input", function(element) {
  if (element.target.value.length > 0) {
    hint.style.display = "none";
    var xhr = new XMLHttpRequest();
    xhr.open("GET", root + "/stocks?q=" + element.target.value);
    xhr.responseType = "json";
    xhr.send();
    xhr.onload = function() {
      if (searchbox.value.length == 0) {
        return;
      }
      while (suggestions.firstChild) {
        suggestions.removeChild(suggestions.firstChild);
      }
      for (var e in xhr.response) {
        var suggestion = document.createElement("li");
        var link = document.createElement("a");
        var symbol = document.createElement("span");
        link.setAttribute("href", root + "/stock/" + xhr.response[e].symbol);
        link.textContent = xhr.response[e].name;
        symbol.textContent = xhr.response[e].symbol;
        suggestions.appendChild(suggestion);
        suggestion.appendChild(link);
        link.appendChild(symbol);
        link.addEventListener("click", function(element) {
          element.preventDefault();
          exitButton.style.opacity = "0";
          exitButton.style.visibility = "hidden";
          suggestions.style.display = "none";
          var loadingText = document.createElement("span");
          loadingText.setAttribute("id", "search-hint")
          loadingText.textContent = "Loading information for "
            + element.target.childNodes[0].textContent + " ("
            + element.target.childNodes[1].textContent + "), shouldn't be long";
          popup.appendChild(loadingText);
          window.location = element.target.getAttribute("href");
        });
      }
    };
  } else {
    while (suggestions.firstChild) {
      suggestions.removeChild(suggestions.firstChild);
    }
  }
});
searchbox.addEventListener("focus", function(element) {
  popup.style.visibility = "visible";
  popup.style.transitionDelay = "0.2s"
  popup.style.opacity = "1";
  searchbox.style.top = "0.5rem";
});
document.getElementById("exit-search").addEventListener("click", function(element) {
  popup.style.transitionDelay = "0s"
  popup.style.opacity = "0";
  if (searchBoxTop) {
    searchbox.style.top = searchBoxTop;
  } else {
    searchbox.style.top = "2rem";
  }
});
popup.addEventListener("transitionend", function(element) {
  if (element.target.style.opacity == "0") {
    element.target.style.visibility = "hidden";
  }
});
