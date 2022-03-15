document.getElementById('end').addEventListener("load", disable());

function message(id) {
  if (confirm("If this employee is an Instructor for any class at IMO Fitness\n " +
      "this action will also delete ALL classes this employee is associated with." +
      "This action is irreversible, Are you sure you want to proceed with this action?\n \n" +
      "To prevent this behavior click 'cancel' and re-assign a new employee to instruct the related classes. ") === true) {
    document.getElementById(id).value = "True";
  } else {
    document.getElementById(id).value = "False";
  }
  return 0
}


// source - https://www.w3schools.com/howto/howto_js_sort_table.asp


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

function memSearch() {
  // Declare variables
  let input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("mem_search");
  filter = input.value.toUpperCase();
  table = document.getElementById("mem_table");
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

function isActive(whatTable) {
  // Get the checkbox
  var checkBox = document.getElementById("Active");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true) {
    onlyActive(whatTable);
  } else {
    showAll(whatTable);
  }
}

function onlyActive(whatTable) {
  // Declare variables
  var filter, table, tr, td, i, txtValue;
  filter = 'ACTIVE';
  if (whatTable === 'members') {
    table = document.getElementById("mem_table");
  } else {
    table = document.getElementById("emp_table");
  }

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

function showAll(whatTable) {
  // Declare variables
  var table, tr, td, i, txtValue;
  if (whatTable === 'members') {
    table = document.getElementById("mem_table");
  } else {
    table = document.getElementById("emp_table");
  }

  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    tr[i].style.display = "";
  }
}

function disable() {
  var date_input;
  date_input = document.getElementById("end");
  if (date_input.valueAsDate === null || date_input.value === "None") {
    document.getElementById("departments").disabled = false;
  } else {
    document.getElementById("departments").disabled = true;
  }

}

