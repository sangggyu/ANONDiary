// $(document).ready(function () {
//   show_comment();
// });

function save_comment(param) {
  console.log(param);
  let comment = $("#1").val();
  $.ajax({
    type: "POST",
    url: "/commentsave",
    data: {
      comment_give: comment,
      param_give: param,
    },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}

// 삭제
function delete_comment(num) {
  $.ajax({
    type: "POST",
    url: "/comment/delete",
    data: {
      deletenum_give: num,
    },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}
