var pinButtons = document.querySelectorAll(".pin_stock");
pinButtons.forEach(function(element) {
  element.addEventListener("click", function (element) {
    console.log
    var pin_xhr = new XMLHttpRequest();
    if (element.target.getAttribute("pin") == "pin") {
      pin_xhr.open("GET", root + "/add_fav?fav=" + element.target.getAttribute("stock"));
    } else if (element.target.getAttribute("pin") == "unpin") {
      pin_xhr.open("GET", root + "/remove_fav?fav=" + element.target.getAttribute("stock"));
    }
    pin_xhr.responseType = "json";
    pin_xhr.send();
    pin_xhr.button = element.target;
    pin_xhr.onload = function() {
      if (this.response == "success: added") {
        this.button.setAttribute("pin", "unpin");
        this.button.textContent = "Unpin stock";
      } else if (this.response == "success: removed") {
        this.button.setAttribute("pin", "pin");
        this.button.textContent = "Pin stock";
      }
    };
  });
});
