"use strict";

var searchbox = document.querySelector(".symbol-search > input");
var popup = document.getElementById("search-popup");
var suggestions = document.getElementById("search-suggestions");
var hint = document.getElementById("search-hint");
var exitButton = document.getElementById("exit-search");
var home = document.querySelector("header > a");
var account = document.querySelector("header > div");
var recentsList = document.getElementById("recent-stocks");
var recentsTitle = document.getElementById("recent-title");

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
          suggestions.style.display = "none";
          if (recentsList) {
            recentsList.style.display = "none";
            recentsTitle.style.display = "none";
          }
          hint.style.display = "none";
          searchbox.value = element.target.childNodes[0].textContent;
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
  popup.style.opacity = "1";
  exitButton.style.visibility = "visible";
  exitButton.style.opacity = "1";
  account.style.opacity = "0";
  home.style.opacity = "0";
  searchbox.setAttribute("id", "active-search");
});
document.getElementById("exit-search").addEventListener("click", function(element) {
  popup.style.opacity = "0";
  exitButton.style.opacity = "0";
  account.style.visibility = "visible";
  account.style.opacity = "1";
  home.style.visibility = "visible";
  home.style.opacity = "1";
  searchbox.removeAttribute("id");
});
popup.addEventListener("transitionend", hide);
home.addEventListener("transitionend", hide);
account.addEventListener("transitionend", hide);
exitButton.addEventListener("transitionend", hide);

var recents = document.querySelectorAll("#recent-stocks a");
recents.forEach(function(element) {
  element.addEventListener("click", function(element) {
    element.preventDefault();
    exitButton.style.opacity = "0";
    suggestions.style.display = "none";
    if (recentsList) {
      recentsList.style.display = "none";
      recentsTitle.style.display = "none";
    }
    hint.style.display = "none";
    searchbox.value = element.target.getAttribute("name");
    var loadingText = document.createElement("span");
    loadingText.setAttribute("id", "search-hint")
    loadingText.textContent = "Loading information for "
      + element.target.getAttribute("name") + " ("
      + element.target.getAttribute("stock") + "), shouldn't be long";
    popup.appendChild(loadingText);
    window.location = element.target.getAttribute("href");
  });
});

function hide(element) {
  if (element.target.style.opacity == "0") {
    element.target.style.visibility = "hidden";
  }
}
