import sys
import importlib


def check_existance() -> bool:
    packages = {"pandas": "Data manipulation ready",
                "matplotlib": "Visualization ready",
                "requests": " Network access ready",
                "numpy": "Numerical computations ready"
                }
    loaded_modules = {}
    missing = []
    all_imported = True
    print("Checking dependencies:")

    for pkg, message in packages.items():
        try:
            module = importlib.import_module(pkg)
            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {pkg} ({version}) - {message}")
            loaded_modules[pkg] = module
        except ImportError:
            print(f"[MISSING] {pkg} - install using pip: pip install {pkg}")
            print(f"install using poetry: poetry add {pkg}\n")
            # pip installs globally or in venv
            # Poetry manages dependencies per project with lockfile.
            missing.append(pkg)
            all_imported = False

    return all_imported


def analyze_data() -> None:
    print("\nAnalyzing data...")
    import pandas as pd
    import numpy as np
    from matplotlib import pyplot as plt
    import requests
    url = "https://api.worldbank.org/v2/country/MAR/indicator/SP.POP.TOTL"
    url += "?format=json"
    try:
        data = requests.get(url).json()
        records = []
        for entry in data[1][:10]:
            if entry['value'] is not None:
                records.append({"year": int(entry['date']),
                                "population": entry['value']
                                })
        df = pd.DataFrame(records).sort_values(by="year")
        growth = np.diff(df['population'])
        idx = np.argmax(growth)
        max_year = df['year'].iloc[idx + 1]
        print("Generating visualization...")
        plt.figure(figsize=(12, 6))
        plt.plot(df['year'], df['population'], label='Population')
        plt.title("Morocco Population Growth (World Bank Data)")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.legend()
        plt.grid(True)
        plt.scatter(max_year, df['population'].iloc[idx + 1], color='red')
        output_file = "analysis.png"
        plt.savefig(output_file)
        print("\nAnalysis complete!")
        print(f"Results saved to: {output_file}")
    except Exception:
        print("Unexpected error happened")


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...\n")
    all_imported = check_existance()
    if not all_imported:
        print("\nImport all modules to run the analysis")
        sys.exit(1)
    analyze_data()
