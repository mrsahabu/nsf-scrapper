import requests
import time
import csv
import itertools
import concurrent.futures
import logging

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def generate_keywords():
    base_keywords = [
        "water",
        "climate",
        "AI",
        "machine learning",
        "data science",
        "biology",
        "chemistry",
        "physics",
        "engineering",
        "robotics",
        "astronomy",
        "neuroscience",
        "oceanography",
        "ecology",
        "genetics",
        "nanotechnology",
        "renewable energy",
        "sustainability",
        "geology",
        "meteorology",
        "cybersecurity",
        "blockchain",
        "quantum computing",
        "biotechnology",
        "astrophysics",
        "materials science",
        "agriculture",
        "environmental science",
        "earth science",
        "public health",
        "epidemiology",
        "artificial intelligence",
        "deep learning",
        "computational biology",
        "bioinformatics",
        "genomics",
        "paleontology",
        "marine biology",
        "wildlife conservation",
        "forestry",
        "hydrology",
        "seismology",
        "biophysics",
        "bioengineering",
        "medical imaging",
        "photonics",
        "optics",
        "nuclear physics",
        "space exploration",
        "pharmacology",
        "behavioral science",
        "psychology",
        "cognitive science",
        "anthropology",
        "sociology",
        "linguistics",
        "archaeology",
        "economics",
        "political science",
        "education research",
        "social sciences",
        "statistics",
        "operations research",
        "theoretical physics",
        "fluid dynamics",
        "geophysics",
        "astrobiology",
        "bioinformatics",
        "computational neuroscience",
        "synthetic biology",
        "systems biology",
        "data analytics",
        "computer vision",
        "natural language processing",
        "speech recognition",
        "renewable materials",
        "biodegradable plastics",
        "urban planning",
        "climate modeling",
        "energy storage",
        "battery technology",
        "hydrogen fuel cells",
        "carbon capture",
        "remote sensing",
        "satellite imaging",
        "quantum materials",
        "graphene research",
        "fusion energy",
        "gene therapy",
        "CRISPR",
        "molecular biology",
        "agricultural engineering",
        "soil science",
        "water resource management",
        "environmental policy",
        "conservation biology",
        "climate adaptation",
        "biodiversity",
        "ecosystem restoration",
        "earth observation",
        "geospatial analysis",
        "wildfire science",
        "coral reef research",
        "deep-sea exploration",
        "marine conservation",
        "exoplanet research",
        "astrochemistry",
        "astrogeology",
        "planetary science",
        "urban economics",
        "health informatics",
        "quantitative finance",
        "operations management",
        "supply chain logistics",
        "biomedical engineering",
        "telecommunications",
        "space technology",
        "food science",
        "veterinary medicine",
        "human-computer interaction",
        "game development",
        "sports analytics",
        "wearable technology",
        "precision agriculture",
        "industrial automation",
        "aerospace engineering",
        "microbiology",
        "pharmaceutical sciences",
        "nutrition science",
        "neuromorphic computing",
        "solar energy",
        "wind energy",
        "hydropower",
        "thermal physics",
        "AI ethics",
        "computational physics",
        "smart grids",
        "internet of things",
        "edge computing",
        "5G networks",
        "bioeconomy",
        "quantum biology",
        "medtech",
        "digital forensics",
        "space medicine",
        "sports medicine",
        "criminal justice",
        "constitutional law",
        "corporate law",
        "intellectual property law",
        "media studies",
        "journalism",
        "public relations",
        "film studies",
        "broadcasting",
        "advertising",
        "marketing analytics",
        "brand management",
    ]

    suffixes = [
        "research",
        "study",
        "project",
        "science",
        "analysis",
        "trends",
        "technology",
        "development",
        "innovation",
        "solutions",
    ]
    keyword_combinations = list(itertools.product(base_keywords, suffixes))
    expanded_keywords = [f"{kw[0]} {kw[1]}" for kw in keyword_combinations]

    return expanded_keywords[:50000]  # Increase to 50,000 keywords


def fetch_award_data(keyword, results_per_page=25, filename="emails.csv"):
    base_url = "https://www.research.gov/awardapi-service/v1/awards.json"
    data_list = []
    offset = 1  # Offset starts at 1
    emails = set()

    logger.info(f"Starting to fetch data for keyword: {keyword}")

    while True:
        params = {
            "keyword": keyword,
            "printFields": "title,piEmail,piFirstName,piLastName,piMiddeInitial,fundProgramName,awardeeStateCode",
            "offset": offset,
        }
        try:
            logger.info(f"Fetching data from offset {offset}")
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            awards = data.get("response", {}).get("award", [])
            if not awards:
                logger.info(
                    f"No more awards found for keyword: {keyword} at offset {offset}. Moving to next keyword."
                )
                break  # Move to the next keyword if no data is found

            for award in awards:
                email = award.get("piEmail")
                if email and email not in emails:
                    emails.add(email)
                    data_list.append(
                        [
                            award.get("piFirstName", ""),
                            award.get("piMiddleInitial", ""),
                            award.get("piLastName", ""),
                            award.get("piEmail", ""),
                            award.get("fundProgramName", ""),
                            award.get("awardeeStateCode", ""),
                            award.get("title", ""),
                        ]
                    )

            # Save data to CSV incrementally
            if data_list:
                save_to_csv_incremental(data_list, filename)
                data_list.clear()

            # If fewer than 25 awards are returned, we've likely reached the end
            if len(awards) < results_per_page:
                logger.info(
                    f"Fewer than {results_per_page} records returned. No more records available for this keyword."
                )
                break

            offset += 1  # Increment the offset by 1, as requested
            time.sleep(0.5)  # Adjust the sleep time as needed for rate-limiting
        except Exception as e:
            logger.error(
                f"Error fetching data for keyword {keyword} at offset {offset}: {e}"
            )
            time.sleep(5)

    return emails


def save_to_csv_incremental(data_list, filename="emails.csv"):
    # Append to the file if it exists, create a new one if not
    file_exists = False
    try:
        with open(filename, mode="r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                [
                    "First Name",
                    "Middle Initial",
                    "Last Name",
                    "Email",
                    "Fund Program",
                    "State Code",
                    "Title",
                ]
            )
        writer.writerows(data_list)
    logger.info(f"Incremental data saved to {filename}")


if __name__ == "__main__":
    keywords = generate_keywords()
    all_emails = set()

    logger.info("Starting the data fetching process...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_award_data, keywords))

    logger.info("Data fetching process completed.")
