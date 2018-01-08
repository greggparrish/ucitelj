// Subscription button for feeds
$(".subButton").click(function () {
  var feed_id = $(this).attr("data-feed");
  var sub_type  = $(this).attr("data-sub");
  var setSub = (sub_type == 'sub') ? 'unsub' : 'sub';
  $.get('/feeds/subscriptions/', {feed_id : feed_id, sub_type : sub_type}, function(data){ });
  $(this).attr('data-sub', setSub);
  $(this).toggleClass('subbed');
  $('#sub_'+feed_id).remove();
  return false;
});


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


// Autocomplete for dictionary
$(".dict_dir").click(function () {
  $(".dict_dir").removeClass('active');
  $(this).addClass('active');
  var textBox = $(this).parent().parent().find('input[type=text]');
  $(textBox).autocomplete("search");
});
$('#autocomplete').autocomplete({
  source:function(request, response) {
    $.getJSON("/practice/define", { q_word: request.term, dict_dir: $('.dict_dir.active').attr('id')}, function(data) {
      response(data.deflist);
    });
},
  minLength: 2,
  select: function(event, ui) {
    $('#search_results').text('');
    $('#search_results').append('<li><span id=\''+ui.item.def_id+'\' class=\'hr-term\' data-add=\'add\'>'+ui.item.label+'</span></li>');
  }
});

// Add extra characters to textbox
$('.extraCharacter').click(function() {
  var addLetter = $(this).text();
  var textBox = $(this).parent().parent().find('input[type=text]');
  var curText = $(textBox).val();
  $(textBox).val(curText+addLetter);
  $(textBox).focus();
});
