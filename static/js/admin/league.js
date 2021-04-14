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
});
