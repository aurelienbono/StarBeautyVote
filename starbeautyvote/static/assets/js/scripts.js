document.addEventListener("DOMContentLoaded", function() {
  var votesInput = document.querySelector('input[name="votes"]');
  var priceInput = document.querySelector('input[name="prices"]');
  var priceElement = document.querySelector('.numberOfVote');

  votesInput.addEventListener('input', function() {
    var inputValue = parseInt(votesInput.value);

    if (!isNaN(inputValue)) {
      var newValue = inputValue * 100;
      priceInput.value = newValue;
      priceElement.textContent = "Price : " + newValue + " Fcfa";
    } else {
      priceInput.value = 0; 
      priceElement.textContent = "Price : 0 Fcfa";
    }
  });
});


  $(document).ready(function(){
    $(".vote-button").click(function(){
      var candidateId = $(this).data('candidate-id');
      var candidateName = $("#userContentName"+candidateId).text();
      var candidateImage = $("#userContentImage"+candidateId).attr('src');
      var priceElement = $("#modal_success .numberOfVote");
  
      $("#modal_candidate_name").text(candidateName);
      $("#modal_candidate_image").attr('src', candidateImage);
  
      // Set the candidate ID to the hidden input
      $("#candidate_id_input").val(candidateId);
  
      // Reset the number of votes input
      $(".form-group input[name='votes']").val("");
  
      // Reset the price
      priceElement.text("Price : 0 FCFA");
    });
  
    // Update price when the number of votes changes
    $(".form-group input[name='votes']").on('input', function() {
      var inputValue = parseInt($(this).val());
      var priceElement = $("#modal_success .numberOfVote");
  
      if (!isNaN(inputValue)) {
        var newValue = inputValue * 100;
        priceElement.text("Price : " + newValue + " FCFA");
      } else {
        priceElement.text("Price : 0 FCFA");
      }
    });
  
  });
  