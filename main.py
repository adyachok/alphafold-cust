from pathlib import Path

import py3Dmol
import requests
from alpha_viewer import alpha_viewer


alphafold_ID = 'AF-P14618-F1'
database_version = 'v3'

model_url = f'https://alphafold.ebi.ac.uk/files/{alphafold_ID}-model_{database_version}.pdb'
model_cif = f'https://alphafold.ebi.ac.uk/files/{alphafold_ID}-model_{database_version}.cif'
error_url = f'https://alphafold.ebi.ac.uk/files/{alphafold_ID}-predicted_aligned_error_{database_version}.json'


def download_file(url):
    # NOTE the stream=True parameter below
    model_data_dir = Path(alphafold_ID)
    if not model_data_dir.exists():
        model_data_dir.mkdir()
    local_filename = model_data_dir.joinpath(url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    return local_filename


# download_file(model_url)
# download_file(model_cif)
# download_file(error_url)

def show_pdb(pdb_file, rank_num=1, show_sidechains=False, show_mainchains=False, color="lDDT"):
  model_name = f"rank_{rank_num}"
  view = py3Dmol.view(js='https://3dmol.org/build/3Dmol.js',)
  view.addModel(open(pdb_file,'r').read(),'pdb')

  if color == "lDDT":
    view.setStyle({'cartoon': {'colorscheme': {'prop':'b','gradient': 'roygb','min':50,'max':90}}})
  elif color == "rainbow":
    view.setStyle({'cartoon': {'color':'spectrum'}})
  # elif color == "chain":
  #   chains = len(queries[0][1]) + 1 if is_complex else 1
  #   for n,chain,color in zip(range(chains),list("ABCDEFGH"),
  #                    ["lime","cyan","magenta","yellow","salmon","white","blue","orange"]):
  #     view.setStyle({'chain':chain},{'cartoon': {'color':color}})
  if show_sidechains:
    BB = ['C','O','N']
    view.addStyle({'and':[{'resn':["GLY","PRO"],'invert':True},{'atom':BB,'invert':True}]},
                        {'stick':{'colorscheme':f"WhiteCarbon",'radius':0.3}})
    view.addStyle({'and':[{'resn':"GLY"},{'atom':'CA'}]},
                        {'sphere':{'colorscheme':f"WhiteCarbon",'radius':0.3}})
    view.addStyle({'and':[{'resn':"PRO"},{'atom':['C','O'],'invert':True}]},
                        {'stick':{'colorscheme':f"WhiteCarbon",'radius':0.3}})
  if show_mainchains:
    BB = ['C','O','N','CA']
    view.addStyle({'atom':BB},{'stick':{'colorscheme':f"WhiteCarbon",'radius':0.3}})

  view.zoomTo()
  return view

show_pdb('AF-P14618-F1/AF-P14618-F1-model_v3.pdb').show()