function table_search() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("search_box");
  filter = input.value;
  table = document.getElementById("sort_table_id");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}