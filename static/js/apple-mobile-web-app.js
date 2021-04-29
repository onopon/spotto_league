// Initialization
jQuery.mobile_js_link = {
	init: function() {
		for (module in jQuery.mobile_js_link) {
			if (jQuery.mobile_js_link[module].init)
				jQuery.mobile_js_link[module].init();
		}
	}
};
jQuery(document).ready(jQuery.mobile_js_link.init);
jQuery.mobile_js_link.rewrite = {
  init: function() {
    var ua = navigator.userAgent;
    if(ua.indexOf('iPhone') > 0 || ua.indexOf('iPod') > 0 || ua.indexOf('Android') > 0 && ua.indexOf('Mobile') > 0){}
    else if(ua.indexOf('iPad') > 0 || ua.indexOf('Android') > 0){}
    else{
      return;
    }
    var all_tags = $('a');
    all_tags.each(function(){
      var url = $(this).attr('href');
      if (url.match(/^(http|https):\/\//i)) {
        return;
      }
      $(this).attr('href','#');
      $(this).click(function(){
        location.href = url;
      });
    });
  }
};
