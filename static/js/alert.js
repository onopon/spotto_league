$(function() {
  /**
   * アラート要素を生成する
   */
  function alert(msg) {
    return $('<div class="alert" role="alert"></div>')
      .text(msg);
  }

  const e = alert('this is alert.').addClass('alert-warning');
  $('#alert').append(e);

  // 3秒後にアラートを消す
  setTimeout(() => {
    $('#login .alert').alert('close');
  }, 3000);
});
