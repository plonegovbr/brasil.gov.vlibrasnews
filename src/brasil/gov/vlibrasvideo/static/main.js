$(function() {
  var VLibrasVideo = (function() {
    function VLibrasVideo() {
      this.$a = $('#viewlet-vlibrasvideo a');
      this.state = this.$a.attr('class');
      this.$a.on('click', this, function(e) {
        var self = e.data;
        e.preventDefault();
        if (self.state === 'ready') {
          self.state = 'playing';
          var html = "<div id='vlibrasvideo-player'>" +
            "<iframe width='560' height='315' src='" + (self.$a.attr('href')) + "?autoplay=1' frameborder='0' allowfullscreen></iframe>" +
          "</div>";
          $('body').append(html);
        } else if (self.state === 'playing') {
          self.state = 'ready';
          $('#vlibrasvideo-player').remove();
        }
      });
    }
    return VLibrasVideo;
  })();
  return new VLibrasVideo();
});
