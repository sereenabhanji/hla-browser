<template>
   
    <div class="child-component">
        <svg ref="gene" class="gene-vis">
            <g ref="geneDrawing"></g>
        </svg>
    </div>
    
    
</template>

<script>
import * as d3 from "d3";
import axios from "axios";

export default{
    name: "GeneVisual",
    
    data: function() {
        return {
            start: 29900000,  // currently im passing start and stop positions
            stop: 33180577,
            length: null,
            chromData: null,
            hoveredPos: "null",
            loading: true
        }
        
    },  
    props: {
        hoveredGene: {
            type: String,
            default: null
        },
    },        
    watch: {
        hoveredGene (newPos, oldPos) {
            console.log(newPos)
            if (newPos != null) {
                this.svg.select("#"+newPos)
                    .attr("fill", "#FC0FC0")
                    .attr("visibility", "visible")
                    .style("shape-rendering", "crispEdges")
                    .raise(); // brings rectangle forward 
                    
            }
        }
    },
  
    mounted: function() {
        this.length = this.stop - this.start;
        // console.log(this.length)
        this.scale = d3.scaleLinear()
            .domain([this.start, this.stop])
            .range([0, 500])
        this.svg = d3.select(this.$refs.gene)
            .attr("width", 500)
            .attr("height", 50)
            //.attr("x", 50)
        this.svg.append("line")
            .attr("x1", 0) 
            .attr("x2", this.scale(this.stop))
            .attr("y1", 20)
            .attr("y2", 20)
            .style("stroke", "#000000")
            .style("stroke-width", 2);
        this.highlight = this.svg.append("rect")
            .attr("x", 0)
            .attr("y", 20)
            .attr("width", 0)
            .attr("height", 10)
            .style("fill", "#FC0FC0")
            .attr("visibility", "hidden")
        
        this.drawing = d3.select(this.$refs.geneDrawing);
        this.getData();
       

        // let data = JSON.parse(JSON.stringify(this.chromData))
        // this.addTranscriptRects()
        // this.drawing = d3.select(this.$refs.drawing)
        
        // this.showGenes()
        

    },

    methods: {
        async getData() {
            const response = await axios.get('http://127.0.0.1:5000/genes/all')
                
            let geneData = response.data;
            this.chromData = new Array(8);
            geneData.forEach(g => {
                if (g.name == this.hoveredGene) {
                    console.log("hovered")
                }
                //console.log(g)
                this.chromData.push(g)
                this.svg.append("rect")
                .attr("x", this.scale(g.txstart))
                .attr("y", 15)
                .attr("width", this.scale(g.txend) - this.scale(g.txstart))
                .attr("height", 10)
                .attr("id", g.name)
                .style("fill", "#00ff00")
                .style("shape-rendering", "crispEdges");

            });
            this.loading = false
                
        },
        addTranscriptRects: function() {
            console.log(this.chromData)
            for (const gene in this.chromData) {
                console.log("hello")
                this.gene_lengths.push(this.chromData[gene]["txend"]-this.chromData[gene]["txstart"])

                
            }
            
        }

}
    
}

</script>