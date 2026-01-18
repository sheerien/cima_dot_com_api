# """
# Synchronous ElCinema scraper using AgentQL + Playwright.
# Designed to be used safely inside FastAPI via run_in_threadpool.
# """

# import agentql
# from playwright.sync_api import sync_playwright
# from app.settings import AGENTQL_API_KEY, BASE_URL
# from app.normalizer import normalize_response

# # Initialize AgentQL using API Key from .env
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

#         production_year
#         duration
#         rate
#     }
# }
# """


# def fetch_work_sync(work_id: str) -> dict:
#     """
#     Fetch movie/series data from ElCinema synchronously.

#     :param work_id: ElCinema work ID
#     :return: Normalized response dictionary
#     """
#     url = f"{BASE_URL}{work_id}/"

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = agentql.wrap(browser.new_page())
#         page.goto(url, timeout=60_000)

#         response = page.query_data(QUERY)
#         browser.close()

#     data = response.get("data", {})

#     return normalize_response(data)

"""
Synchronous ElCinema scraper using AgentQL + Playwright.
Safe to be used inside FastAPI via run_in_threadpool.
"""

import agentql
from playwright.sync_api import sync_playwright

from app.settings import AGENTQL_API_KEY, BASE_URL
from app.normalizer import normalize_response

# Initialize AgentQL using API key from .env
agentql.configure(api_key=AGENTQL_API_KEY)

# AgentQL query aligned with UI inputs & IPTV needs
QUERY = """
{
    data {
        title_arabic
        title_english

        poster_url
        backdrop_url

        plot

        cast[] {
            name
        }

        crew[] {
            name
            job
        }

        genres
        release_date
        runtime
        trailer_url
        rate
        country

        production_year
        duration
    }
}
"""


def fetch_work_sync(work_id: str) -> dict:
    """
    Fetch movie/series metadata from ElCinema synchronously.

    :param work_id: ElCinema work ID
    :return: Normalized IPTV-friendly response
    """
    url = f"{BASE_URL}{work_id}/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = agentql.wrap(browser.new_page())

        page.goto(url, timeout=60_000)

        response = page.query_data(QUERY)

        browser.close()

    data = response.get("data", {}) if response else {}

    # Pass work_id explicitly to normalizer
    return normalize_response(data, elcinema_id=work_id)
