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
            color = '#0000ff'
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
            'text': f'*METAR for {station_id}*\n{raw_text}',
            'icon_url': 'https://aviationweather.gov/images/layout/noaa_logo.png',
            'attachments': [
                {
                    # 'pretext': raw_text,
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


def taf(airfield):
    """
    Build a TAF message
    :param airfield:
    :return:
    """
    params = {
        'stationString': airfield,
        'hoursBeforeNow': 1,
    }

    wc = Client(datasource='tafs', **params)
    wc.request()

    if wc.wxdata['data']['num_results'] > 0:
        wx = dict(wc.wxdata['data']['TAF'][0])

        station_id = airfield.upper()
        raw_text = wx['raw_text']
        issue_time = wx['issue_time'].strftime('%d%H%MZ')
        valid_from = wx['valid_time_from'].strftime('%d%H')
        valid_to = wx['valid_time_to'].strftime('%d%H')

        forecasts = []
        for f in wx['forecast']:
            forecast_from = f['fcst_time_from'].strftime('%d%HZ')
            forecast_to = f['fcst_time_to'].strftime('%d%HZ')
            ctype = f['change_indicator']
            time_becmg = f['time_becoming'].strftime('%d%HZ') if f['time_becoming'] is not None else None
            prob = f['probability']
            wind_direction = f['wind_dir_degrees']
            wind_speed = f['wind_speed_kt']
            wind_gust = f['wind_gust_kt']
            visibility = f['visibility_statute_mi']
            wx_string = str(f['wx_string'])
            skies = f['sky_condition']
            vert_vis = f['vert_vis_ft']

            # Wind builder
            if wind_direction is None:
                winds = 'No Change'
            elif wind_direction == 0 and wind_speed == 0:
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

            ceiling = None  # Pretty much only used for flight category determination
            if len(skies) > 1:
                skylist = []
                for x in skies:
                    cover = x['sky_cover']
                    cloud_alt = x['cloud_base_ft_agl'] if 'cloud_base_ft_agl' in x else None
                    skylist.append(f'{skd[cover]} at {cloud_alt}')

                    if ceiling is None and (cover == 'BKN' or cover == 'OVC'):
                        ceiling = cloud_alt

                sky = '\n'.join(skylist)
            else:
                cover = skies[0]['sky_cover']
                cloud_alt = skies[0]['cloud_base_ft_agl'] if 'cloud_base_ft_agl' in skies[0] else None

                if ceiling is None and (cover == 'BKN' or cover == 'OVC'):
                    ceiling = cloud_alt

                if vert_vis is not None:
                    sky = f'Vertical visibility of {vert_vis}'
                    ceiling = vert_vis
                elif cover == 'SKC':
                    sky = 'Clear'
                elif cover == 'CAVOK':
                    sky = 'Cloud and Visibility OK'
                elif cover == 'CLR':
                    sky = 'Clear under 12000'
                else:
                    sky = f'{skd[cover]} at {cloud_alt}'

            if ceiling is None:
                ceiling = 9999
            # End sky builder

            # Flight category
            if ceiling > 3000 and visibility > 5:
                flight_category = 'VFR'
                color = '#00ff00'
            elif 3000 > ceiling >= 1000 or 5 > visibility >= 3:
                flight_category = 'MVFR'
                color = '#0000ff'
            elif 1000 > ceiling >= 500 or 3 > visibility >= 1:
                flight_category = 'IFR'
                color = '#ff0000'
            else:
                flight_category = 'LIFR'
                color = '#b642f4'
            # End flight category

            # Cleanup stuff
            if ctype is None:
                ctype = 'N/A'
            elif ctype == 'BECMG':
                ctype = f'Becoming between {forecast_from} and {time_becmg}'
            elif ctype == 'PROB':
                ctype = f'PROB {prob}'

            if visibility > 6:
                visibility = '6+'

            fd = {
                'color': color,
                'fields': [
                    {
                        'title': 'Forecast From',
                        'value': forecast_from,
                        'short': True,
                    },
                    {
                        'title': 'Forecast To',
                        'value': forecast_to,
                        'short': True,
                    },
                    {
                        'title': 'Change Type',
                        'value': ctype,
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
                        'title': 'Flight Category',
                        'value': flight_category,
                        'short': True,
                    },
                ]
            }
            forecasts.append(fd)

        taf_msg = {
            'text': '\n'.join([
                f'*TAF for {station_id}*',
                f'{raw_text}\n*Issued:* {issue_time}',
                f'*Valid from:* {valid_from}',
                f'*Valid to:* {valid_to}',
            ]),
            'icon_url': 'https://aviationweather.gov/images/layout/noaa_logo.png',
            'attachments': forecasts
        }

        return taf_msg

    return {
        'text': f'No TAF results for {airfield.upper()}. Either not a valid station ID, TAFs aren\'t issued,  or some other error occurred.'
    }
