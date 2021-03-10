$(function() {
  $('#target-table td').on('click', function() {
    var td = $(this)[0];
    let hash = league_log_hash[td.id];
    let counts = [];
    hash.details_hash_list.forEach (details_hash => {
      counts.push(`<p>${details_hash.score_1} - ${details_hash.score_2}</p>`);
    });
    $('#modal-title').text(`${hash.user_name_1} vs ${hash.user_name_2}`);
    $('#modal-body').html(counts.join(""));
    $('#detailModal').modal('show');
  });

  let league_id = $('#league_id').text();
  $.ajax({
      url: `/league/${league_id}/json`,
      contentType: 'application/json;charset=UTF-8',
      type: 'GET'
    }).done(function(data){
      setData($.parseJSON(data));
    }).fail(function(){
      console.log('fail');
    });

  let game_count;
  let league_log_hash;
  function setData(jsonData) {
    game_count = jsonData.game_count;
    league_log_hash = jsonData.league_log_hash;
    for (let [key, log] of Object.entries(league_log_hash)) {
      $(`#${key}`).text(`${log.count_1} - ${log.count_2}`);
    }
  }
});
