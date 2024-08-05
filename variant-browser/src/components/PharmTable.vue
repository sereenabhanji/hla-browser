<template>
    <div class="child-component">
      <h6 style="font-weight: bold; color: #004aad;"> {{ annType }} Annotations </h6>
      <div ref="table" class="table-sm"></div>
    </div>
  </template>
    
    <script>
    import axios from 'axios';
    import { TabulatorFull as Tabulator } from 'tabulator-tables';
    import 'bootstrap/dist/css/bootstrap.css';//HX
    import 'bootstrap/dist/js/bootstrap.js';//HX
    import '@/assets/css/tabulator-style.css'
  
  
    export default {
      name: 'PharmTable',
      filters: [],
      data() {
        return {
          tabulator: null,
          empty: true,
        };
      }, 
      props: {
        variant: String,
        annType: String,
      },
  
      mounted: function () {
        this.popTable();
      },
      methods: {
          popTable() {
              this.tabulator = new Tabulator(this.$refs.table, {
                  ajaxURL:`http://127.0.0.1:5000/annotations/${this.annType}/${this.variant}`,
                  ajaxConfig: "GET",
                  ajaxContentType:"json",
                  layout: "fitDataFill",
                  //autoColumns:true, // needed this for data to be displayed
                  columns: this.setColumns(),
                  //rowHeight:10,
                  //height: "200px"
                  placeholder: "No " + this.annType + " annotations for this variant"
              });
              this.tabulator.on("dataLoaded", function(data) {
                console.log(data.length)
                this.empty = data.length == 0
                console.log(this.empty)
                
              })
             
          },
          setColumns() {
            if (this.annType == "Clinical") {
              return [{title: "Variant/Haplotypes", field: "Variant/Haplotypes"},
                      {title: "Level of Evidence", field: "Level of Evidence"},
                      {title: "Score", field:"Score"},
                      {title: "Phenotype Category", field: "Phenotype Category"},
                      {title: "PMID Count", field: "PMID Count"},
                      {title: "Evidence Count", field: "Evidence Count"},
                      {title: "Drug(s)", field: "Drug(s)"},
                      {title: "Phenotype(s)", field: "Phenotype(s)"},]
            }
            if (this.annType == "Variant") {
              return [{title: "Variant/Haplotypes", field: "Variant/Haplotypes"},
                      {title: "Drug(s)", field: "Drug(s)"},
                      {title: "Score", field:"Score"},
                      {title: "Phenotype Category", field: "Phenotype Category"},
                      {title: "Phenotype", field: "Sentence"},
                      {title: "Pediatric", field: "Specialty Population", formatter: this.isPed},
                      {title: "PMID", field: "PMID", formatter: this.pmid},
                    ]

            }
          },
          pmid: function(cell, formatter) {
            var id = cell.getValue();
            var url = `https://pubmed.ncbi.nlm.nih.gov/${id}/`
            return "<a href="+url+" target=\"_blank\">"+id+"</a>";
          },
          isPed: function(cell, formatter) {
            if (cell.getValue() == "pediatric") {
              return "Yes"
            }
            else {
              return "No"
            }
          }
      },
      
    };
    </script>
  
 <style scoped>
 .child-component {
  padding-top: 1rem;
 }
.table-sm {
  padding-bottom: 2rem;
}
</style>