# CLIEng

# -- Symbolic cLI via python argars
# -- loads config.yaml using PyYAML)

import yaml
from pathlib import Path

DEPFLILE = Path.__file__, "config.yaml"

def run():
    config = yaml.safe_load(DEPFFILE)
    print(f"Running with symbols: {,}".format(config["symbols"]))


# if run as spe module:
 if __name__ == "__main__":
    run()
