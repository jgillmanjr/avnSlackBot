from addsPy import Client
from decimal import Decimal


def metar(airfield):
    """
    Build a METAR message
    :param airfield:
    :return: A dictionary
    """
    params = {
        'stationString': airfield,
        'hoursBeforeNow': 1,
    }

    wc = Client(datasource='metars', **params)
    wc.request()

    if wc.wxdata['data']['num_results'] > 0:
        wx = dict(wc.wxdata['data']['METAR'][0])

        station_id = airfield.upper()
        raw_text = wx['raw_text']
        observation_time = wx['observation_time'].strftime('%H%MZ')
        flight_category = wx['flight_category']
        wind_direction = wx['wind_dir_degrees']
        wind_speed = wx['wind_speed_kt']
        wind_gust = wx['wind_gust_kt']
        visibility = wx['visibility_statute_mi']
        wx_string = str(wx['wx_string'])
        skies = wx['sky_condition']
        vert_vis = wx['vert_vis_ft']
        temp_c = wx['temp_c']
        dewpoint_c = wx['dewpoint_c']
        altim = wx['altim_in_hg']
        elevation_ft = wx['elevation_m'] * Decimal('3.28084')

        # Flight category color
        if flight_category == 'VFR':
            color = '#00ff00'
        elif flight_category == 'MVFR':
            color = '#0000ff',
        elif flight_category == 'IFR':
            color = '#ff0000'
        else:
            color = '#b642f4'
        # End flight category color

        # Wind builder
        if wind_direction == 0 and wind_speed == 0:
            winds = 'Calm'
        elif wind_direction == 0:
            winds = f'Variable at {wind_speed}'
        else:
            if wind_direction < 100:
                wind_direction = f'0{wind_direction}'
            winds = f'{wind_direction} at {wind_speed}'

        if wind_gust is not None:
            winds += f' gusting {wind_gust}'
        # End wind builder

        # Sky builder
        skd = {
            'FEW': 'Few',
            'SCT': 'Scattered',
            'BKN': 'Broken',
            'OVC': 'Overcast'
        }

        if len(skies) > 1:
            skylist = []
            for x in skies:
                cover = x['sky_cover']
                cloud_alt = x['cloud_base_ft_agl'] if 'cloud_base_ft_agl' in x else None
                skylist.append(f'{skd[cover]} at {cloud_alt}')

            sky = '\n'.join(skylist)
        else:
            cover = skies[0]['sky_cover']
            cloud_alt = skies[0]['cloud_base_ft_agl'] if 'cloud_base_ft_agl' in skies[0] else None
            if vert_vis is not None:
                sky = f'Vertical visibility of {vert_vis}'
            elif cover == 'SKC':
                sky = 'Clear'
            elif cover == 'CAVOK':
                sky = 'Cloud and Visibility OK'
            elif cover == 'CLR':
                sky = 'Clear under 12000'
            else:
                sky = f'{skd[cover]} at {cloud_alt}'
        # End sky builder

        metar_msg = {
            'text': f'METAR for {station_id}',
            'icon_url': 'https://aviationweather.gov/images/layout/noaa_logo.png',
            'attachments': [
                {
                    'pretext': raw_text,
                    # 'thumb_url': 'https://aviationweather.gov/images/layout/noaa_logo.png',
                    'color': color,
                    'fields': [
                        {
                            'title': 'Observation Time',
                            'value': observation_time,
                            'short': True,
                        },
                        {
                            'title': 'Flight Category',
                            'value': flight_category,
                            'short': True,
                        },
                        {
                            'title': 'Winds',
                            'value': winds,
                            'short': True,
                        },
                        {
                            'title': 'Visibility',
                            'value': f'{visibility} SM',
                            'short': True,
                        },
                        {
                            'title': 'Wx',
                            'value': wx_string,
                            'short': True,
                        },
                        {
                            'title': 'Sky Conditions',
                            'value': sky,
                            'short': True,
                        },
                        {
                            'title': 'Temp (°c)',
                            'value': str(temp_c),
                            'short': True,
                        },
                        {
                            'title': 'Dewpoint (°c)',
                            'value': str(dewpoint_c),
                            'short': True,
                        },
                        {
                            'title': 'Altimeter',
                            'value': str(round(altim, 2)),
                            'short': True,
                        },
                        {
                            'title': 'Field Elevation',
                            'value': str(round(elevation_ft, 0)),
                            'short': True,
                        },
                    ]
                }
            ]
        }

        return metar_msg

    return {
        'text': f'No METAR results for {airfield.upper()}. Either not a valid station ID or some other error occurred.'
    }
