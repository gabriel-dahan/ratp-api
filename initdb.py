from api import app, db
from api.models import RATP_Line

import json, requests


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        url = "https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/download/?format=json&timezone=Europe/Berlin&lang=fr"
        
        res = requests.get(url).text
        parsed_data = json.loads(res)
        
        conv = { "metro": "metro", "tram": "tramway", "funicular": "metro", "bus": "bus", "rail": "train" }

        for entry in parsed_data:
            fields = entry.get("fields", {})

            name = fields.get("name_line")
            id = fields.get("id_line")
            transport = conv[fields.get("transportmode")]
            groupname = fields.get("shortname_groupoflines")
            operatorname = fields.get("operatorname")
            networkname = fields.get("networkname")

            r = RATP_Line(id = id, type = transport, name = name, groupname = groupname, operatorname = operatorname, networkname = networkname)
            db.session.add(r)
        db.session.commit()