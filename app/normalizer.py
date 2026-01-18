# """
# Normalize AgentQL response into a unified IPTV-friendly schema.
# """


# def normalize_response(data: dict) -> dict:
#     """
#     Normalize raw AgentQL data.

#     Arabic title has priority.
#     English title used only if Arabic is missing.
#     """

#     # Title priority: Arabic > English
#     title_ar = data.get("title_arabic")
#     title_en = data.get("title_english")

#     final_title = title_ar or title_en

#     # Normalize crew
#     crew = {
#         "director": [],
#         "writer": [],
#         "scenario": []
#     }

#     for person in data.get("crew", []):
#         job = (person.get("job") or "").strip()
#         name = person.get("name")

#         if job == "مخرج":
#             crew["director"].append(name)
#         elif job == "مؤلف":
#             crew["writer"].append(name)
#         elif job == "سيناريو":
#             crew["scenario"].append(name)

#     # Normalize cast
#     cast = [
#         {
#             "name": actor.get("name"),
#             "character": actor.get("character")
#         }
#         for actor in data.get("cast", [])
#     ]

#     return {
#         # Titles
#         "title": final_title,
#         "title_ar": title_ar,
#         "title_en": title_en,

#         # Media
#         "poster": data.get("img_url"),
#         "trailer": data.get("trailer_url"),

#         # Content
#         "plot": data.get("plot"),
#         "production_year": data.get("production_year"),
#         "duration": data.get("duration"),
#         "rating": data.get("rate"),

#         # People
#         "crew": crew,
#         "cast": cast
#     }

"""
Normalize AgentQL ElCinema response into a unified IPTV-friendly schema.
"""


def normalize_response(data: dict, elcinema_id: str) -> dict:
    """
    Normalize raw AgentQL data.

    Rules:
    - Arabic title has priority
    - English title used only if Arabic is missing
    - Output matches IPTV panel input fields
    """

    # Title priority
    title_ar = data.get("title_arabic")
    title_en = data.get("title_english")
    title = title_ar or title_en

    # Crew normalization
    director = None
    writers = []

    for person in data.get("crew", []):
        job = (person.get("job") or "").strip()
        name = person.get("name")

        if job == "مخرج" and not director:
            director = name
        elif job == "مؤلف":
            writers.append(name)

    # Cast normalization (names only – input friendly)
    cast_names = [actor.get("name") for actor in data.get("cast", []) if actor.get("name")]

    return {
        # IDs
        "elcinamdotcom_id": elcinema_id,

        # Titles
        "title": title,
        "title_arabic": title_ar,
        "title_english": title_en,

        # Images
        "poster_url": data.get("poster_url"),
        "backdrop_url": data.get("backdrop_url"),

        # Content
        "plot": data.get("plot"),
        "genres": data.get("genres"),
        "release_date": data.get("release_date"),
        "runtime": data.get("runtime") or data.get("duration"),
        "production_year": data.get("production_year"),
        "rating": data.get("rate"),

        # Media
        "trailer_url": data.get("trailer_url"),

        # People
        "cast": cast_names,
        "director": director,
        "writers": writers,

        # Extra
        "country": data.get("country")
    }
