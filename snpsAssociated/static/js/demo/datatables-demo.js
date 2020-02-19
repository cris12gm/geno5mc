// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTablePromoters').DataTable({
    "order":[[1, "desc"]]
  });
  $('#dataTablePromotersLite').DataTable({
    "pageLength" : 6,
    "order":[[3, "desc"]],
    "searching": false,
    "bLengthChange":false
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
  $('#dataTableGenesMQ').DataTable({
    "order":[[3,"asc"]]
  });
  $('#dataTableTLMQ').DataTable({
    "order":[[2,"desc"]]
  });
  $('#dataTableRegulationMQ').DataTable({
    "order":[[2,"desc"]]
  });
  $('#dataTableSamples').DataTable({
    "order":[[3,"desc"]]
  });
  $('#dataTableTopResults').DataTable({
    "order":[[5,"desc"]]
  });
}); 