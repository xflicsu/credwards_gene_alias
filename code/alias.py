import sys, orangecontrib.bio.gene
from biomart import BiomartServer
from collections import defaultdict

def loadEnsSyn(ensSynFile):
    gene2ens = defaultdict(dict)
    with open(ensSynFile) as f:
        for line in f:
            enst, ensg, gene = line.strip('\n').split('\t')
            gene2ens[gene][ensg] = True
    return gene2ens

if __name__ == '__main__':
    geneFile, ensSynFile, outFile = sys.argv[1:]
    gene2ens = loadEnsSyn(ensSynFile)
    #matching targets are NCBI gene IDs
    #targets = orangecontrib.bio.gene.EnsembleGeneInfo("9606").keys()
    #gm = orangecontrib.bio.gene.GMEnsemble("9606")
    #gm.set_targets(targets)
    server = BiomartServer( "http://www.biomart.org/biomart" )
    d = server.datasets['hsapiens_gene_ensembl']    
    response = d.search({'attributes':['entrezgene',
                                       'ensembl_gene_id',
                                       'external_gene_name',
                                       'ens_hs_gene']},
                        header=1)
    genes = {}
    with open(geneFile) as f:
        for line in f:
            gene = line.strip()
            genes[gene] = True

    for line in response.iter_lines():
        sp = line.split('\t')
        if sp[2] in genes:
            gene2ens[ sp[2] ][ sp[1] ] = True
            print(sp[3])
    with open(outFile, 'w') as fout:
        for gene in gene2ens:
            print >> fout, gene + '\t' + ','.join(gene2ens[gene])

