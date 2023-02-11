



function diary_modify_open(num) {
  $("#total_diary").empty();
  $.ajax({
    type: "GET",
    url: "/diary/modify_open",
    data: {'num_give':num},
    success: function (response) {
        let low = response['']
    },
  });
}