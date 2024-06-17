

  $(document).ready(function(){
    $(".vote-button").click(function(){
      var candidateId = $(this).data('candidate-id');
      var candidateName = $("#userContentName"+candidateId).text();
      var candidateImage = $("#userContentImage"+candidateId).attr('src');
      var priceElement = $("#modal_success .numberOfVote");
  
      $("#modal_candidate_name").text(candidateName);
      $("#modal_candidate_image").attr('src', candidateImage);
  
      $("#candidate_id_input").val(candidateId);
  
      $(".form-group input[name='votes']").val("");
  
      priceElement.text("Price : 0 FCFA");
    });
  
    $(".form-group input[name='votes']").on('input', function() {
      var inputValue = parseInt($(this).val());
      var priceElement = $("#modal_success .numberOfVote");
  
      if (!isNaN(inputValue)) {
        var numberOfVote = inputValue ;
        var numberTranche  = Math.floor(numberOfVote/10)

        var resteOfElements = numberOfVote % 10;
        var totalPrice = (numberTranche * 11 * 100) + (resteOfElements * 100);


        priceElement.text("Price : " + totalPrice + " FCFA");
      } else {
        priceElement.text("Price : 0 FCFA");
      }
    });
  
  });
  