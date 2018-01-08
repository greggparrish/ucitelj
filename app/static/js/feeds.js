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
