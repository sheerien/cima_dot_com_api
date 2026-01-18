# """
# AgentQL scraping logic with async playwright.
# """

# import agentql
# from agentql.ext.playwright.async_api import Page
# from playwright.async_api import async_playwright
# from app.settings import BASE_URL, AGENTQL_API_KEY
# from app.normalizer import normalize_elcinema

# # Configure AgentQL API key
# agentql.configure(api_key=AGENTQL_API_KEY)

# QUERY = """
# {
#     data{
#         title
#         img_url
#         trailer_url
#         plot

#         crew[]{
#             name
#             job
#         }

#         cast[]{
#             name
#             character
#         }

#         rate
#     }
# }
# """


# async def fetch_work(work_id: str) -> dict:
#     """
#     Fetch work metadata by work_id using AgentQL and normalize it.
#     Raises RuntimeError if anything goes wrong.
#     """
#     url = f"{BASE_URL}{work_id}/"

#     try:
#         async with async_playwright() as p:
#             browser = await p.chromium.launch(headless=True)
#             page: Page = agentql.wrap(await browser.new_page())
#             await page.goto(url)
#             response = await page.query_data(QUERY)
#             await browser.close()
#     except Exception as e:
#         raise RuntimeError(f"Failed to fetch work {work_id}: {str(e)}")

#     if "data" not in response:
#         raise RuntimeError(f"No data found for work {work_id}")

#     return normalize_elcinema(response["data"])


# """
# Synchronous scraper for ElCinema using AgentQL and Playwright.
# This avoids asyncio issues on Windows with Python 3.12.
# """

# import agentql
# from playwright.sync_api import sync_playwright
# from app.settings import AGENTQL_API_KEY, BASE_URL
# from app.normalizer import normalize_response

# # Configure AgentQL
# agentql.configure(api_key=AGENTQL_API_KEY)

# QUERY = """
# {
#     data{
#         title
#         img_url
#         trailer_url
#         plot

#         crew[]{
#             name
#             job
#         }

#         cast[]{
#             name
#             character
#         }

#         rate
#     }
# }
# """


# def fetch_work_sync(work_id: str) -> dict:
#     """
#     Fetch work data synchronously and normalize it.

#     :param work_id: ElCinema work ID
#     :return: Normalized dictionary
#     """
#     url = f"{BASE_URL}{work_id}/"

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = agentql.wrap(browser.new_page())
#         page.goto(url, timeout=60_000)

#         response = page.query_data(QUERY)
#         browser.close()

#     if "data" not in response:
#         raise ValueError("Invalid response from AgentQL")

#     return normalize_response(response["data"])


# """
# Synchronous scraper for ElCinema using AgentQL and Playwright.
# Fetches Arabic and English titles directly from AgentQL response and normalizes data.
# """

# import agentql
# from playwright.sync_api import sync_playwright
# from app.settings import AGENTQL_API_KEY, BASE_URL
# from app.normalizer import normalize_response

# # Configure AgentQL
# agentql.configure(api_key=AGENTQL_API_KEY)

# QUERY = """
# {
#     data{
#         title_arabic
#         title_english
#         img_url
#         trailer_url
#         plot

#         crew[]{
#             name
#             job
#         }

#         cast[]{
#             name
#             character
#         }

#         rate
#     }
# }
# """


# def fetch_work_sync(work_id: str) -> dict:
#     """
#     Fetch work data synchronously via AgentQL, normalize titles and all other fields.

#     :param work_id: ElCinema work ID
#     :return: Normalized dictionary
#     """
#     url = f"{BASE_URL}{work_id}/"

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = agentql.wrap(browser.new_page())
#         page.goto(url, timeout=60_000)

#         # Fetch data via AgentQL
#         response = page.query_data(QUERY)
#         browser.close()

#     data = response.get("data", {})

#     # Pass titles directly
#     data["title_ar"] = data.get("title_arabic")
#     data["title_en"] = data.get("title_english")

#     return normalize_response(data)

"""
Synchronous ElCinema scraper using AgentQL + Playwright.
Designed to be used safely inside FastAPI via run_in_threadpool.
"""

import agentql
from playwright.sync_api import sync_playwright
from app.settings import AGENTQL_API_KEY, BASE_URL
from app.normalizer import normalize_response

# Initialize AgentQL using API Key from .env
agentql.configure(api_key=AGENTQL_API_KEY)

QUERY = """
{
    data{
        title_arabic
        title_english
        img_url
        trailer_url
        plot

        crew[]{
            name
            job
        }

        cast[]{
            name
            character
        }

        production_year
        duration
        rate
    }
}
"""


def fetch_work_sync(work_id: str) -> dict:
    """
    Fetch movie/series data from ElCinema synchronously.

    :param work_id: ElCinema work ID
    :return: Normalized response dictionary
    """
    url = f"{BASE_URL}{work_id}/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = agentql.wrap(browser.new_page())
        page.goto(url, timeout=60_000)

        response = page.query_data(QUERY)
        browser.close()

    data = response.get("data", {})

    return normalize_response(data)
