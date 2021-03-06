$(document).ready(function() {
  createVerblist();
});

createVerblist = function() {
  var listContainer = $('#verblistContainer');
  var numLeft = $('.verb-list').length;
  $.getJSON("{{ url_for('practice.verbs') }}", {'load_list': 'True'}, function(data) {
    $.each(data, function(index, value){
      if (index===0) {activate=' active'}else{activate=''};
      listContainer.prepend('<ul class=\'list-unstyled verb-list\' data-pron=\''+value.pronoun_code+'\' data-verb=\''+value.hr_word+'\' data-tense=\''+value.verb_tense+'\' data-hr_id=\''+value.def_id+'\'><li class=\'\' id=\''+value.def_id+'\'><h1>'+value.hr_word+'</h1></li><li class=\'definitions\'>'+value.en_words.join(',')+'</li>{% if current_user.is_authenticated and current_user.has_role('admin') %}<li>[<span id=\'notVerb\' class=\'admin-text\'>not a verb/infinitive</span>]</li>{% endif %}<li class=\'challenge\'><h3>'+value.pronoun_word+' + '+value.verb_tense+' ('+value.pronoun_code+') '+'</h3></li></ul>');
    })
    if (numLeft === 0){
      $('#verblistContainer').find('ul.verb-list').first().addClass('active');
    }
  });
}

nextWord = function() {
  var numLeft = $('.verb-list').length;
  $('.verb-list.active').remove();
  if (numLeft === 2){
    createVerblist();
  }
  $('.verb-list').first().addClass('active');
}

$(document).on('click', '#skipButton', function () {
  event.preventDefault();
  nextWord();
});

$(document).on('click', '#notVerb', function () {
  var hr_id = $('.verb-list.active').data('hr_id');
  $.ajax({
    type: 'POST',
    url: '{{ url_for('practice.rm_verb_role') }}', 
    data: {'hr_id':hr_id },
    success: function (data, response) { nextWord(); }
  });
});

$(document).on('submit', function () {
  event.preventDefault();
  var pronoun = $('.verb-list.active').data('pron');
  var verb_tense = $('.verb-list.active').data('tense');
  var verb = $('.verb-list.active').data('verb');
  var hr_id = $('.verb-list.active').data('hr_id');
  var answer = $('#answerBox').val();
  var numLeft = $('.verb-list').length;
  $('.verb-list.active').remove();
  $.getJSON("/practice/verbs/check", {'pronoun_code':pronoun, 'verb':verb, 'verb_tense':verb_tense, 'answer':answer, 'hr_id':hr_id}, function(data, response) {
    if (data.grade == 'correct') {
      $('#lastWord.correct').prepend('<li><span id=\''+data.hr_id+'\' class=\'hr-term\' data-add=\'add\'>'+data.verb+'</span></li>');
    } else {
      $('#lastWord.incorrect').prepend('<li><span id=\''+data.hr_id+'\' class=\'hr-term\' data-add=\'add\'>You:'+data.answer+' Answer:'+data.correct_answer+'</span></li>');
    }
    $('#answerBox').val('');
  })
  if (numLeft === 2){
    createVerblist();
  }
  nextWord();
});
