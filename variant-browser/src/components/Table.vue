<template>
  <div class="child-component">
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
    name: 'Table',
    filters: [],
    data() {
      return {
        tabulator: null,
      };
    }, 
    props: {
      gene: String,
    },

    mounted: function () {
      this.popTable();
    },
    methods: {
        popTable() {
            this.tabulator = new Tabulator(this.$refs.table, {
                ajaxURL:`http://127.0.0.1:5000/alleles/${this.gene}`,
                ajaxConfig: "GET",
                ajaxContentType:"json",
                layout: "fitColumns",
                autoColumns:true, // needed this for data to be displayed
                autoColumnsDefinitions: [ // override autocolumn setting column defs to field names
                    {title: "Allele ID", field: "allele_id"},
                    {title: "Count", field: "count"},
                    {title: "Frequency", field:"frequency"},
                    {title: "Gene", field: "gene"}
                ],
                //rowHeight:10,
                height: "600px"
            });
           
        },
       
    },
  };
  </script>

