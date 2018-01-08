// Autocomplete for dictionary
$(".dict_dir").click(function () {
  $(".dict_dir").removeClass('active');
  $(this).addClass('active');
  var textBox = $(this).parent().parent().find('input[type=text]');
  $(textBox).autocomplete("search");
});
$('#autocomplete').autocomplete({
  source:function(request, response) {
    $.getJSON("/words/define", { q_word: request.term, dict_dir: $('.dict_dir.active').attr('id')}, function(data) {
      response(data.deflist);
    });
},
  minLength: 2,
  select: function(event, ui) {
    $('#search_results').text('');
    $('#search_results').append('<li><span id=\''+ui.item.def_id+'\' class=\'hr-term\' data-add=\'add\'>'+ui.item.label+'</span></li>');
  }
});
