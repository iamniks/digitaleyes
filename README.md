# DigitalEyes - Monitor

## Installation :

    pip install -r requirements.txt

## Configuration  :

**Edit : *config.json***

Exemple :
```
    "base_link": "https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?price=asc&collection=",
    "collections": [
        {
            "collection": "The Sneks",
            "price": 1
        },
        {
            "collection": "ShroomZ",
            "price": 1
        }
    ],
    "webhooks": [
        {
            "name": "<name>",
            "url": "<url>"
        },
        {
            "name": "<name>",
            "url": "<url>"
        }
    ],
    "avatar_url": "https://pbs.twimg.com/profile_images/1430306224713740292/q4termyJ_400x400.jpg",
    "footer_name": "<footer_name>",
    "footer_image_url": "<footer_image_url>"
```

You can find collection name at the end of : https://digitaleyes.market/collections/ShroomZ

#### Warning !

At the end of the last "}" do not put a "," !

Exemple :

```
{
    "collections": [
        {
            "collection": "<collection>",
            "price": 1,
            "webhooks": [
                {
                    "name": "<name>",
                    "url": "<url>",
                    "footer_name": "<footer_name>",
                    "footer_image_url": "<footer_image_url>"
                } !!!
            ]
        } !!!
    ],
    "avatar_url": "https://pbs.twimg.com/profile_images/1434909426838814727/b1R0dmnf.jpg"
}
```

## Execution :

    python digitaleyes.py




