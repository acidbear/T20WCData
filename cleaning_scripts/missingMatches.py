from bs4 import BeautifulSoup
import requests
import pandas as pd

URLS = ["https://www.espncricinfo.com/series/women-s-world-t20-2013-14-628373/pakistan-women-vs-south-africa-women-2nd-match-group-a-682969/full-scorecard",
        "https://www.espncricinfo.com/series/women-s-world-t20-2013-14-628373/australia-women-vs-south-africa-women-6th-match-group-a-682977/full-scorecard",
        "https://www.espncricinfo.com/series/women-s-world-t20-2013-14-628373/australia-women-vs-ireland-women-9th-match-group-a-682983/full-scorecard",
        "https://www.espncricinfo.com/series/women-s-world-t20-2013-14-628373/bangladesh-women-vs-england-women-11th-match-group-b-682987/full-scorecard"]

for url in URLS :
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    wickets = soup.find_all("td", class_="ds-w-0 ds-whitespace-nowrap ds-text-right")
    namesW = soup.find_all("td",class_="ds-flex ds-items-center")

    runs = soup.find_all("td",class_="ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-typo")
    namesR = soup.find_all("td",{"class" : ["ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-flex ds-items-center",
                                    "ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-flex ds-items-center ds-border-line-primary ci-scorecard-player-notout"]})
    
    # for name, wicket in zip(namesW,wickets):
    #     print(name.text,wicket.text)

    # for name, run in zip(namesR,runs):
    #     print(name.text,run.text)


wicket_additions_dict = {
    "player" : ["Asmavia Iqbal","Sumaiya Siddiqi","Sana Mir","Anam Amin",
                "Qanita Jalil","Nida Dar","S Ismail","CL Tryon","S Loubser","M Kapp",
                "MM Letsoalo", "D van Niekerk", "S Luus","RM Farrell","JL Jonassen",
                "SJ Coyte","EA Perry","EA Osborne","JL Hunter","S Ismail","CL Tryon",
                "S Loubser","M Kapp","D van Niekerk","S Luus","IMHC Joyce","LN McCarthy",
                "EAJ Richardson","LK O'Reilly","EJ Tice","L Delany","HL Ferling","JL Jonassen",
                "SJ Coyte","JL Hunter","EA Perry","EA Osborne","Salma Khatun","Jahanara Alam",
                "Rumana Ahmed","Fahima Khatun","Khadija Tul Kubra","Lata Mondal","A Shrubshole",
                "D Hazell","RL Grundy","NR Sciver-Brunt","JL Gunn","GA Elwiss"],

    "wickets" : [0,0,0,0,0,0,2,0,1,3,0,0,2,2,1,0,0,2,
                 2,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,0,2,2,2,
                 0,1,0,2,0,2,3,0,3,0,0]
}

run_additions_dict = {
    "player" : ["L Lee","D van Niekerk","Nain Abidi","Qunita Jalil","Javeria Khan","Nida Dar",
                "Bismah Marrof","Sana Mir","Nahida Khan","Asmavia Iqbal","Batool Fatima","Sumaiya Siddiqi",
                "Anam Amin","L Lee","D van Niekerk","T Chetty","M du Preez","M Kapp",
                "Y van der Westhuizen","CL Tryon","S Ismail","S Loubser","S Luus","MM Letsoalo",
                "DM Kimmince","AJ Healy","MM Lanning","AJ Blackwell","EA Perry","DM Kimmince","AJ Healy",
                "MM Lanning","AJ Blackwell","CMA Shillington","ELC Flanagan","IMHC Joyce",
                "MEMO Scott-Hayward","CNIM Joyce","EJ Tice","EAJ Richardson","LN McCarthy",
                "MV Waldorn","CM Edwards","SJ Taylor","TT Beaumont","LS Greenway","NR Sciver-Brunt",
                "HC Knight","JL Gunn","Ayasha Rahman","Shamima Sultana","Salma Khatun","Fargana Hoque",
                "Rumana Ahmed","Lata Mondal","Nuzhat Tasnia","Sanjida Islam","Jahanara Alam",
                "Fahima Khatun","Khadija Tul Kubra"],


    "runs" : [67,90,28,6,11,32,15,3,10,1,6,2,0,0,
              12,30,14,20,0,3,13,1,19,0,17,0,6,24,41,35,9,126,12,
              22,0,28,11,11,19,6,0,4,80,7,2,3,20,18,0,10,1,3,1,1,10,5,5,2,16,1]
}

WICKET_ADDITIONS = pd.DataFrame.from_dict(wicket_additions_dict)
RUN_ADDITIONS = pd.DataFrame.from_dict(run_additions_dict)

# WICKET_ADDITIONS.to_csv(path_or_buf="WICKET_ADDITIONS.csv",index=False)
# RUN_ADDITIONS.to_csv(path_or_buf="RUN_ADDITIONS.csv",index=False)