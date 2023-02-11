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
        let num = rows[i]["num"];
        let title = rows[i]["title"];
        let content = rows[i]["content"];
        let temp_html = `<tr>
                          <th scope="row">${num}</th>
                          <td><a href="/detail/${num}">${title}</a></td>
                          <td>Otto</td>
                          <td>@mdo</td>
                          <td>@mdo</td>
                        </tr>`;
        $(".total_diary").append(temp_html);
      }
    },
  });
}
