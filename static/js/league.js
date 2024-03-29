$(function() {
  let league_id = $('#league_id').text();
  let user_id = $('#user_id').text();
  let game_count;
  let league_log_hash;
  let point_rank_hash;
  let targetId;
  class GameData {
    constructor(league_id, hash, score_1_list, score_2_list) {
      this.league_id = league_id;
      this.hash = hash;
      this.score_1_list = score_1_list;
      this.score_2_list = score_2_list;
    }
    toHash() {
      return { league_id: this.league_id, 
               user_id_1: this.hash.user_id_1,
               user_id_2: this.hash.user_id_2,
               score_1_list: this.score_1_list,
               score_2_list: this.score_2_list };

    }
  }

  $('#target-table td').click(function() {
    targetId = $(this).attr('class');
    let hash = league_log_hash[targetId];
    if (hash == undefined) { return false; }
    for (let i = 0; i < game_count; i++) {
      let detail = hash.details_hash_list[i];
      if (detail == undefined) {
        detail = {"score_1": '', "score_2": ''};
      }
      let count_1 = detail.score_1;
      let count_2 = detail.score_2;
      $(`#modal-body .score_1_${i}`).val(count_1);
      $(`#modal-body .score_2_${i}`).val(count_2);
      $(`#modal-body .result p.score_1_${i}`).text(count_1);
      $(`#modal-body .result p.score_2_${i}`).text(count_2);
    }
    $('#modal-title').text(`${hash.user_name_1} vs ${hash.user_name_2}`);
    $('#detailModal').modal('show');
  });

  $('#modal-save-btn').click(function() {
    var leftScores = $("#detailModal .score-left").map(function (index, el) {
      let score = $(this).val();
      if ($(this).val() == "") {
        score = '0';
      }
      return score;
    }).toArray();
    var rightScores = $("#detailModal .score-right").map(function (index, el) {
      return $(this).val();
    }).toArray();
    let gameData = new GameData(league_id, league_log_hash[targetId], leftScores, rightScores);
    postLeagueLog(gameData);
  });

  $('.number-spinner button').click(function() {
    let btn = $(this);
    let value = btn.closest('.number-spinner').find('input').val().trim();
    if (btn.attr('data-dir') == 'up') {
      value++;
    } else {
      value--;
    }
    btn.closest('.number-spinner').find('input').val(Math.max(0,value));
    return false;
  });

  function postLeagueLog(gameData) {
      $.ajax({
          url: "/league/log",  //POST送信を行うファイル名を指定
          type: "POST",
          data: gameData.toHash()
        }).done(function(data){
          updateData($.parseJSON(data));
        }).fail(function(){
          console.log('fail');
        });
  }

  function loadLeague(league_id) {
    $.ajax({
        url: `/league/${league_id}/json`,
        contentType: 'application/json;charset=UTF-8',
        type: 'GET'
      }).done(function(data){
        setData($.parseJSON(data));
      }).fail(function(){
        console.log('fail');
      });
  }

  function setData(jsonData) {
    game_count = jsonData.game_count;
    league_log_hash = jsonData.league_log_hash;
    point_rank_hash = jsonData.point_rank_hash;
  }

  loadLeague(league_id);

  function updateData(jsonData) {
    for (let key in jsonData) {
      for (let cKey in jsonData[key]) {
        league_log_hash[key][cKey] = jsonData[key][cKey];
      }
    }
    for (let [key, log] of Object.entries(league_log_hash)) {
      let personalGameCount = `${log.count_1} - ${log.count_2}`;
      $(`.${key} .game-count`).text(personalGameCount);
      let scoreLefts = $(`form.personal-record.${key}`).find('input.score-left');
      let scoreRights = $(`form.personal-record.${key}`).find('input.score-right');
      for (let i = 0; i < game_count; i++) {
        let detail = log.details_hash_list[i];
        if (detail == undefined) {
          detail = {"score_1": "", "score_2": ""};
        }
        let count_1 = detail.score_1;
        let count_2 = detail.score_2;
        $(`#modal-body .score_1_${i}`).val(count_1);
        $(`#modal-body .score_2_${i}`).val(count_2);
        if (log.user_id_1 == user_id) {
            scoreLefts.eq(i).val(count_1);
            scoreRights.eq(i).val(count_2);
        }
      }
    }
  }

  $('form.personal-record').submit(function () {
    let form = $(this).closest('form.personal-record');
    let rival_id = form.find('input[name=rival_id]').val();
    let target_id = `${user_id}-${rival_id}`;
    let leftScores = form.find('input.score-left').map(function(){
      return parseInt($(this).val());
    }).get();
    let rightScores = form.find('input.score-right').map(function(){
      return parseInt($(this).val());
    }).get();
    let gameData = new GameData(league_id, league_log_hash[target_id], leftScores, rightScores);
    postLeagueLog(gameData);
    return false;
  });

  $('div.current_point').click(function () {
    let userId = $(this).find('.user_id').text();
    let prh = point_rank_hash[userId];
    let basePoint = prh.current_points_hash.BasePoint.reduce(function(a,b){ return a + b; }, 0);
    let bonusPoint = prh.current_points_hash.BonusPoint.reduce(function(a,b){ return a + b; }, 0);
    let continuousPoint = prh.current_points_hash.ContinuousPoint.reduce(function(a,b){ return a + b; }, 0);
    let league_points = prh.current_points_hash.LeaguePoint;
    $('#pointDetailModal .modal-title').text(`${prh.user_name} さんのポイント内訳`);
    $('#pointDetailModal .base-point').text(`${basePoint}`);
    $('#pointDetailModal .league-point-frame').text(`${prh.current_points_hash.LeaguePoint.length} / 8`);
    $('#pointDetailModal .league-point').text(league_points.join("\n"));
    $('#pointDetailModal .bonus-point').text(`${bonusPoint}`);
    $('#pointDetailModal .continuous-point').text(`${continuousPoint}`);
    $('#pointDetailModal').modal('show'); 
  });

  $('#league button.cancel').click(function() {
    return confirm('募集締切日を過ぎている場合、再度参加希望を出すことはできません。キャンセルしてもよろしいですか？');
  });
});
