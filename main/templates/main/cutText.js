  $(document).ready(function () {
    $( ".cut-text" ).each(function() {
        if($(this).text().length > maxLength) {
          text = $(this).text();
          firstSpaceIndex = text.substring(maxLength,text.length).indexOf(" ");
          dots = "...";
          if(firstSpaceIndex > -1 && firstSpaceIndex < 15) {
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

    $( ".cut-text-header" ).each(function() {
        if($(this).text().length > maxLengthHeader) {
          text = $(this).text();

          if(text.length - maxLengthHeader <= 5) {
              return;
          }

          firstSpaceIndex = text.substring(maxLengthHeader,text.length).indexOf(" ");
          dots = "...";
          if(firstSpaceIndex > -1 && firstSpaceIndex < 5) {
            if(text[maxLengthHeader+firstSpaceIndex-1] === ".") {
              dots = "..";
            }
            $(this).text($(this).text().substring(0,maxLengthHeader+firstSpaceIndex) + dots);
          }
          else {
            $(this).text($(this).text().substring(0,maxLengthHeader) + dots);
          }
        }
    });
  });
