import requests
from bs4 import BeautifulSoup

def get_data_by_separator(text, separator = '[edit]', min_characters = 50):
    return [x for x in text.split(separator) if len(x) >= min_characters]

def get_data_by_chunks(text, num_chunks = 25):
    chunk_size = len(text) // num_chunks
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

class ChunkGenerator:
    def __init__(self, num_chunks = 25,
                use_chunks = True,
                use_separator = False,
                separator = '[edit]',
                ):
        self.num_chunks = num_chunks
        self.separator = separator
        self.use_separator = use_separator
        self.use_chunks = use_chunks

    def get_data_from_wikipedia(self, search_prompt):
        use_separator = self.use_separator
        use_chunks = self.use_chunks

        wiki_api_url = "https://en.wikipedia.org/w/api.php"

        search_params = {
            "format": "json",
            "action": "query",
            "list": "search",
            "srsearch": f"{search_prompt}",
        }

        search_response = requests.get(wiki_api_url, params=search_params)
        search_data = search_response.json()

        # Check if there are search results
        if "query" in search_data and "search" in search_data["query"]:
            search_results = search_data["query"]["search"]

            if search_results:
                # Get the title of the first search result
                first_result_title = search_results[0]["title"]

                # Define parameters for the parse API request
                parse_params = {
                    "format": "json",
                    "action": "parse",
                    "page": first_result_title,
                }

                # Make the parse API request
                parse_response = requests.get(wiki_api_url, params=parse_params)
                parse_data = parse_response.json()

                # Extract and print the text content of the first search result
                if "parse" in parse_data:
                    text_content = parse_data["parse"]["text"]["*"]
                    soup = BeautifulSoup(text_content, "html.parser")
                    cleaned_text = soup.get_text()
                else:
                    print("Failed to retrieve article content.")
            else:
                print("No search results found.")
        else:
            print("Search API request failed.")
        if use_separator == True:
            use_chunks = False
            return get_data_by_separator(cleaned_text, separator = self.separator, min_characters = 50)
        if use_chunks == True:
            use_separator = False
            return get_data_by_chunks(cleaned_text, num_chunks = self.num_chunks)