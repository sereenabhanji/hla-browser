<template>
    <div class="svg-container">
        <svg ref="allele" class="allele-vis">
        </svg>
    </div>
    
</template>

<script>
import * as d3 from "d3";
import axios from "axios";

export default{
    name: "AlleleVisual",
    data: function() {
        return {
            margin: {top: 20, right: 10, bottom: 20, left: 12},
        }
    },
    
    props: {
        gene: {
            type: String,
        },
 
    },
    watch: {
        gene: function() {
            this.getData();
        }

    },
    mounted: function() {
        //this.initializaSvg();
        //this.highlightExons();
        this.getData();
        

    },

    methods: {
        initializaSvg() {
            d3.selectAll("svg > *").remove()
            this.width = 500 - this.margin.left - this.margin.right;
            this.height = 100 - this.margin.top - this.margin.bottom;

            console.log(this.start)
            this.length = this.stop - this.start;
            this.scale = d3.scaleLinear()
                .domain([this.start, this.stop])
                .range([0, this.width])
            this.svg = d3.select(this.$refs.allele)
                .attr("viewBox", `0 0 500 30`)
                .append("g")
                //.attr("width", this.width + this.margin.left + this.margin.right )
                //.attr("height", this.height + this.margin.top + this.margin.bottom)
                .attr("transform", "translate(" + this.margin.left + "," + this.margin.bottom + ")");
            
            this.svg.append("line")
                .attr("x1", 0) 
                .attr("x2", this.scale(this.stop))
                .attr("y1", 5)
                .attr("y2", 5)
                .style("stroke", "#000000")
                .style("stroke-width", 2);
                      
        },
    
        getData() {
            try {
                axios
                .get(`http://127.0.0.1:5000/genes/${this.gene}`)
                .then(response => {
                    for (const d of response.data) {
                        console.log(d)
                        this.start = d.txstart 
                        this.stop = d.txend
                        this.regions = d.regions
                    }
                    this.initializaSvg();
                    this.highlightExons();
                })
            }
            catch (error) {
                console.error('errror')
            }
        },
        
        
        highlightExons() {
            for (const reg of this.regions) {
                this.svg.append("rect")
                    .attr("x", this.scale(reg[0]))
                    .attr("y", 0)
                    .attr("width", this.scale(reg[1])-this.scale(reg[0]))  // literally screaming because this linear scale is not linear ...
                    .attr("height", 10)
                    .style("fill", "#004aad")
                    .append("div")
                    .style("position", "absolute")
                    .style("visibility", "hidden")
                    .text("tooltip")
                        .on("mouseover", function(){console.log(this.tooltip);return this.tooltip.style("visibility", "visible");})
                        .on("mousemove", function(){return this.tooltip.style("top", d3.select(this).attr("y")+"px").style("left",(d3.select(this).attr("x"))+"px");})
                        .on("mouseout", function(){return this.tooltip.style("visibility", "hidden");});
                                            
                 
                
            }
        },
        mouseover: (event, d) => {
            console.log("mouseover")
            d3.select("div").style("visibility", "visible");
        },

        mouseleave: (event, d) =>  {
            this.tooltip.style('opacity', 0);
        },

        mousemove: (event, d) => {
            const text = d3.select('.tooltip-area__text');
            text.text("hello");
            const [x, y] = d3.pointer(event);

            this.tooltip
            .attr('transform', `translate(${x}, ${y})`);
        }

}
    
}

</script>

<style scoped>
.svg-container {
    display: inline-block;
    position: relative;
    width: 100%;
    vertical-align: top;
    overflow: hidden;
}
.svg-content {
    display: inline-block;
    position: absolute;
    top: 0;
    left: 0;
}
</style>