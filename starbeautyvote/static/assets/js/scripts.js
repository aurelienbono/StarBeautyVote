document.addEventListener("DOMContentLoaded", function() {
    var inputElement = document.querySelector('.form-control');

    var priceElement = document.querySelector('.numberOfVote');

    inputElement.addEventListener('input', function() {
      var inputValue = parseInt(inputElement.value);

      if (!isNaN(inputValue)) {
        var newValue = inputValue * 100;
        
        priceElement.textContent = "Price : " + newValue + " Fcfa";
      } else {
        priceElement.textContent = "Price : 0 Fcfa";
      }
    });
  });