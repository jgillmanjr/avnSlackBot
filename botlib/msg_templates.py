metar_msg = """{{
    "text": "*METAR for {station_id}*",
    "attachments": [
        {{
            "pretext": "{raw_text}",
            "thumb_url": "https://aviationweather.gov/images/layout/noaa_logo.png",
            "color": "#0000ff",
            "fields": [
                {{
                    "title": "Observation Time",
                    "value": "{observation_time}",
                    "short": true
                }},
                {{
                    "title": "Flight Category",
                    "value": "{flight_category}",
                    "short": true
                }},
                {{
                    "title": "Winds From",
                    "value": "{wind_direction}°",
                    "short": true
                }},
                {{
                    "title": "Wind Speed",
                    "value": "{wind_speed} kts",
                    "short": true
                }},
                {{
                    "title": "Visibility",
                    "value": "{visibility}",
                    "short": true
                }},
                {{
                    "title": "Temp.",
                    "value": "{temp_c}° C",
                    "short": true
                }},
                {{
                    "title": "Dew Point",
                    "value": "{dewpoint_c}° C",
                    "short": true
                }}
            ]
        }}
    ]
}}"""