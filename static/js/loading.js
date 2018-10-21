var links = document.getElementsByTagName("a");
function initStockLinks() {
  for (var i = 0; i < links.length; i++) {
    if (links[i].getAttribute("stock-link") != "pending") {
      continue;
    }
    links[i].addEventListener("click", function(element) {
      element.preventDefault();
      showPopup();
      exitButton.style.opacity = "0";
      suggestions.style.display = "none";
      if (recentsList) {
        recentsList.style.display = "none";
        recentsTitle.style.display = "none";
      }
      hint.style.display = "none";
      var link = element.target.parentElement;
      searchbox.value = link.getAttribute("name");
      var loadingText = document.createElement("span");
      loadingText.setAttribute("id", "search-hint")
      loadingText.textContent = "Loading information for "
        + link.getAttribute("name") + " ("
        + link.getAttribute("stock") + "), shouldn't be long";
      popup.appendChild(loadingText);
      window.location = link.getAttribute("href");
    });
    links[i].setAttribute("stock-link", "done");
  }
}
