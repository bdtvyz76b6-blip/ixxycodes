import requests


VPN_URL = "https://orelvpnrailoh-production.up.railway.app/add-days"


def give_days(user_id, days):

    try:

        r = requests.post(
            VPN_URL,
            json={
                "user_id": user_id,
                "days": days
            },
            timeout=10
        )


        print(
            "VPN RESPONSE:",
            r.text
        )


        return r.json()


    except Exception as e:

        print(
            "VPN API ERROR:",
            e
        )

        return None