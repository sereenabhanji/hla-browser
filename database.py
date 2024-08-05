#from flask import Flask, jsonify
#from flask_pymongo import PyMongo
#import sys
from pymongo import MongoClient, collection
import csv 
import pprint
import json
import pandas as pd

client = MongoClient()

db = client.hladb

def create_alleles():
    db.alleles.drop()
    db.create_collection('alleles')
    db.alleles.create_index('gene')
    print("Empty Allele collection created")   

def create_genes():
    db.genes.drop()
    db.create_collection('genes')
    print("Empty Genes collection created")

def create_coverage():
    db.coverage.drop()
    db.create_collection('coverage')
    db.coverage.create_index('pos')  # so we can easily query based on gene position 
    print("Empty sequencing coverage collection created")

def load_alleles(freqency_file): 
    '''
    load in frequency file with 3 columns: HLA allele name, total count, frequency
    insert each row to the DB as a document representing allele variant and its info
    '''
    n = 0
    with open(freqency_file, 'rt') as file:
        reader = csv.reader(file)
        for line in reader:
                gene = line[0].split("*")[0]
                allele = {'allele_id': line[0], 'count': line[1], 'total':line[2], 'cag_frequency':float(f'{float(line[3]):.{3}g}'), 'tapas_frequency': line[4], 'gene': gene}
                db.alleles.insert_one(allele)
                print(f"Allele {line[0]} inserted into DB")
                n += 1

    print(f"{n} alleles added to gene DB")

def get_gene_info(name):  # takes in HLA gene (such as A or B), returns all alleles of the gene
    result = db.alleles.find({"gene": name})
    for entry in result:
        entry.pop('_id')
        pprint.pprint(entry)
        print(",")

def get_all_alleles():  # get all allele variants of all HLA genes 
     result = db.alleles.find()
     for entry in result:
          entry.pop('_id')
          pprint.pprint(entry)
          print(',')

def load_genes():
    '''
     currently im going to mannually create a CSV with all 8 HLA genes
     and in this function I will add to gene collection
    '''
    file = '/Users/sereenabhanji/Downloads/hla-exons.txt'
    df = pd.read_csv(file)

    mhc = {'name': "all", 'txstart': 29942531, 'txend': 33089696}
    gene_regs = []
    for i in range(len(df.index)):
        gene = {}
        gene['name'] = df.loc[i]["gene"]
        gene['txstart'] = int(df.loc[i]["txStart"])
        # print(gene['txstart'])
        gene['txend'] = int(df.loc[i]["txEnd"])        

        gene_regs.append([int(df.loc[i]["txStart"]), int(df.loc[i]["txEnd"])])
        starts = df.loc[i]["exonStarts"].split(',')
        ends = df.loc[i]["exonEnds"].split(',')
        count = df.loc[i]["exonCount"]

        exons = []

        for j in range(count):
            start = int(starts[j])
            end = int(ends[j])
            exons.append([start, end])

        gene['regions'] = exons
        db.genes.insert_one(gene)
        print(gene)
        print(f"Gene {gene['name']} inserted into db")
    
    mhc['regions'] = gene_regs
    db.genes.insert_one(mhc)
    print(mhc)
    print("MHC region inserted into DB")

def load_depth(file):
    n = 0
    with open(file, 'rt') as file:
        reader = csv.reader(file, delimiter="\t")
        for line in reader:
            coord = {'pos': int(line[0]), 'cov': float(line[1]) }
            db.coverage.insert_one(coord)
            n += 1
    
    print(f"{n} sequencing coordinates inserted into the database")

def load_pharm_data(file):
    with open(file, 'rt') as file:
        reader = csv.reader(file)
        for line in reader:
            db.alleles.update_many({"allele_id": line[0]},{"$set":{"clinical_ann":line[2], "guideline_ann":line[3], "label_ann":line[4], "multilink_ann": line[5], "variant_ann": line[6], "vip_gene": line[7]}})
            print(line)

def add_ancestry(file):
    with open(file, 'rt') as file: 
        reader = csv.reader(file)
        for line in reader:
            entry = f"FC: {line[6]}, MA: {line[7]}, HT: {line[8]}"
            db.alleles.update_one({"allele_id": line[0]}, {"$set": {"freq_by_ancestry": entry }})
            print(line)

def add_pharm(file):
    #db.pharm.drop()
    #db.create_collection('pharm')
    #db.alleles.create_index('Allele ID')
    #print("Empty Pharm collection created")
    df = pd.read_csv(file)
    df = df.fillna(0)
    #print()
    db.pharm.insert_many(df.to_dict('records'))


if __name__ == '__main__':
    #file = '/Users/sereenabhanji/Downloads/allele_frequencies_final_not.csv'
    #create_alleles()
    #load_alleles(file)
    # get_gene_info("A")
    # get_all_alleles()
    #create_genes()
    #load_genes()
    #create_coverage()
    #load_depth('/Users/sereenabhanji/Downloads/HLA-computed-depths.csv')
    #load_pharm_data('/Users/sereenabhanji/Downloads/all_annotations.csv')
    #add_ancestry('/Users/sereenabhanji/Downloads/freqs_by_ancestry.csv')
    add_pharm('/Users/sereenabhanji/Downloads/clinical_anns_all.csv')