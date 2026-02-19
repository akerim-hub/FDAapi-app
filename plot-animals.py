import requests
import pandas as pd
import matplotlib.pyplot as plt

def fetch_and_plot_animal_data():
    BASE_URL = "https://api.fda.gov/animalandveterinary/event.json"
    limit = 1000
    params = {"limit": limit}
    
    print(f"Fetching {limit} records from {BASE_URL}...")
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        results = data.get("results", [])
        if not results:
            print("No data found.")
            return

        species_list = []
        for record in results:
            animal = record.get("animal", {})
            species = animal.get("species")
            if species:
                species_list.append(species)
        
        # Count occurrences using pandas
        species_counts = pd.Series(species_list).value_counts()
        print("\nSpecies Counts:")
        print(species_counts)


        plt.figure(figsize=(10, 6))
        species_counts.plot(kind='bar', color='skyblue')
        plt.title('Animal Species Counts (FDA Open Data)')
        plt.xlabel('Species')
        plt.ylabel('Number of Events')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        

        output_file = 'animal_species_counts.png'
        plt.savefig(output_file)
        print(f"\nPlot saved to {output_file}")


    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_plot_animal_data()
