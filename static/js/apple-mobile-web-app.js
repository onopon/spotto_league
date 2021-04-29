$(function() {
  $(document).on('click', 'a', function(e){
    val = $(this).attr("href");
    if (val.match(/^(http|https):\/\//i)) {
      return true;
    }
    e.preventDefault();
    location.href = $(this).attr('href') ;
    return false;
  });
});
