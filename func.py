from itertools import islice


def display_conversion(symbol_base, amount, currency, symbol_foreign, output, foreign):
    return f"""
    <div class="card  text-dark my-5 border-0">
    
    <div class="card-body">
          <div class="row">
      <div class="col"> <cite title="Source Title"></cite>
      <h5 class="text-dark" style="font-family: 'Encode Sans', sans-serif;font-size:50px;">{symbol_base} {"{:,.2f}".format(amount)} </h5>
        <figcaption class="blockquote-footer" style="font-size: 15px;"><cite title="Source Title"> {currency} </cite></figcaption>
    </div>
    <div class="col ml-5">
      <p class ="text-center mt-3" style="font:18px Rajdhani"><em>is currently<br/>Equivalent to</em></p>
    </div>
     <div class="col"> <cite title="Source Title"></cite>
      <h5 class="display-6  text-dark" style="font-family: 'Encode Sans', sans-serif;font-size:50px;">{symbol_foreign} {"{:,.2f}".format(output)} </h5>
        <figcaption class="blockquote-footer" style="font-size: 15px;"><cite title="Source Title"> {foreign} </cite></figcaption>
    </div>
  
  </div>

    </div>
    """


def header(first='', last=''):
    return f"""
    <div class="card text-center border-0" style="margin-top:-15vh">
      <div class="card-body">
      <span style="font:15px Thasadith;">A web app created by <a href ="https://www.linkedin.com/in/franklyn-achara-59b959162/" >  Achara Franklyn</a> </span>
         <p class="card-text my-3" style="font:40px Syncopate"><i class="bi bi-chevron-double-right"></i> <span style="color:{first}">Cash</span>&<span style="color:{last}">Coins</span>
          <i class="bi bi-chevron-double-left" style="font-size:30px; font-color:black;"></i></p>
          <p class="card-text" style="font:15px Quicksand">This is a simple yet powerful app built to  converts  Cryptocurrencies and 
          fiat currencies of most counties of the world and also provides  information on coins and trends on currency conversions</p>
          <p class="card-text" style = "font: 18px Rajdhani;word-spacing:20px">Simple | Reliable |  Efficient </p>
     
      </div>
    </div>
    <hr/>

    """


def display_country_details(map, open, country, flag, diction):
    keysList = [key for key in diction]
    questions = [diction[i] for i in diction]

    code = ""
    code += f"""
    <div class="badge bg-success m-3" style ="font-size:15px;"></div>
    <div>
    <img src={flag} alt="image here" class="mb-4 mx-3" style="width:15%;height:15%;" >
    <span class="h1"><strong> {country} </strong></span>
    <span class="badge bg-warning" style="border border-1"><a href={map} id='uniqueid' style ="font-size:15px;">Google map</a></span>
    <span class="badge bg-warning" style="border border-1" ><a href='{open}' id='uniqueid' style ="font-size:15px;">OpenSt</a></span>
   </div>

   <ul class="list-group list-group-flush ">"""
    for (key, value) in zip(keysList[:-6], questions[:-6]):
        code += f"""<li class="list-group-item bg-transparent p-2 list-group-item d-flex justify-content-between align-items-center text-muted">{key.capitalize()}
                <span ><strong>{value}</strong> </span></li>"""

    code += f"""</ul>"""
    return code


def show_crypto(amount, coin, symbol1, converted, symbol2, name, sign=""):

    return f"""
    <div class="container-fluid">
  <div class="row" >
    <div class="col"> <cite title="Source Title">{amount} {coin} ({symbol1}) is Equivalent to</cite>
      <h1 style="font-family: 'Encode Sans', sans-serif;font-size: 40px;letter-spacing: 2px;"><b>{sign}</b> {converted}</h1>
        <figcaption class="blockquote-footer" style="font-size: 15px;"><cite title="Source Title">{name} ({symbol2})</cite></figcaption>
    </div>
</div>
<div class="card-group">


"""


def show_list(ranking, image, coin, symbol, whitepaper, website, dict):
    keysList = [key for key in dict]
    questions = [dict[i] for i in dict]
    code = ""
    code += f"""
    <div class="badge bg-warning m-3" style ="font-size:15px;">Rank #{ranking}</div>
    <div>
    <img src={image} alt="image here" class="rounded-circle mb-4 mr-4" style="width:10%;height:10%;">
    <span class="h1"><strong> {coin} ({symbol})</strong></span>
   <span class="badge badge bg-warning" ><a href='{whitepaper}' id='uniqueid' style ="font-size:15px;">Website</a></span>
   <span class="badge badge bg-warning"><a href='{website}' id='uniqueid' style ="font-size:15px;">White Paper</a></span>
   </div>

   <ul class="list-group list-group-flush ">"""
    for (key, value) in zip(keysList[:8], questions[:8]):
        code += f"""<li class="list-group-item bg-transparent p-2 list-group-item d-flex justify-content-between align-items-center text-muted">{key.capitalize()}
                <span ><strong>{value}</strong> </span></li>"""

    code += f"""</ul>"""
    return code
