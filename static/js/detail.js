// $(document).ready(function () {
//   show_comment();
// });

function save_comment(param, isLogin) {
  // console.log(param, isLogin);
  let comment = $("#1").val();
  let nick = isLogin;
  $.ajax({
    type: "POST",
    url: "/commentsave",
    data: {
      comment_give: comment,
      param_give: param,
      nick: nick,
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
