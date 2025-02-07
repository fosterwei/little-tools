import asyncio
import aiohttp
import json
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin

# =======================
# Configuration Constants
# =======================
OPENROUTER_API_KEY = "" # Replace with your OpenRouter API key
SERPAPI_API_KEY = "" # Replace with your SERPAPI API key
JINA_API_KEY = "" # Replace with your JINA API key


# Endpoints
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
SERPAPI_URL = "https://serpapi.com/search"
JINA_BASE_URL = "https://r.jina.ai/"

# Default LLM model (can be changed if desired)
DEFAULT_MODEL = "anthropic/claude-3.5-haiku"


# ============================
# Asynchronous Helper Functions
# ============================

async def call_openrouter_async(session, messages, model=DEFAULT_MODEL):
    """
    Asynchronously call the OpenRouter chat completion API with the provided messages.
    Returns the content of the assistant's reply.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "X-Title": "OpenDeepResearcher, by Matt Shumer",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages
    }
    try:
        async with session.post(OPENROUTER_URL, headers=headers, json=payload) as resp:
            if resp.status == 200:
                result = await resp.json()
                try:
                    return result['choices'][0]['message']['content']
                except (KeyError, IndexError) as e:
                    print("Unexpected OpenRouter response structure:", result)
                    return None
            else:
                text = await resp.text()
                print(f"OpenRouter API error: {resp.status} - {text}")
                return None
    except Exception as e:
        print("Error calling OpenRouter:", e)
        return None


async def generate_search_queries_async(session, user_query):
    """
    Ask the LLM to produce up to four precise search queries (in Python list format)
    based on the user's query.
    """
    prompt = (
        "You are an expert research assistant. Given the user's query, generate up to four distinct, "
        "precise search queries that would help gather comprehensive information on the topic. "
        "Return only a Python list of strings, for example: ['query1', 'query2', 'query3']."
    )
    messages = [
        {"role": "system", "content": "You are a helpful and precise research assistant."},
        {"role": "user", "content": f"User Query: {user_query}\n\n{prompt}"}
    ]
    response = await call_openrouter_async(session, messages)
    if response:
        try:
            search_queries = eval(response)
            if isinstance(search_queries, list):
                return search_queries
            else:
                print("LLM did not return a list. Response:", response)
                return []
        except Exception as e:
            print("Error parsing search queries:", e, "\nResponse:", response)
            return []
    return []


async def perform_search_async(session, query):
    """
    Asynchronously perform a Google search using SERPAPI for the given query.
    Returns a list of result URLs.
    """
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "engine": "google"
    }
    try:
        async with session.get(SERPAPI_URL, params=params) as resp:
            if resp.status == 200:
                results = await resp.json()
                if "organic_results" in results:
                    links = [item.get("link") for item in results["organic_results"] if "link" in item]
                    return links
                else:
                    print("No organic results in SERPAPI response.")
                    return []
            else:
                text = await resp.text()
                print(f"SERPAPI error: {resp.status} - {text}")
                return []
    except Exception as e:
        print("Error performing SERPAPI search:", e)
        return []


async def fetch_webpage_text_async(session, url):
    """
    Asynchronously retrieve the text content of a webpage using Jina.
    The URL is appended to the Jina endpoint.
    """
    full_url = f"{JINA_BASE_URL}{url}"
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}"
    }
    try:
        async with session.get(full_url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.text()
            else:
                text = await resp.text()
                print(f"Jina fetch error for {url}: {resp.status} - {text}")
                return ""
    except Exception as e:
        print("Error fetching webpage text with Jina:", e)
        return ""


async def is_page_useful_async(session, user_query, page_text):
    """
    Ask the LLM if the provided webpage content is useful for answering the user's query.
    The LLM must reply with exactly "Yes" or "No".
    """
    prompt = (
        "You are a critical research evaluator. Given the user's query and the content of a webpage, "
        "determine if the webpage contains information relevant and useful for addressing the query. "
        "Respond with exactly one word: 'Yes' if the page is useful, or 'No' if it is not. Do not include any extra text."
    )
    messages = [
        {"role": "system", "content": "You are a strict and concise evaluator of research relevance."},
        {"role": "user", "content": f"User Query: {user_query}\n\nWebpage Content (first 20000 characters):\n{page_text[:20000]}\n\n{prompt}"}
    ]
    response = await call_openrouter_async(session, messages)
    if response:
        answer = response.strip()
        if answer in ["Yes", "No"]:
            return answer
        else:
            if "Yes" in answer:
                return "Yes"
            elif "No" in answer:
                return "No"
    return "No"


async def extract_relevant_context_async(session, user_query, search_query, page_text):
    """
    Given the original query, the search query used, and the page content,
    have the LLM extract all information relevant for answering the query.
    """
    prompt = (
        "You are an expert information extractor. Given the user's query, the search query that led to this page, "
        "and the webpage content, extract all pieces of information that are relevant to answering the user's query. "
        "Return only the relevant context as plain text without commentary."
    )
    messages = [
        {"role": "system", "content": "You are an expert in extracting and summarizing relevant information."},
        {"role": "user", "content": f"User Query: {user_query}\nSearch Query: {search_query}\n\nWebpage Content (first 20000 characters):\n{page_text[:20000]}\n\n{prompt}"}
    ]
    response = await call_openrouter_async(session, messages)
    if response:
        return response.strip()
    return ""


async def get_new_search_queries_async(session, user_query, previous_search_queries, all_contexts):
    """
    Based on the original query, the previously used search queries, and all the extracted contexts,
    ask the LLM whether additional search queries are needed.
    """
    context_combined = "\n".join(all_contexts)
    prompt = (
        "You are an analytical research assistant. Based on the original query, the search queries performed so far, "
        "and the extracted contexts from webpages, determine if further research is needed. "
        "If further research is needed, provide up to four new search queries as a Python list (for example, "
        "['new query1', 'new query2']). If you believe no further research is needed, respond with exactly <done>."
        "\nOutput only a Python list or the token <done> without any additional text."
    )
    messages = [
        {"role": "system", "content": "You are a systematic research planner."},
        {"role": "user", "content": f"User Query: {user_query}\nPrevious Search Queries: {previous_search_queries}\n\nExtracted Relevant Contexts:\n{context_combined}\n\n{prompt}"}
    ]
    response = await call_openrouter_async(session, messages)
    if response:
        cleaned = response.strip()
        if cleaned == "<done>":
            return "<done>"
        try:
            new_queries = eval(cleaned)
            if isinstance(new_queries, list):
                return new_queries
            else:
                print("LLM did not return a list for new search queries. Response:", response)
                return []
        except Exception as e:
            print("Error parsing new search queries:", e, "\nResponse:", response)
            return []
    return []


async def generate_final_report_async(session, user_query, all_contexts):
    """
    Generate the final comprehensive report using all gathered contexts.
    """
    context_combined = "\n".join(all_contexts)
    prompt = (
        "You are an expert researcher and report writer. Based on the gathered contexts below and the original query, "
        "write a comprehensive, well-structured, and detailed report that addresses the query thoroughly. "
        "Include all relevant insights and conclusions without extraneous commentary."
    )
    messages = [
        {"role": "system", "content": "You are a skilled report writer."},
        {"role": "user", "content": f"User Query: {user_query}\n\nGathered Relevant Contexts:\n{context_combined}\n\n{prompt}"}
    ]
    report = await call_openrouter_async(session, messages)
    return report


async def process_link(session, link, user_query, search_query):
    """
    Process a single link: fetch its content, judge its usefulness, and if useful, extract the relevant context.
    """
    print(f"Fetching content from: {link}")
    page_text = await fetch_webpage_text_async(session, link)
    if not page_text:
        return None
    usefulness = await is_page_useful_async(session, user_query, page_text)
    print(f"Page usefulness for {link}: {usefulness}")
    if usefulness == "Yes":
        context = await extract_relevant_context_async(session, user_query, search_query, page_text)
        if context:
            print(f"Extracted context from {link} (first 200 chars): {context[:200]}")
            return context
    return None


async def fetch_sitemap_async(session, sitemap_url):
    """
    Fetch and parse a sitemap XML file.
    Returns a list of all URLs found in the sitemap.
    """
    try:
        async with session.get(sitemap_url) as resp:
            if resp.status == 200:
                sitemap_content = await resp.text()
                root = ET.fromstring(sitemap_content)
                
                # Handle both standard sitemaps and sitemap indexes
                urls = []
                
                # Check if this is a sitemap index
                if 'sitemapindex' in root.tag:
                    # Fetch each individual sitemap
                    sitemap_tasks = []
                    for sitemap in root.findall('.//{*}loc'):
                        sitemap_tasks.append(fetch_sitemap_async(session, sitemap.text))
                    results = await asyncio.gather(*sitemap_tasks)
                    for result in results:
                        urls.extend(result)
                else:
                    # Regular sitemap - extract URLs directly
                    for url in root.findall('.//{*}loc'):
                        urls.append(url.text)
                
                return urls
            else:
                print(f"Error fetching sitemap: {resp.status}")
                return []
    except Exception as e:
        print(f"Error processing sitemap: {e}")
        return []


async def fetch_sitemap_async(session, sitemap_url):
    """
    Fetch and parse a sitemap XML file.
    Returns a list of all valid webpage URLs found in the sitemap (excluding image URLs).
    """
    try:
        async with session.get(sitemap_url) as resp:
            if resp.status == 200:
                sitemap_content = await resp.text()
                root = ET.fromstring(sitemap_content)
                
                # Handle both standard sitemaps and sitemap indexes
                urls = []
                
                # Helper function to check if URL is valid for our purposes
                def is_valid_url(url):
                    # Exclude common image file extensions and CDN URLs
                    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
                    cdn_indicators = ('cdn.', '/cdn/', '/assets/', '/images/', '/img/')
                    
                    url_lower = url.lower()
                    return not (
                        url_lower.endswith(image_extensions) or
                        any(indicator in url_lower for indicator in cdn_indicators) or
                        'cdn.shopify.com' in url_lower
                    )
                
                # Check if this is a sitemap index
                if 'sitemapindex' in root.tag:
                    # Fetch each individual sitemap
                    sitemap_tasks = []
                    for sitemap in root.findall('.//{*}loc'):
                        if not is_valid_url(sitemap.text):  # Skip image sitemaps
                            continue
                        sitemap_tasks.append(fetch_sitemap_async(session, sitemap.text))
                    if sitemap_tasks:
                        results = await asyncio.gather(*sitemap_tasks)
                        for result in results:
                            urls.extend(result)
                else:
                    # Regular sitemap - extract URLs directly
                    for url in root.findall('.//{*}loc'):
                        if is_valid_url(url.text):
                            urls.append(url.text)
                
                return urls
            else:
                print(f"Error fetching sitemap: {resp.status}")
                return []
    except Exception as e:
        print(f"Error processing sitemap: {e}")
        return []

async def select_relevant_urls_async(session, urls, keyword, research_context):
    """
    Ask the LLM to select 10-20 most relevant URLs based on the keyword
    and previous research context.
    """
    # First, let's filter URLs to remove any that are obviously irrelevant
    def url_relevance_score(url, keyword):
        """Basic relevance scoring for initial filtering"""
        url_lower = url.lower()
        keyword_parts = keyword.lower().split()
        
        # Initialize score
        score = 0
        
        # Check for keyword parts in URL
        for part in keyword_parts:
            if part in url_lower:
                score += 1
        
        # Penalize obvious non-content pages
        if any(x in url_lower for x in ['/cart', '/checkout', '/account', '/login', '/admin']):
            score -= 10
            
        return score

    # Sort URLs by initial relevance score
    scored_urls = [(url, url_relevance_score(url, keyword)) for url in urls]
    scored_urls.sort(key=lambda x: x[1], reverse=True)
    
    # Take top 50 URLs for LLM analysis
    candidate_urls = [url for url, score in scored_urls[:50]]
    
    prompt = (
        "You are an expert content curator specializing in finding relevant web content. "
        "Your task is to select the most relevant URLs for researching the given keyword. "
        "Consider URL structure and likely content relevance.\n\n"
        "Instructions:\n"
        "0. Look for exact phrase matches in the URL slug first"
        "1. Analyze each URL carefully\n"
        "2. Select 10-20 URLs that are most likely to contain relevant content\n"
        "3. Return ONLY a Python list containing the selected URLs\n"
        "4. Focus on content-rich pages (avoid cart, checkout, account pages)\n\n"
        f"Keyword: <keyword>{keyword}</keyword>\n"
        f"Research Context Summary: {research_context[:500]}...\n\n"
        "Available URLs:\n" + "\n".join(candidate_urls)
    )
    
    messages = [
        {"role": "system", "content": "You are a precise URL curator focusing on content relevance."},
        {"role": "user", "content": prompt}
    ]
    
    response = await call_openrouter_async(session, messages)
    if response:
        try:
            # Clean the response to handle potential formatting issues
            cleaned_response = response.strip()
            if cleaned_response.startswith("```python"):
                cleaned_response = cleaned_response.split("```python")[1]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response.rsplit("```", 1)[0]
                
            selected_urls = eval(cleaned_response)
            
            if isinstance(selected_urls, list):
                # Ensure all URLs are from the original list
                valid_urls = [url for url in selected_urls if url in urls]
                
                if 10 <= len(valid_urls) <= 20:
                    return valid_urls
                elif len(valid_urls) > 20:
                    return valid_urls[:15]
                else:
                    # If not enough valid URLs, fall back to top scoring URLs
                    return [url for url, _ in scored_urls[:15]]
        except Exception as e:
            print(f"Error parsing URL selection: {e}")
            # Fallback to scored URLs
            return [url for url, _ in scored_urls[:15]]
            
    return [url for url, _ in scored_urls[:15]]

async def analyze_website_content_async(session, urls, keyword, research_context):
    """
    Analyze content from selected URLs, extracting images, information, and context.
    Returns a structured analysis of each page.
    """
    analyses = []
    
    for url in urls:
        print(f"Analyzing website content from: {url}")
        page_text = await fetch_webpage_text_async(session, url)
        
        if not page_text:
            continue
            
        # Extract relevant information using the LLM
        prompt = (
            "You are an expert content analyzer. Given the webpage content, extract relevant information "
            "related to our keyword and research topic. Format your response as a valid JSON object with "
            "the following structure:\n"
            "{\n"
            '  "key_info": "Main points and findings related to the topic",\n
            '  "relevant_links": "find relevant links
            '  "images": "relevant image links to be used in content mentioned in the content",\n'
            '  "context": "Additional context and supporting information"\n'
            "}\n\n"
            f"Keyword: {keyword}\n"
            "Note: Ensure your response is valid JSON with proper escaping of special characters."
        )
        
        messages = [
            {"role": "system", "content": "You are a thorough content analyzer producing valid JSON output."},
            {"role": "user", "content": f"{prompt}\n\nPage Content (first 20000 chars):\n{page_text[:20000]}"}
        ]
        
        analysis = await call_openrouter_async(session, messages)
        if analysis:
            try:
                # Clean the response to ensure valid JSON
                cleaned_analysis = analysis.strip()
                if cleaned_analysis.startswith("```json"):
                    cleaned_analysis = cleaned_analysis.split("```json")[1]
                if cleaned_analysis.endswith("```"):
                    cleaned_analysis = cleaned_analysis.rsplit("```", 1)[0]
                
                parsed_analysis = json.loads(cleaned_analysis)
                parsed_analysis['url'] = url
                analyses.append(parsed_analysis)
            except json.JSONDecodeError as e:
                print(f"Error parsing analysis for {url}: {e}")
                continue
    
    return analyses


async def create_detailed_outline_async(session, research_context, website_analyses, keyword):
    """
    Create a detailed outline combining the initial research and website-specific analyses.
    """
    # Prepare a summary of website analyses
    website_summary = "\n".join([
        f"URL: {analysis['url']}\n"
        f"Key Info: {analysis['key_info']}\n"
        f"Context: {analysis['context']}\n"
        for analysis in website_analyses
    ])
    
    prompt = (
        "You are an expert content organizer. Create a detailed outline that combines:\n"
        "1. The initial research findings\n"
        "2. The specific information found on the analyzed website\n"
        "The outline should be comprehensive, well-structured, and focused on our keyword.\n"
        "Use proper outline format with main sections (I, II, III) and subsections (A, B, C).\n"
        "You need to include real internal links and images from <websitesummary>"
        f"Keyword: {keyword}"
    )
    
    messages = [
        {"role": "system", "content": "You are a skilled content organizer."},
        {"role": "user", "content": 
            f"{prompt}\n\n"
            f"Initial Research:\n{research_context}\n\n"
            f"Website Analyses:<websitesummary>\n{website_summary}</websitesummary>"}
    ]

    
    
    outline = await call_openrouter_async(session, messages)
    return outline


# =========================
# Main Asynchronous Routine
# =========================

async def async_main():
    user_query = input("Enter your research query/topic: ").strip()
    iter_limit_input = input("Enter maximum number of iterations (default 10): ").strip()
    iteration_limit = int(iter_limit_input) if iter_limit_input.isdigit() else 10

    aggregated_contexts = []    # All useful contexts from every iteration
    all_search_queries = []     # Every search query used across iterations
    iteration = 0

    async with aiohttp.ClientSession() as session:
        # ----- INITIAL SEARCH QUERIES -----
        new_search_queries = await generate_search_queries_async(session, user_query)
        if not new_search_queries:
            print("No search queries were generated by the LLM. Exiting.")
            return
        all_search_queries.extend(new_search_queries)

        # ----- ITERATIVE RESEARCH LOOP -----
        while iteration < iteration_limit:
            print(f"\n=== Iteration {iteration + 1} ===")
            iteration_contexts = []

            # For each search query, perform SERPAPI searches concurrently
            search_tasks = [perform_search_async(session, query) for query in new_search_queries]
            search_results = await asyncio.gather(*search_tasks)

            # Aggregate all unique links from all search queries of this iteration
            unique_links = {}
            for idx, links in enumerate(search_results):
                query = new_search_queries[idx]
                for link in links:
                    if link not in unique_links:
                        unique_links[link] = query

            print(f"Aggregated {len(unique_links)} unique links from this iteration.")

            # Process each link concurrently
            link_tasks = [
                process_link(session, link, user_query, unique_links[link])
                for link in unique_links
            ]
            link_results = await asyncio.gather(*link_tasks)

            # Collect non-None contexts
            for res in link_results:
                if res:
                    iteration_contexts.append(res)

            if iteration_contexts:
                aggregated_contexts.extend(iteration_contexts)
            else:
                print("No useful contexts were found in this iteration.")

            # Check if more searches are needed
            new_search_queries = await get_new_search_queries_async(session, user_query, all_search_queries, aggregated_contexts)
            if new_search_queries == "<done>":
                print("LLM indicated that no further research is needed.")
                break
            elif new_search_queries:
                print("LLM provided new search queries:", new_search_queries)
                all_search_queries.extend(new_search_queries)
            else:
                print("LLM did not provide any new search queries. Ending the loop.")
                break

            iteration += 1

        # Generate initial research report
        print("\nGenerating initial research report...")
        final_report = await generate_final_report_async(session, user_query, aggregated_contexts)
        print("\n==== INITIAL RESEARCH REPORT ====\n")
        print(final_report)

        # Begin website-specific research phase
        print("\nMoving to website-specific research phase...")
        sitemap_url = input("Enter the sitemap URL: ").strip()
        keyword = input("Enter the specific keyword to focus on: ").strip()

        # Fetch and process sitemap
        print("Fetching sitemap...")
        all_urls = await fetch_sitemap_async(session, sitemap_url)
        if not all_urls:
            print("No URLs found in sitemap. Exiting.")
            return

        # Select relevant URLs
        print("Selecting relevant URLs...")
        selected_urls = await select_relevant_urls_async(session, all_urls, keyword, final_report)
        print(f"Selected {len(selected_urls)} relevant URLs")

        # Analyze website content
        print("Analyzing website content...")
        website_analyses = await analyze_website_content_async(session, selected_urls, keyword, final_report)
        print(f"Completed analysis of {len(website_analyses)} pages")

        # Create detailed outline
        print("\nGenerating detailed outline...")
        detailed_outline = await create_detailed_outline_async(session, final_report, website_analyses, keyword)
        
        print("\n==== DETAILED OUTLINE ====\n")
        print(detailed_outline)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()``
