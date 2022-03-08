
// source - https://www.w3schools.com/howto/howto_js_filter_table.asp


function empSearch() {
  // Declare variables
  let input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("emp_search");
  filter = input.value.toUpperCase();
  table = document.getElementById("emp_table");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

// source https://www.w3schools.com/howto/howto_js_display_checkbox_text.asp

function isActive() {
  // Get the checkbox
  var checkBox = document.getElementById("Active");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true) {
    onlyActive();
  } else {
    all();
  }
}

function onlyActive() {
  // Declare variables
  var filter, table, tr, td, i, txtValue;
  filter = 'ACTIVE';
  table = document.getElementById("emp_table");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[3];
    if (td) {
      txtValue = td.textContent;
      if (txtValue === filter) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function all() {
  // Declare variables
  var table, tr, td, i, txtValue;
  table = document.getElementById("emp_table");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[3];
    if (td) {
      txtValue = td.textContent;
      if (txtValue) {
        tr[i].style.display = "";
      }
    }
  }
}