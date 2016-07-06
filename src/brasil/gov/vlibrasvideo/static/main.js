$(function() {
  var VLibrasVideo = (function() {
    function VLibrasVideo() {
      this.$a = $('#viewlet-vlibrasvideo a');
      this.closeTitle = this.$a.attr('data-close-title');
      this.state = this.$a.attr('data-state');
      this.$a.on('click', $.proxy(this.iconClick, this));
      $('body').on('click', '#vlibrasvideo-player .close', $.proxy(this.closeClick, this));
    }
    VLibrasVideo.prototype.iconClick = function(e) {
      e.preventDefault();
      if (this.state === 'ready') {
        this.state = 'playing';
        var html = "<div id='vlibrasvideo-player'>" +
          "<a href='#' class='close' title='" + this.closeTitle + "'>" + this.closeTitle + "</a>" +
          "<iframe width='560' height='315' src='" + (this.$a.attr('href')) + "?autoplay=1' allowfullscreen></iframe>" +
        "</div>";
        $('body').append(html);
      }
    };
    VLibrasVideo.prototype.closeClick = function(e) {
      e.preventDefault();
      if (this.state === 'playing') {
        this.state = 'ready';
        $('#vlibrasvideo-player').remove();
      }
    };
    return VLibrasVideo;
  })();
  return new VLibrasVideo();
});
