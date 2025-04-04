from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Searches for LinkedIn or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name} LinkedIn OR Twitter")

    for result in res:
        url = result.get("url", "")
        if "linkedin.com" in url or "twitter.com" in url:
            return url

    return None  # Return None if no relevant profile is found
