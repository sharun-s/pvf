partyangle={'INC(I)':90, 'JNP':355, 'INC':85, 'TDP':0, 
            'BLD':5,'JP':10, 'ICSP':300,
            'IND':270, 'CPI':180, 'BJP':325, 'MIM':260, 'CPI(ML)':190, 'TRS':270,
            'DMM': 280, 'BSP': 250, 'SP':290, 'PPOI':240, 
            #1999 onwards
            'ATDP':300, 'NTRTDP(LP)':310, 'MCPI(S)':190, 'CPM':200,
            'BJRP':320, 'CPI(ML)(L)':210, 
            'TPPP':220, 'PRAP':230, 'JSP':230, 'BHSASP':330, 'LSP':340, 'RDHP':345, 'PP':325, 
            'RPS':305, 'NOTA':0, 'JASPA':315, 'YSRCP':135, 
            'AAAP':355, 'STR':205, 'AIMIM':260, 'BCUF':215, 
            'SUCI':225, 'WPOI':295, 'MASP':270, 'JaSPa':315, 'PSHP':316, 'JSRP':317, 'AIFB':318, 'IUML':319, 'NSP':321, 'VCK':322, 'RDP':323, 'VJP':324}
# increasing the highest value will change all other colors
# look at matplotlib.org colormap references for different colormaps
partycolor={'INC(I)': 0, 'INC':2, 'JNP':6.5, 'TDP':6, 
            'BLD':7,'JP':7, 'ICSP':11,
            'IND': 11, 'CPI': 5, 'BJP':6.5, 'MIM':3, 'CPI(ML)':5, 'TRS':11,
            'DMM':11, 'BSP':4,'SP':11, 'PPOI':11, 
            'ATDP':11, 'NTRTDP(LP)':10, 'MCPI(S)':5, 'CPM':5,
            'BJRP':11, 'CPI(ML)(L)':5,
            'TPPP':11, 'PRAP':11, 'JSP':11, 'BHSASP':11, 'LSP':11, 'RDHP':11, 'PP':11, 
            'RPS':11, 'NOTA':1, 'JASPA':11, 'YSRCP':1, 
            'AAAP':11, 'STR':11, 'AIMIM':3, 'BCUF':11, 
            'SUCI':11, 'WPOI':11, 'MASP':11, 'JaSPa':11, 'PSHP':11, 'JSRP':11, 'AIFB':11, 'IUML':11, 'NSP':11, 'VCK':11,'RDP':11,'VJP':11}

# currently using hardcoded data until datafiles include 
# electiontype col - MP, MLA, ZLTC, MLTC, Panchayat, Ward
electiontype={'Anantapur':'MP', 
                  'Uravakonda':'MLA',
                  'Guntakal':'MLA',
                  'Tadipatri':'MLA',
                  'Rayadurg':'MLA', 
                  'Anantapur Urban':'MLA', 
                  'Singanamala':'MLA',
                  'Kalyandurg':'MLA'}

import pandas as pd
#debugging helper fns
#get rows with exact keyword in col
g=lambda df,col,keyword:df[x.col == keyword]
#get rows containing keyword in col
gco=lambda df,col,keyword:df[df.col.str.contains(keyword)]


mv = pd.read_csv("data/mandal_spelling_variants.txt", 
      names=['variant','standard'], index_col=0 )
def getSpellingVariants(mandal):
      if mandal in mv.index:
            tmp = mv.loc[mandal]
            if tmp.size ==1: 
                  return [tmp.standard]
            else:
                  return tmp.standard.values # return all variants
      else:
            return None 