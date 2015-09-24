DATA = '../data/'
WORK = '../work/'

data = {'human':(DATA + 'HumanErythroidStagesDataset.csv',),
        'mouse':(DATA + 'MouseErythroidStagesDataset.csv',
                 DATA + 'MouseMEP-MK-ErythDataset.csv')}

rule getGenes:
    input: DATA + 'HumanErythroidStagesDataset.csv',
           DATA + 'MouseErythroidStagesDataset.csv',
           DATA + 'MouseMEP-MK-ErythDataset.csv'
    output: ens = WORK + 'geneLs/{species}.ens',
            gene = WORK + 'geneLs/{species}.gene'
    run: 
        files = data[wildcards.species]
        shell('cat {files} | grep -v Intron | grep -v Ensembl | cut -f 1 -d "," > {output.gene}.pre')
        shell('cat {files} | grep -v Intron | grep -v Ensembl | cut -f 3 -d "," >> {output.gene}.pre')
        shell("""cat {output.gene}.pre | sed -e 's/\x0d//g' | sed '/^\s*$/d' | sort -u > {output.gene}""")
        shell("""cat {files} | grep -v Intron | grep -v Ensembl | cut -f 2 -d "," | sed -e 's/\x0d//g' | sed '/^\s*$/d' | sort -u > {output.ens}""")
        shell('rm {output.gene}.pre')

rule all:
    input: expand(WORK + 'geneLs/{species}.{gset}', \
                  species = ('human', 'mouse'), \
                  gset = ('ens', 'gene'))
