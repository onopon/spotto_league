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

  $('#admin .btn.notify_via_linebot').click(function() {
    var userSelect = $('[name=user-select] option:selected');
    var leagueIdBoxes = $('#admin input[name="league_ids"]:checked');
    var leagueIds = [];
    leagueIdBoxes.toArray().forEach(function(chk) {
      leagueIds.push(parseInt(chk.value));
    });
    confirmMsg = "通知チェック欄にチェックが入ったリーグ戦全てをLINEグループで通知します。よろしいですか？（最大10件）"
      + "\n\nまた、通知には時間がかかる場合がございます。OKボタンを押したら少しお待ちください。";
    if (confirm(confirmMsg)) {
      if (leagueIds.length > 10) {
        alert('同時に通知できる最大件数は10件までです。');
        return false;
      }
      postNotify(leagueIds);
    }
    return false;
  });

  function postNotify(leagueIds) {
      $.ajax({
          url: '/admin/league/notify_recruiting',
          type: "POST",
          data: {'league_ids': leagueIds}
        }).done(function(_){
          alert('通知しました。LINEをご確認ください。');
        }).fail(function(){
          console.log('fail');
        });
  }
});
