# """
# Normalization functions to convert raw AgentQL response into stable schema.
# """

# from typing import Dict, Any


# def normalize_elcinema(data: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Normalize raw elcinema AgentQL data into structured format.
#     """
#     directors, writers, scenarios = [], [], []

#     for person in data.get("crew", []):
#         job = person.get("job", "")
#         name = person.get("name", "")

#         if job == "مخرج":
#             directors.append(name)
#         elif job == "مؤلف":
#             writers.append(name)
#         elif job == "سيناريو":
#             scenarios.append(name)

#     actors = [
#         {
#             "name": actor.get("name"),
#             "character": actor.get("character") or ""
#         }
#         for actor in data.get("cast", [])
#     ]

#     return {
#         "title": data.get("title"),
#         "img_url": data.get("img_url"),
#         "trailer_url": data.get("trailer_url"),
#         "plot": data.get("plot"),
#         "rate": data.get("rate"),
#         "directors": directors,
#         "writers": writers,
#         "scenarios": scenarios,
#         "actors": actors,
#     }


# """
# Normalize AgentQL ElCinema response to a stable IPTV-friendly schema.
# """

# def normalize_response(data: dict) -> dict:
#     crew_map = {
#         "director": [],
#         "writer": [],
#         "scenario": []
#     }

#     for person in data.get("crew", []):
#         job = (person.get("job") or "").strip()
#         name = person.get("name")
#         if job == "مخرج":
#             crew_map["director"].append(name)
#         elif job == "مؤلف":
#             crew_map["writer"].append(name)
#         elif job == "سيناريو":
#             crew_map["scenario"].append(name)

#     cast = [
#         {
#             "name": actor.get("name"),
#             "character": actor.get("character")
#         }
#         for actor in data.get("cast", [])
#     ]

#     return {
#         "title": data.get("title"),
#         "poster": data.get("img_url"),
#         "trailer": data.get("trailer_url"),
#         "plot": data.get("plot"),
#         "rating": data.get("rate"),
#         "crew": crew_map,
#         "cast": cast
#     }

# def normalize_response(data: dict) -> dict:
#     """
#     Normalize raw AgentQL data and provide consistent structure
#     with Arabic and English titles.
#     """

#     # Crew mapping
#     crew_map = {
#         "director": [],
#         "writer": [],
#         "scenario": []
#     }
#     for person in data.get("crew", []):
#         job = (person.get("job") or "").strip()
#         name = person.get("name")
#         if job == "مخرج":
#             crew_map["director"].append(name)
#         elif job == "مؤلف":
#             crew_map["writer"].append(name)
#         elif job == "سيناريو":
#             crew_map["scenario"].append(name)

#     # Cast
#     cast = [
#         {
#             "name": actor.get("name"),
#             "character": actor.get("character")
#         }
#         for actor in data.get("cast", [])
#     ]

#     return {
#         "title_ar": data.get("title_ar"),    # Arabic title
#         "title_en": data.get("title_en"),    # English title
#         "poster": data.get("img_url"),
#         "trailer": data.get("trailer_url"),
#         "plot": data.get("plot"),
#         "rating": data.get("rate"),
#         "crew": crew_map,
#         "cast": cast
#     }


"""
Normalize AgentQL response into a unified IPTV-friendly schema.
"""


def normalize_response(data: dict) -> dict:
    """
    Normalize raw AgentQL data.

    Arabic title has priority.
    English title used only if Arabic is missing.
    """

    # Title priority: Arabic > English
    title_ar = data.get("title_arabic")
    title_en = data.get("title_english")

    final_title = title_ar or title_en

    # Normalize crew
    crew = {
        "director": [],
        "writer": [],
        "scenario": []
    }

    for person in data.get("crew", []):
        job = (person.get("job") or "").strip()
        name = person.get("name")

        if job == "مخرج":
            crew["director"].append(name)
        elif job == "مؤلف":
            crew["writer"].append(name)
        elif job == "سيناريو":
            crew["scenario"].append(name)

    # Normalize cast
    cast = [
        {
            "name": actor.get("name"),
            "character": actor.get("character")
        }
        for actor in data.get("cast", [])
    ]

    return {
        # Titles
        "title": final_title,
        "title_ar": title_ar,
        "title_en": title_en,

        # Media
        "poster": data.get("img_url"),
        "trailer": data.get("trailer_url"),

        # Content
        "plot": data.get("plot"),
        "production_year": data.get("production_year"),
        "duration": data.get("duration"),
        "rating": data.get("rate"),

        # People
        "crew": crew,
        "cast": cast
    }
