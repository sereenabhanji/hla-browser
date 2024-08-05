from flask import Flask, jsonify, request, send_file
from flask_pymongo import PyMongo
from flask_cors import CORS
import pymongo

app = Flask(__name__ )
CORS(app)

app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/hladb"
mongo = PyMongo(app, "mongodb://127.0.0.1:27017/hladb")  # accessing my DB

@app.route('/', methods=['GET'])  # gets all alleles of all genes
def get_all_alleles():
    alleles = mongo.db.alleles.find()
    data = []
    for a in alleles:
        a.pop('_id')
        data.append(a)
    return jsonify(data)

@app.route('/alleles/<name>', methods=['GET'])  # get all alleles of gene input
def get_gene(name):
    alleles = mongo.db.alleles.find({"gene": name}, {"gene": 0, "_id": 0})
    data = []
    for a in alleles:
        data.append(a)
    return jsonify(data)

@app.route('/matches/<substring>', methods=['GET'])  # get all alleles which contain the substring
def query_from_substr(substring):
    try:
        q = substring.split('*')
        query = q[0] + '[*]' + q[1]
    except:
        query = substring

    result = mongo.db.alleles.find({"allele_id": {"$regex": query}})
    data = []
    for r in result:
        r.pop('_id')
        data.append(r)
    return jsonify(data)

@app.route('/genes/regions')  # get all regions of all genes
def get_gene_regions():
    regions = mongo.db.genes.find({}, {"name":1, "txstart": 1, "txend": 1, "_id":0})
    reg = []
    for region in regions:
        reg.append(region)
    return jsonify(reg)

@app.route('/genes/<name>', methods=['GET'])
def get_exons(name):
    exons = mongo.db.genes.find({"name": name}, {"_id": 0})
    data = []
    for e in exons:
        data.append(e)
    return jsonify(data)

@app.route('/depths/<name>', methods=['GET'])
def get_depth(name):
    points = mongo.db.genes.find({"name": name}, {"_id": 0})
    for p in points:
        start = p.pop("txstart")
        end = p.pop("txend")

    coords = mongo.db.coverage.find({"pos": {"$gte": start, "$lte": end}})
    data = []
    for c in coords:
        c.pop("_id")
        data.append(c)

    # this probably could be written more efficiently ....
    get_min_cov = mongo.db.coverage.find({"pos": {"$gte": start, "$lte": end}}).sort({"cov":1}).limit(1) 
    get_max_cov = mongo.db.coverage.find({"pos": {"$gte": start, "$lte": end}}).sort({"cov":-1}).limit(1) 
    
    res = {}
    res["txstart"] = start
    res["txend"] = end

    for min in get_min_cov:
        min.pop("_id")
        min.pop("pos")
        res["min"] = min

    for max in get_max_cov:
        max.pop("_id")
        max.pop("pos")
        res["max"] = max

    res["points"] = data
    

    return jsonify(res)

@app.route('/annotations/<type>/<gene>')
def get_annotations(type, gene):
    anns = mongo.db.pharm.find({"Annotation Type": type, "Allele ID": gene}, {})
    data = []
    for a in anns:
        a.pop("_id")
        data.append(a)
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True, port=8000)