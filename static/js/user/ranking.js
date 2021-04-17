$(function() {
  let year = $('#year').text();
  let point_rank_hash;

  function loadRanking(year) {
    $.ajax({
        url: `/user/ranking/${year}/json`,
        contentType: 'application/json;charset=UTF-8',
        type: 'GET'
      }).done(function(data){
        setData($.parseJSON(data));
      }).fail(function(){
        console.log('fail');
      });
  }

  function setData(jsonData) {
    point_rank_hash = jsonData.point_rank_hash;
  }

  loadRanking(year);

  $('div.current_point').click(function () {
    let userId = $(this).find('.user_id').text();
    let prh = point_rank_hash[userId];
    let basePoint = prh.current_points_hash.BasePoint.reduce(function(a,b){ return a + b; }, 0);
    let bonusPoint = prh.current_points_hash.BonusPoint.reduce(function(a,b){ return a + b; }, 0);
    let league_points = prh.current_points_hash.LeaguePoint;
    $('#pointDetailModal .modal-title').text(`${prh.user_name} さんのポイント内訳`);
    $('#pointDetailModal .base-point').text(`${basePoint}`);
    $('#pointDetailModal .league-point-frame').text(`${prh.current_points_hash.LeaguePoint.length} / 8`);
    $('#pointDetailModal .league-point').text(league_points.join("\n"));
    $('#pointDetailModal .bonus-point').text(`${bonusPoint}`);
    $('#pointDetailModal').modal('show'); 
  });
});
