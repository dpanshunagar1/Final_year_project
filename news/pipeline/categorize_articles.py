# rss_pipeline_scripts/categorize_articles.py

# Define categories and their associated keywords
CATEGORY_KEYWORDS = {
    "TECHNOLOGY": ["technology", "tech", "smartphone", "artificial intelligence", "AI", "software", "internet", "innovation", "digital", "computing"],
    "WORLD NEWS": ["world", "international", "global", "foreign", "countries", "nations", "politics", "conflict", "diplomacy", "borders"],
    "SPORTS": ["sports", "football", "cricket", "hockey", "tennis", "golf", "racing", "athlete", "tournament", "championship"],
    "BUSINESS": ["business", "economy", "finance", "market", "stock", "company", "trade", "investment", "profit", "revenue"],
    "POLITICS": ["politics", "government", "election", "president", "minister", "party", "parliament", "legislation", "policy", "vote"],
    "ENTERTAINMENT": ["entertainment", "movie", "film", "music", "song", "actor", "celebrity", "show", "art", "culture"],
    "HEALTH": ["health", "medical", "disease", "treatment", "doctor", "hospital", "wellness", "nutrition", "pandemic", "virus"],
    "SCIENCE": ["science", "research", "discovery", "study", "experiment", "physics", "chemistry", "biology", "astronomy", "nature"],
    "LIFESTYLE": ["lifestyle", "fashion", "travel", "food", "home", "style", "beauty", "culture", "hobbies", "relationships"],
    "LOCAL NEWS": ["local", "city", "region", "community", "news", "events", "government", "council", "residents", "area"],
    "INDIA": ["india", "indian", "bharat", "new delhi", "mumbai", "kolkata", "chennai", "rupee", "gandhi", "modi"],
}

def predict_article_category(title, summary, content):
    text = f"{title} {summary} {content or ''}".lower()
    matched_categories = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        match_count = 0
        for keyword in keywords:
            if keyword in text:
                match_count += 1
        if match_count > 0:
            matched_categories[category] = match_count

    if matched_categories:
        # Return the category with the most keyword matches
        return max(matched_categories, key=matched_categories.get)
    else:
        return None

if __name__ == '__main__':
    test_title = "New Smartphone Launched with AI Features"
    test_summary = "A leading tech company has announced its latest smartphone."
    test_content = "The phone boasts a powerful processor and advanced AI capabilities..."
    predicted_category = predict_article_category(test_title, test_summary, test_content)
    print(f"Predicted category: {predicted_category}")

    test_title_world = "UN calls for ceasefire as conflict intensifies"
    predicted_category_world = predict_article_category(test_title_world, "", "")
    print(f"Predicted category: {predicted_category_world}")

    test_title_india = "PM Modi addresses the nation on economic reforms"
    predicted_category_india = predict_article_category(test_title_india, "", "")
    print(f"Predicted category: {predicted_category_india}")