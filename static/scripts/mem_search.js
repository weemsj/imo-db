function mem_search() {
  // Declare variables
  let input, filter, table, tblr, tbld, i, txtValue;
  input = document.getElementById("mem_search");
  filter = input.value.toUpperCase();
  table = document.getElementById("mem_table");
  tblr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tblr.length; i++) {
    tbld = tblr[i].getElementsByTagName("td")[2];
    if (tbld) {
      txtValue = tbld.textContent || tbld.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tblr[i].style.display = "";
      } else {
        tblr[i].style.display = "none";
      }
    }
  }
}