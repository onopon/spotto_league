$(function() {
  let user_id = $('#user_id').text();

  $('.recruiting button.join').click(function() {
    let btn = $(this);
    let recruitingForm = btn.closest('.recruiting');
    let league_id = recruitingForm.find('input[name=league_id]').val().trim();
    postJoin(league_id, recruitingForm);
    return false;
  });

  $('.recruiting button.cancel').click(function() {
    let btn = $(this);
    let recruitingForm = btn.closest('.recruiting');
    let league_id = recruitingForm.find('input[name=league_id]').val().trim();
    postCancel(league_id, recruitingForm);
    return false;
  });

  function postJoin(league_id, recruitingForm) {
      $.ajax({
          url: `/user/league/join`,
          type: "POST",
          data: {'league_id': league_id}
        }).done(function(_){
          recruitingForm.find('button.cancel').removeClass('collapse');
          recruitingForm.find('button.join').addClass('collapse');
        }).fail(function(){
          console.log('fail');
        });
  }

  function postCancel(league_id, recruitingForm) {
      $.ajax({
          url: `/user/league/cancel`,
          type: "POST",
          data: {'league_id': league_id}
        }).done(function(_){
          recruitingForm.find('button.join').removeClass('collapse');
          recruitingForm.find('button.cancel').addClass('collapse');
        }).fail(function(){
          console.log('fail');
        });
  }
});
