$(function() {
  var VLibrasNews = (function() {
    function VLibrasNews() {
      this.$a = $('#viewlet-vlibrasnews a');
      this.closeTitle = this.$a.attr('data-close-title');
      this.state = this.$a.attr('data-state');
      this.$a.on('click', $.proxy(this.iconClick, this));
      $('body').on('click', '#vlibrasnews-player .close', $.proxy(this.closeClick, this));
    }
    VLibrasNews.prototype.iconClick = function(e) {
      e.preventDefault();
      if (this.state === 'ready') {
        this.state = 'playing';
        var html = "<div id='vlibrasnews-player'>" +
          "<a href='#' class='close' title='" + this.closeTitle + "'>" + this.closeTitle + "</a>" +
          "<iframe width='560' height='315' src='" + (this.$a.attr('href')) + "?autoplay=1' allowfullscreen></iframe>" +
        "</div>";
        $('body').append(html);
      }
    };
    VLibrasNews.prototype.closeClick = function(e) {
      e.preventDefault();
      if (this.state === 'playing') {
        this.state = 'ready';
        $('#vlibrasnews-player').remove();
      }
    };
    return VLibrasNews;
  })();
  return new VLibrasNews();
});
