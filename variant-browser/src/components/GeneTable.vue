<template>
    <div class="child-component">
       <div ref="table" class="table-sm"></div>
    </div>
  </template>
    
    <script>
    import axios from 'axios';
    import { TabulatorFull as Tabulator } from 'tabulator-tables';
    //import '@/assets/css/tabulator-style.css'

  
    export default {
      name: 'Table',
      emits: ["hover"],
      props: {
        view: {
          type: String,
          default: "all"
        }
      },
      data() {
        return {
          tabulator: null,
          filter: null,
        };
      }, 
      mounted: function () {
        this.popTable();
      },
      watch: {
        view: function(newView, oldView) {
          //console.log(newView)
          if (newView != "all") {
            this.filter = [{field: "allele_id", type: "starts", value: newView}]
          }
          else {
            this.filter = []
          }
          this.updateFilter()
          console.log(this.filter)
        }
        
      },
      methods: {
          popTable() {
              this.tabulator = new Tabulator(this.$refs.table, {
                  ajaxURL:"http://127.0.0.1:5000/",
                  ajaxConfig: "GET",
                  ajaxContentType:"json",
                  layout: "fitDataFill",
                  // autoColumns:true, // needed this for data to be displayed
                  columns: [ // override autocolumn setting column defs to field names
                    {title: "Allele Name", field: "allele_id", formatter: this.link},
                    {title: "Count", field:"count", headerSortStartingDir:"desc"},
                    {title: "Total", field: "total", headerSortStartingDir:"desc"},
                    {title: "Frequency in CaG", field: "cag_frequency", headerSortStartingDir:"desc"},
                    {title: "Frequency in TAPAS", field: "tapas_frequency", headerSortStartingDir:"desc"},
                    {title: "Frequency per Ancestry", field: "freq_by_ancestry", headerSortStartingDir:"desc"},
                    {title: "No. Clinical Annotations", field: "clinical_ann", headerSortStartingDir:"desc"},
                    {title: "No. Variant Annotations", field: "variant_ann", headerSortStartingDir:"desc"},
                    {title: "No. Drug Label Annotations", field: "label_ann", headerSortStartingDir:"desc"}
                  ],
                  //rowHeight: 40,
                  height: "400px",                  
              });
              //this.tabulator.on("rowMouseOver", this.hover) ;
              //this.tabulator.value.scrollToColumn(col.field);
              
          },
          
          hover: function (e, row) {
            //console.log("hello" + row.getData().name)
            this.$emit("hover", row.getData().name)
          },
          link: function(cell, formatter) {
            var url = cell.getValue();
            //return `<router-link :to="{ name: 'Gene', params: { gene: '${url}'} }">${url}</router-link>`;
            return "<a href="+url+">"+url+"</a>"; // this works but trying to use router link
          },
          updateFilter: function() {
            this.tabulator.setFilter(this.filter)
            //console.log(this.filterArr)
          }
      },
    };
    </script>
  
<style scoped>
.table-sm {
  padding-bottom: 4rem;
}

</style>