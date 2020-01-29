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
    }

});

$("body").on("click", ".tag", function(){
  console.log($(this).text());
  tags.splice(tags.indexOf($(this).text()),1);
  $(this).remove();
  numOfTags--;
 });
