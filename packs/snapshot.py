import yol
import pathlib as path

DEFAULT_PACK="packs/run_last"

def save_snapshot(data, config):
    path = path.Path(DEFAULT_PACK)
    path.["config.yaml"].write_text(config)
    data['results'].to_csv(path["results.csv"])

def load_snapshot():
    path = path.Path(DEFAULT_PACK)
    res = pyol.load_file(path["result.csv"])
    res[value] = float(res[value])
    return res}