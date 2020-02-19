// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTablePromoters').DataTable({
    "order":[[1, "desc"]]
  });
  $('#dataTablePromotersLite').removeAttr('width').DataTable({
    "pageLength" : 6,
    "order":[[1, "desc"]],
    "searching": false,
    "bLengthChange":false,
    "autoWidth": false,
    "columnDefs": [
      { "width": "10%", "targets": 1 }
    ]
  });
  $('#dataTableEnhancersLite').removeAttr('width').DataTable({
    "pageLength" : 6,
    "order":[[1, "desc"]],
    "searching": false,
    "bLengthChange":false,
    "autoWidth": false,
    "columnDefs": [
      { "width": "10%", "targets": 1 }
    ]
  });
  $('#dataTableTLightsLite').removeAttr('width').DataTable({
    "pageLength" : 6,
    "order":[[1, "desc"]],
    "searching": false,
    "bLengthChange":false,
    "autoWidth": false,
    "columnDefs": [
      { "width": "10%", "targets": 1 }
    ]
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