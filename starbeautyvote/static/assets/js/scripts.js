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

  $(document).ready(function(){
    $(".vote-button").click(function(){
      var candidateId = $(this).data('candidate-id');
      var candidateName = $("#userContentName"+candidateId).text();
      var candidateImage = $("#userContentImage"+candidateId).attr('src');
      
      $("#modal_candidate_name").text(candidateName);
      $("#modal_candidate_image").attr('src', candidateImage);

      $(".form-group input").val("");

      $(".numberOfVote").text("Price : 0 FCFA");


    });
  });