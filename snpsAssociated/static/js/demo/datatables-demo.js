// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTableGenes').DataTable({
    "order":[[1, "desc"]]
  });
  $('#dataTableRegulation').DataTable({
      "order":[[1,"desc"]]
  });
  $('#dataTableTL').DataTable({
      "order":[[1,"desc"]]
  });
  $('#dataTableSNPs').DataTable({
      "order":[[2,"asc"]]
  });
}); 