$(function() {
  function countCheck() {
    var capacity = parseInt($("#capacity").text());
    var checks = $('#admin-league input[name="enabled_league_member_ids"]:checked').length;
    $("#check-count").text(checks);
    if (checks > capacity) {
      $("#check-count").addClass("red");
    } else {
      $("#check-count").removeClass("red");
    }
  }

  $('#admin-league input[name="enabled_league_member_ids"]').click(function() {
    countCheck();
  });
  countCheck();

  $('#admin-league .btn.register').click(function() {
    var capacity = parseInt($("#capacity").text());
    var checks = $('#admin-league input[name="enabled_league_member_ids"]:checked').length;
    if (checks < 2) {
      alert('2人以上チェックを入れないと開催できません。');
      return false;
    }
    if (checks > capacity) {
      return confirm('参加者数が許容人数を超えてしまっていますが、よろしいですか？');
    }
  });

  $('#admin-league .btn.force-join').click(function() {
    var userSelect = $('[name=user-select] option:selected');
    if (confirm(`${userSelect.text()}さんを飛び入り参加させてもよろしいですか？`)) {
      var leagueId = parseInt($("#league_id").text());
      var loginName = userSelect.val();
      postForceJoin(leagueId, loginName);
    }
    return false;
  });

  function postForceJoin(leagueId, loginName) {
      $.ajax({
          url: `/user/league/join`,
          type: "POST",
          data: {'league_id': leagueId, 'login_name': loginName, 'force_join': true}
        }).done(function(_){
          window.location.href = `/admin/league/${leagueId}`;
        }).fail(function(){
          console.log('fail');
        });
  }
});
