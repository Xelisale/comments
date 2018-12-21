## Description
    Programm download comments whis one site(vivino.com)
    
## Requirements
    Python => 3.7
   
## Install
##### Path of default /opt/
    cd /opt/
    git clone https://github.com/Xelisale/django.git api_comments
    cd api_comments/ 
    python3.7 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
##### If you need njinx configuration
    cp bin/api_comments_serv.conf /etc/njinx/site-avaliable/
    ln -s /etc/njinx/site-avaliable/api_comments_serv.conf /opt/etc/njinx/site-enable/api_comments_serv.conf
    njinx -t
    If all ok
    restart systemctl njinx
    
##### Add demon
    ln -s /opt/api_comments/bin/api_comments.service /etc/systemd/system/api_comments.service
    
## How use
#### Need give POST request
##### 1 Request, search for identical or similar wine
    Example:
        curl -H "Content-Type:application/json" -X POST -d '{"name":"Little Beauty Sauvignon Blanc Marlborough"}' http://mydomen.ru/api/names/find/
    Return:
        {"names":
            [[{"id":"1758778",
                   "image":"https://images.vivino.com/thumbs/SMbI_VdUTkKpqAc1n-Z76A_pl_375x500.png",
                   "name":"Sauvignon Blanc"}],
             [{"id":"1156374",
                   "image":"https://images.vivino.com/thumbs/JAzVu5MISKOJVWxiymtgvg_pl_375x500.png",
                   "name":"Black Edition Sauvignon Blanc"}]]}

##### 2 Request, getting comments by id
    Example:
        curl -H "Content-Type:application/json" -X POST -d '{"id":"1758778"}' http://mydomen.ru/api/names/find/id/
    Retern:
        {"comment":[
            {"Nick Rowan":
                {"image":
                    {"location":"//images.vivino.com/avatars/-EHlNZt5T1WBMvp7vRFe8A.jpg",
                     "variations":
                        {"large":"//thumbs.vivino.com/avatars/-EHlNZt5T1WBMvp7vRFe8A_300x300.jpg",
                         "small_square":"//thumbs.vivino.com/avatars/-EHlNZt5T1WBMvp7vRFe8A_50x50.jpg"}},
                 "note":"\u201dI come from a little known corner of the world called Marlborough \u201c states the back label. \n?!\nWhat person that has ever heard the word \u201cwine\u201d hasn\u2019t heard of \u201cMarlborough\u201d. Have they forgotten to change the back label text since the late 90s?\n\nInteresting peach and tropical note to the otherwise typical Sauvignon Blanc grapefruit and nettle. A \u201cfizz\u201d to the nose. \nServed a tad too warm, but the richness and complexity (yes, there is some) comes through. \nA lovely stone minerality streak runs through it>>>"}}]}
                    
