  $(document).ready(function () {
    $( ".cut-text" ).each(function() {
        if($(this).text().length > maxLength) {
          text = $(this).text();
          firstSpaceIndex = text.substring(maxLength,text.length).indexOf(" ");
          dots = "...";
          if(firstSpaceIndex>-1) {
            if(text[maxLength+firstSpaceIndex-1] === ".") {
              dots = "..";
            }
            $(this).text($(this).text().substring(0,maxLength+firstSpaceIndex) + dots);
          }
          else {
            $(this).text($(this).text().substring(0,maxLength) + dots);
          }
        }
    });
  });
