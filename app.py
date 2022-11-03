from pathlib import Path

from flask import Flask, jsonify, render_template
from biopandas.pdb import PandasPdb

app = Flask(__name__)


@app.route('/<name>', methods=['GET'])
def get_molecula_info(name):
    file_path = Path(f'downloads/{name}.pdb')
    if file_path.exists():
        print(file_path)
        ppdb = PandasPdb().read_pdb(str(file_path))
    else:
        ppdb = PandasPdb().fetch_pdb(name)
        ppdb.to_pdb(path=f'downloads/{name}.pdb')
    # return jsonify({
    #     'pdbCode': ppdb.code,
    #     'pdbHeaderLine': ppdb.header,
    #     'pdbRaw1000': ppdb.pdb_text[:1000]
    # }), 200
    reference_point = (9.362, 41.410, 10.542)
    distances = ppdb.distance(xyz=reference_point, records=('ATOM',))
    return render_template('molecule.html', code=ppdb.code, distances=distances)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
