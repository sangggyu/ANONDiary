function show_popup_create() {
  window.open("/create_page", "a", "width=1000, height=800, left=100, top=50");
}

$(document).ready(function () {
  show_content();
});

function show_content() {
  $("#total_diary").empty();
  $.ajax({
    type: "GET",
    url: "/diary",
    data: {},
    success: function (response) {
      // console.log(response);
      let rows = response["list"];
      for (let i = 0; i < rows.length; i++) {
        let num = rows[i]["diaryid"];
        let title = rows[i]["title"];
        let view = rows[i]["view"];
        let createtime = gettimestamp(rows[i]["createtime"]);
        // let createtime = rows[i]["createtime"];
        let nickname = rows[i]["nick"];
        let content = rows[i]["content"];
        let temp_html = `<tr>
                          <th scope="row">${num}</th>
                          <td><a href="/detail/${num}">${title}</a></td>
                          <td>${nickname}</td>
                          <td>${createtime}</td>
                          <td>${view}</td>
                        </tr>`;
        $(".total_diary").append(temp_html);
      }
    },
  });
}

function gettimestamp(createtime) {
  //console.log(createtime)
  createtime = createtime.substr(0, 19).replace("T", " ");
  var startDate = new Date(createtime);
  var endDate = new Date(); // 현재시각
  var seconds = (endDate.getTime() - startDate.getTime()) / 1000; // 두 데이타 갭

  if (seconds > 3600 * 24) {
    // 24시간 보다 작으면
    return createtime;
  } else {
    return createtime.substr(11, 19);
    //return new Date(seconds * 1000).toISOString().slice(11, 19);
  }
}
