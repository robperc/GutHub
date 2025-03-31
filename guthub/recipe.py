import requests
from bs4 import BeautifulSoup

class Recipe:
    def __init__(self, url):
        self.name = None
        self.url = url
        self.ingredients = []
        self.instructions = []
        self.categories = []

    def _extract_text(self, soup, selectors):
        """Helper function to extract and clean text from multiple selectors."""
        results = []
        seen = set()
        for selector in selectors:
            for element in soup.select(selector):
                text = element.get_text(separator=" ", strip=True)  # Use separator to handle nested tags
                cleaned_text = " ".join(text.split())  # Normalize whitespace
                cleaned_text = cleaned_text.replace("▢", "").strip()  # Remove unwanted symbols
                if cleaned_text not in seen:
                    seen.add(cleaned_text)
                    results.append(cleaned_text)
        return results

    def get_recipe(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract recipe name
            name_selectors = [
                'h1.headline',
                'h1.recipe-title', 
                '.wprm-recipe-name', 
                'h1.entry-title', 
                '.headline', 
                '.recipe-summary__h1',
                '.article-heading.text-headline-400'  # Added selector for AllRecipes recipe name
            ]
            name_results = self._extract_text(soup, name_selectors)
            self.name = name_results[0] if name_results else None

            # Extract categories
            category_selectors = [
                '.breadcrumbs li a',  # Common breadcrumb navigation
                '.category', 
                '.tags a', 
                '.recipe-categories a'
            ]
            self.categories = self._extract_text(soup, category_selectors)

            # Filter out categories with more than 4 words
            self.categories = [category for category in self.categories if len(category.split()) <= 4]

            # Extract ingredients
            ingredient_selectors = [
                '.ingredient', 
                '.ingredients-item', 
                '.recipe-ingredient', 
                '.wprm-recipe-ingredient', 
                '.ingredients-section li', 
                '.recipe-ingredients__list-item', 
                'span.ingredients-item-name',
                '.ingredients-item-name',
                '.mm-recipes-structured-ingredients__list li'
            ]
            self.ingredients = self._extract_text(soup, ingredient_selectors)

            # Extract instructions
            instruction_selectors = [
                '.instruction', 
                '.step', 
                '.recipe-step', 
                '.wprm-recipe-instruction', 
                '.instructions-section li', 
                '.recipe-directions__list--item', 
                'div.paragraph p',
                '.instructions-section-item p',
                '#mm-recipes-steps__content_1-0'  # Added selector for AllRecipes instructions
            ]
            self.instructions = self._extract_text(soup, instruction_selectors)

            # Additional fallback for specific container structure in the example URL
            if not self.ingredients:
                self.ingredients = self._extract_text(soup, ['.wprm-recipe-ingredients li'])
            if not self.instructions:
                self.instructions = self._extract_text(soup, ['.wprm-recipe-instructions li'])

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the webpage: {e}")
        except Exception as e:
            print(f"Error parsing the webpage: {e}")

    def to_dict(self):
        """Return the recipe data as a dictionary."""
        return {
            "name": self.name,
            "url": self.url,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "categories": self.categories,
        }
