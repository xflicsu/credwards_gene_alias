import sys, orangecontrib.bio.gene

if __name__ == '__main__':
    geneFile, outFile = sys.argv[1:]
    #matching targets are NCBI gene IDs
    targets = orangecontrib.bio.gene.EnsembleGeneInfo("9606").keys()
    print('here')
    gm = orangecontrib.bio.gene.GMEnsemble("9606")
    gm.set_targets(targets)

    with open(geneFile) as f:
        with open(outFile, 'w') as fout:
            for line in f:
                gene = line.strip()
                if gene:
                    print >> fout, gene + '\t' + str(gm.umatch(gene))
        
