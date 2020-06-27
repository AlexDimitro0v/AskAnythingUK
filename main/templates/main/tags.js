  $('#max_tags_message').text("You can provide a maximum of " + maxTags + " tags.");
  // When enter is pressed, new tag is added
  $('#tag-input').keypress(function (e) {
      if (e.which == 13 ) {
        let tagValue = $('#tag-input').val().trim();
        if(tagValue != "" && numOfTags < maxTags && !tags.includes(tagValue)) {
          numOfTags++;
          tags.push(tagValue);
          $('#tag-input').val('');
          $('#tags').append("<span class='tag' id='tagtag' style='line-height: 50px; white-space: nowrap'>"+tagValue+"</span>");
          $('#tags').append(" ");
        }
        else if(numOfTags >= maxTags) {
          if( $("#overlay_error_tags").css('display') == 'block') {
            $('#okay_tags').click();
          }
          else {
            $('#overlay_error_tags').css("display","block");
            $('body').css("overflow","hidden");
          }
        }
      }

  });

  $("body").on("click", ".tag", function(){
    tags.splice(tags.indexOf($(this).text()),1);
    $(this).remove();
    numOfTags--;
   });

  $('#okay_tags').click(function(e) {
    $('#overlay_error_tags').css("display","none");
    $('body').css("overflow","visible");
  });
