// Call the dataTables jQuery plugin
$(document).ready(function() {
  // QuerySNP
  $('#dataTablePromoters').DataTable({
    "order":[[5, "desc"]]
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
      "order":[[5,"desc"]]
  });
  $('#dataTableTL').DataTable({
      "order":[[1,"desc"]]
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
  $('#dataTableTopResults_Promoter').DataTable({
    "order":[[5,"desc"]]
  });
  $('#dataTableTopResults_Enhancer').DataTable({
    "order":[[5,"desc"]]
  });
  // QueryGene
  $('#dataTableSNPsTopResults').DataTable({
    "order":[[2,"desc"]]
  });
  $('#dataTableSNPsPromoter').DataTable({
    "order":[[1,"desc"]]
  });
  $('#dataTableSNPsEnhancer').DataTable({
    "order":[[1,"desc"]]
  });
  $('#dataTableSNPsTLights').DataTable({
    "order":[[1,"desc"]]
  });
  // QueryTrait
  $('#dataTableQueryTrait').DataTable({});
}); 