
import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import date, datetime
from streamlit_option_menu import option_menu
import validators
from func import *
import os
from dotenv import load_dotenv


st.set_page_config(
    layout="wide", initial_sidebar_state="expanded", page_icon=':moneybag:')
os.environ["API_KEY"] == st.secrets["API_KEY"]
api_key = os.environ["API_KEY"]
# api_key = "75a59256-92a1-4fd2-af79-9592946e0458"
# setting the page layout


# styling the page layout
# with open('style.css') as f:
#     st.markdown(f'<style>[f.read()]</style>', unsafe_allow_html=True)
hide_things = """
<style>
#MainMenu { visibility: hidden;}
footer { visibility:hidden;}
header { visibility:hidden;}
</style>
"""
st.markdown(hide_things, unsafe_allow_html=True)
st.markdown("""<meta charset="utf-8">""", unsafe_allow_html=True)
st.markdown("""<meta name="viewport" content="width=device-width, initial-scale=1">""",
            unsafe_allow_html=True)
st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
 integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">""", unsafe_allow_html=True)

st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.3/font/bootstrap-icons.css">""", unsafe_allow_html=True)
st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Encode+Sans:wght@100;122&family=Rajdhani&family=Thasadith&family=Quicksand:wght@300&family=Work+Sans:wght@100&family=Josefin+Slab:wght@100&family=Syncopate:wght@700&display=swap" rel="stylesheet">""",
            unsafe_allow_html=True)


# function for fiat currencies

@ st.cache
def currency():
    # API for symbols of currencies
    response = requests.get('https://api.exchangerate.host/symbols').json()
    # setting a list
    lister = []
    # iterating through json to append on the list
    for value in response['symbols'].items():
        lister.append(value[1]["description"]+" (" + value[0] + ")")

    return lister


# A function that takes currency  abbreviating to give details about the country
# st.write(currency())
@ st.cache
def country(code):

    # API for country details
    url1 = 'https://restcountries.com/v3.1/currency/'
    url2 = 'https://restcountries.com/v2/currency/'

    if code:  # checking if the currency abbrev is valid
        respone2 = requests.get(url2+code).json()
        respone1 = requests.get(url1+code).json()
        if code == 'USD':  # ensuring we return the real united states
            position = respone2[-1]
        else:
            position = respone2[0]
        # since Europe is not a country give details about europe seperately
        if code == 'EUR':
            my_dict = {
                'capital': 'Brussels, EU HQ', 'languages': 'Russian,German , French, Italian...', 'population': '746,419,440', 'Geolocation(latlng)': "15.2551 / 54.5260",
                'code': 'EUR', 'callingCodes': '+39 , +43 , +33 ....', 'subregion': 'None', 'region': 'Continent', 'demonym': 'European', 'symbol': '€',
                'flags': ' https://flagcdn.com/w320/eu.png', 'Country': 'Europe (continent)',
                'googlemaps': 'https://www.google.com/maps/d/u/0/embed?mid=1dKqPU-1jlWv8owKZtUTi7Cp-L20&ie=UTF8&hl=en&msa=0&ll=49.72447900000002%2C19.511719000000017&spn=27.402756%2C79.013672&z=4&output=embed',
                'openStreetMaps': 'https://www.openstreetmap.org/relation/2668952'}
        else:  # append country details
            my_dict = {
                'capital': position['capital'], 'languages': position['languages'][0]['name'], 'population': "{:,}".format(position['population']), 'Geolocation(latlng)': " ".join([str(position['latlng'][0]), ',', str(position['latlng'][1])]),
                'callingCodes': '+' + position['callingCodes'][0], 'subregion': position['subregion'],
                'code': position['currencies'][0]['code'],  'region': position['region'], 'demonym': position['demonym'], 'symbol': position['currencies'][0]['symbol'],
                'flags': position['flags']['png'], 'Country': position['name'], 'googlemaps': respone1[0]['maps']['googleMaps'], 'openStreetMaps': respone1[0]['maps']['openStreetMaps']}
    return my_dict  # return dataframe

# function to round of value of currencies


def rounding(num, den, factor):
    input = (num/den) * factor
    if input > 1:  # if is greater than zero give it 2 decimal places
        return "{:,.2f}".format(input)
    else:  # if is less than zero give it 8 decimal places
        return "{:.8f}".format(input)


# get fiat currency and convert it
def converter(base, foreign, date, amount):
    # API to convert fiat currencies
    url = f'https://api.exchangerate.host/convert?from={base}&to={foreign}&places=2&{date}'

    response = requests.get(url)
    if response.status_code != 200:
        return st.error(f'Cant display any Charts on {base} ')
    else:
        response = requests.get(url).json()
    #  if the base is less than foreign currency and flip it since API supprts conversion rates greater than 1
        if float(response['info']['rate']) > 1:
            # return conersion rate and multiply by the input ammount by the user
            return float(response['info']['rate']) * amount
        else:
            # flip the base currency to be foreign currency and foreing to be base currency
            url = f'https://api.exchangerate.host/convert?from={foreign}&to={base}&places=2&{date}'
            response = requests.get(url).json()
            # get the reciprocal to get the conversion rates
            return (1/float(response['info']['rate'])) * amount


def slider():
    year = st.slider('Chose the Period ?', 2006,  2022, 2021)
    return year


@ st.cache
def fiat_trend(year, base, foreign, amount, sign, baser, foreigner):

    url = f'https://api.exchangerate.host/convert?from={base}&to={foreign}&places=2&date={year}'
    response1 = requests.get(url)
    if response1.status_code != 200:
        return st.error(f'Cant display any Charts on {base} ')
        st.stop()
    else:
        df = pd.DataFrame(columns=['Date', 'Rate'])
        for i in range(2006, int(year+1), 1):
            if i == 2022:
                years = '2022-'+str(date.today())[5:]
            else:
                years = str(i) + '-12-31'
            url = f'https://api.exchangerate.host/convert?from={base}&to={foreign}&places=2&date={years}'
            # if  response.status_code != 200:

            response = requests.get(url).json()
            to_append = [years, response['info']['rate']]
            df_length = len(df)
            df.loc[df_length] = to_append

            # df = df.concat(
            #     {"Date": years, 'Rate': response['info']['rate']}, ignore_index=True)

        df['year'] = pd.DatetimeIndex(df['Date']).year.astype('str')
        # df['Rate'] = df['Rate'] * amount
        # df['Rate'] = (df['Rate'] * amount).apply(lambda x: '[:,.2f]'.format(x))
        fig = go.Figure()
        # Area chart for total population from 1955 to 2020
        fig.add_trace(go.Scatter(x=df['year'],
                                 y=df['Rate'],
                                 fill='tozeroy',  # fill down to xaxis
                                 fillcolor='orange',
                                 text=(
                                     df['Rate'] * amount).apply(lambda x: '{sign}{:,.2f}'.format(x, sign=sign)),
                                 mode="lines+markers+text",
                                 line={
            'dash': 'solid', 'color': 'orange'},
            textfont_size=14
        ))
        fig.update_traces(textposition='top center')
        # fig.update_traces(texttemplate=df['Rate']
        #                   # textposition='auto'
        #                   )

        # fig.update_layout(yaxis_tickformat=f"{sign}")
        # fig.update_trace(textposition='outside', textfont_size=14)
        # fig = go.Figure([go.Bar(x=df['year'], y=df['Rate'], text=sign + df['Rate'],
        # textposition="outside", marker=dict(color='#F58680'))])
        fig.update_xaxes(nticks=df.shape[0] * 2)
        fig.update_layout(
            # title_text=f'<b>[coin.capitalize()] Last [days] days</b>', title_x=0.5,
            title_text=f'Curency  Yearly Conversion Trend <br>The history  of equivalence of {amount} {baser}  to {foreigner} (2006 - {year})<br>', title_x=0.5,
            margin=dict(l=5, r=5, b=10, t=35),
            width=1200,
            height=350,
            # mode="markers+text",

            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig

# the fiat currencies Page


def fx_exchange():

    cole1, cole2, cole3 = st.columns([1, 4, 1])
    with cole2:
        st.markdown(header(first='#FFB449'), unsafe_allow_html=True)

    # Setting up the sidebar
    with st.sidebar:
        # input box for the amount up the sidebar
        '---'
        st.sidebar.header("Converting Fiat Currencies")
        spacer(st, 1)
        amount = st.number_input(
            f'Enter the Amount you want to convert', min_value=0.00, format="%.2f", value=1.00)
        # drop down for base fiat
        base_fiat = st.selectbox(
            'Select the Domain Currency',
            options=currency())
        # drop down for foreign fiat
        foreign_fiat = st.selectbox(
            'Select the Currency you want to convert to',
            # the currency list drop down must not contain what is currently selected on the base fiat
            options=[x for x in currency() if x != base_fiat]
        )
     # Setting up the page header

    mydate = datetime.today().strftime('%Y-%m-%d')
    base_dict = country(base_fiat[-4:-1])
    foreign_dict = country(foreign_fiat[-4:-1])

    st.markdown(display_conversion(base_dict['symbol'], amount, base_fiat, foreign_dict['symbol'],
                                   converter(base_fiat[-4:-1], foreign_fiat[-4:-1], mydate, amount), foreign_fiat), unsafe_allow_html=True)
    col1,  col2 = st.columns([3, 3])
    with col1:
        st.markdown(display_country_details(
            base_dict['googlemaps'], base_dict['openStreetMaps'], base_dict['Country'], base_dict['flags'], base_dict), unsafe_allow_html=True)
    with col2:
        st.markdown(display_country_details(
            foreign_dict['googlemaps'], foreign_dict['openStreetMaps'], foreign_dict['Country'], foreign_dict['flags'], foreign_dict), unsafe_allow_html=True)
    spacermain(st, 2)
    kol1,  kol2, kol3 = st.columns([0.5, 4, 0.5])
    with kol2:
        conversion_year = st.slider(
            'Select year of conversion', 2006, int(date.today().year), 2020, 1)
        # display fiat_trend charts
        # st.write(fiat_trend(conversion_year, foreign_dict,
        #                     base_fiat, amount, base_fiat.iloc[0]['symbol'], base_fiat, foreign_fiat[-4:-1]))

        st.write(fiat_trend(conversion_year,
                 base_fiat[-4:-1], foreign_fiat[-4:-1], amount, foreign_dict['symbol'], base_fiat, foreign_fiat))


def spacer(order, number):
    for i in range(number):
        order.sidebar.markdown(
            '<br/>', unsafe_allow_html=True)


######################################################################################################################################################################
@ st.cache
def coin_name():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '2000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    json = requests.get(url, params=parameters, headers=headers).json()
    df_coin = pd.DataFrame(columns=['symbol', 'name', 'dollar'])
    for i in json['data']:
        to_append = [i['symbol'], i['name'], i['quote']['USD']['price']]
        df_length = len(df_coin)
        df_coin.loc[df_length] = to_append
    return df_coin


def crypto_charts(coin,  days, key):
    spacermain(st, 2)
    radio = st.radio(label=' ', options=[
        '1d', '7d', '30d', '90d', '180d', '365d'], key={key}, horizontal=True)
    if radio == '1d':
        days = 1
    elif radio == '7d':
        days = 7
    elif radio == '30d':
        days = 30
    elif radio == '90d':
        days = 90
    elif radio == '180d':
        days = 180
    elif radio == '365d':
        days = 365

    url = 'https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency=usd&days={days}'.format(
        coin=coin.lower(), days=str(days))

    response = requests.get(url)
    valid = validators.url(url)

    if valid != True or response.status_code != 200:
        st.error(f'Cant display any Charts on {coin} ')
        st.stop()

    else:

        dft = pd.read_json(url)
        dft.columns = ['Time', 'Open', 'High', 'Low', 'Close']
        dft['Date'] = pd.to_datetime(dft['Time']/1000, unit='s')
        dft.drop(['Time'], axis=1, inplace=True)


# Plotting Charts
    fig = go.Figure(data=[go.Candlestick(x=dft['Date'],
                                         open=dft['Open'],
                                         high=dft['High'],
                                         low=dft['Low'],
                                         close=dft['Close'])],
                    )

    fig.update_layout(
        title_text=f'<b>{coin.capitalize()} Last {days} days</b>', title_x=0.5,
        margin=dict(l=5, r=5, b=10, t=35),
        height=350,
        width=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'


    )

    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#FFB449', mirror=True, showgrid=True)

    st.write(fig)


def spacermain(order, number):
    for i in range(number):
        order.markdown(
            '<br/>', unsafe_allow_html=True)


# Function to get coind etails


def collectibles(symbol):

    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    url2 = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'

    parameters = {
        'symbol': symbol
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    json = requests.get(url, params=parameters, headers=headers).json()
    json2 = requests.get(url2, params=parameters, headers=headers).json()

    # dictinary to get the items
    main_items = {

        "Date added": json['data'][symbol][0]['date_added'][:10],
        "Price": "${:,.2f}".format(json['data'][symbol][0]['quote']['USD']['price']),
        "Maximum Supply": json['data'][symbol][0]['max_supply'],

        "Number of Market Pairs": json['data'][symbol][0]['num_market_pairs'],

        "Circulating Supply": "{:,.2f}".format(
            json['data'][symbol][0]['circulating_supply']),

        "Market Captalization": "${:,.2f}".format(
            json['data'][symbol][0]['quote']['USD']['market_cap']),

        "Volume change in 24h": json['data'][symbol][0]['quote']
        ['USD']['volume_change_24h'],
        "Market Cap Dominance": "${:,.2f}".format(json['data'][symbol][0]['quote']
                                                  ['USD']['market_cap_dominance']),
        "Ranking": json['data'][symbol][0]['cmc_rank'],
        "coin_name": json2['data'][symbol][0]['name'],
        "coin_symbol": json2['data'][symbol][0]['symbol']
    }

    try:
        main_items['technical_doc'] = json2['data'][symbol][0]['urls']['technical_doc'][0]
        main_items['image'] = json2['data'][symbol][0]['logo']
        main_items['website'] = json2['data'][symbol][0]['urls']['website'][0]
    except IndexError:
        main_items['technical_doc'] = ''
        main_items['image'] = ''
        main_items['website'] = ''

    # Return the dictionary

    return main_items

# display crypto page


def crypto_page():
    cole1, cole2, cole3 = st.columns([1, 4, 1])
    with cole2:
        st.markdown(header(last='#FFB449'), unsafe_allow_html=True)
    # calling the  coin_name function to give the dropdown
    df_coin = coin_name()

    st.sidebar.markdown(
        '<hr/>', unsafe_allow_html=True)
    st.sidebar.header("Converting Cryptocurrencies")

    # amount of crypto to exchange
    amountcrypto = st.sidebar.number_input(
        f'Enter the Amount you want to convert', min_value=0.00, format="%.2f", value=1.00)

    # drop down list for base coin
    base_coin = st.sidebar.selectbox(
        'Base Coin?',
        options=df_coin["symbol"])

    # drop down list for foreign coin
    foreign_coin = st.sidebar.selectbox(
        'The Coin you want to convert to?',
        options=[x for x in df_coin["symbol"] if x not in [base_coin, 'BTC']])

    # drop down list for fiat currency
    currency_convert = st.sidebar.selectbox(
        'Choose the Currency Name?', currency())

    filter_base = df_coin[df_coin.symbol == base_coin]
    filter_foreign = df_coin[df_coin.symbol == foreign_coin]
    filter_BTC = df_coin[df_coin.symbol == 'BTC']
    try:
        currency_code_ = currency_convert[-4:-1]
    except IndexError:
        currency_code_ = ''

    value = rounding(filter_base.iloc[0]['dollar'],
                     filter_foreign.iloc[0]['dollar'], amountcrypto)
    btc_value = rounding(
        filter_BTC.iloc[0]['dollar'], filter_base.iloc[0]['dollar'], amountcrypto)
    currency_value = converter('USD', currency_code_, datetime.today().strftime(
        '%Y-%m-%d'), filter_base.iloc[0]['dollar'])
    # st.write(currency_code_)
    spacermain(st, 2)

    # Display KPIs show_crypto
    xol1, xol2, xol3 = st.columns(3)
    with xol1:
        # show_crypto(amount, coin, converted, symbol, name)
        st.markdown(show_crypto(amountcrypto, filter_base.iloc[0]['name'], filter_base.iloc[0]['symbol'], value,
                    filter_foreign.iloc[0]['symbol'], filter_foreign.iloc[0]['name']), unsafe_allow_html=True)
    with xol2:
        st.markdown(show_crypto(amountcrypto, filter_base.iloc[0]['name'], filter_base.iloc[0]['symbol'], btc_value,
                    filter_BTC.iloc[0]['symbol'], filter_BTC.iloc[0]['name']), unsafe_allow_html=True)

    with xol3:
        st.markdown(show_crypto(amountcrypto, filter_base.iloc[0]['name'], filter_base.iloc[0]['symbol'], "{:,.2f}".format(currency_value),
                    currency_convert[-4:-1], currency_convert[:-5], country(currency_code_)['symbol']), unsafe_allow_html=True)

    spacermain(st, 1)
    colet1, colet2 = st.columns(2)

    base_dict = collectibles(base_coin)
    foreign_dict = collectibles(foreign_coin)

    with colet1:
        st.markdown(show_list(base_dict['Ranking'], base_dict['image'], base_dict['coin_name'], base_dict['coin_symbol'], base_dict['technical_doc'], base_dict['website'],
                              base_dict), unsafe_allow_html=True)
    with colet2:
        st.markdown(show_list(foreign_dict['Ranking'], foreign_dict['image'], foreign_dict['coin_name'], foreign_dict['coin_symbol'], foreign_dict['technical_doc'], foreign_dict['website'],
                              foreign_dict), unsafe_allow_html=True)

    kola1, kola2 = st.columns(2)
    with kola1:
        crypto_charts(base_dict['coin_name'].lower(), 0, 'base')

    with kola2:
        crypto_charts(foreign_dict['coin_name'].lower(), 0, 'foreign')


def navbar():
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=['Cryptocurrency', 'Fiat Currency'],
            icons=['currency-bitcoin', 'cash-coin'],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"background-color": "#F4F4F4", "width": "inherit"},
                "icon": {"color": "red", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#FFB449"},
            }
        )
    if selected == "Fiat Currency":
        fx_exchange()

    else:
        crypto_page()


navbar()
