// Add/rm word from user wordbank
$(document).on('click', '.hr-term', function () {
  var word_id = $(this).attr('id');
  var add_type = $(this).attr("data-add");
  var setAdd = (add_type == 'add') ? 'rm' : 'add';
  $.get('/practice/wordbank/add/', {word_id : word_id, add_type : add_type}, function(data){ });
  $(this).attr('data-add', setAdd);
  $(this).toggleClass('wb');
  return false;
});

// Add extra characters to textbox
$('.extraCharacter').click(function() {
  var addLetter = $(this).text();
  var textBox = $(this).parent().parent().find('input[type=text]');
  var curText = $(textBox).val();
  $(textBox).val(curText+addLetter);
  $(textBox).focus();
  $(textBox).autocomplete("search");
});
