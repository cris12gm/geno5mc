// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    "order":[[1, "desc"]]
  });
  $('#dataTable1').DataTable();
  $('#dataTable2').DataTable(
    {
      "order":[[1,"desc"]]
    }
  );
});