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
$(".hr-term").click(function () {
  var word_id = $(this).attr('id');
  var add_type = $(this).attr("data-add");
  var setAdd = (add_type == 'add') ? 'rm' : 'add';
  $.get('/words/wordbank/add/', {word_id : word_id, add_type : add_type}, function(data){ });
  $(this).attr('data-add', setAdd);
  $(this).toggleClass('wb');
  return false;
});


// Autocomplete for dictionary
$(".dict_dir").click(function () {
  $(".dict_dir").removeClass('active');
  $(this).addClass('active');
});
$('#autocomplete').autocomplete({
  source:function(request, response) {
    $.getJSON("/words/define", { q_word: request.term, dict_dir: $('.dict_dir.active').attr('id')}, function(data) {
      response(data.deflist);
    });
},
  minLength: 2,
  select: function(event, ui) {
    $('#search_results').text(ui.item.label);
  }
});
