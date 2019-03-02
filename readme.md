# Scrapstuff

Scapstuff fetch dofus 1.29 data from http://barbok.eratz.fr

## Fetched data

You could find all fetched data here:
- [items](fetched_data/items.json)
- [sets](fetched_data/sets.json)

## Getting started

### Requesite

You need at least python 3.7
To install dependancies run:
```bash
pip install -r requirements.txt
```

### Scraper

#### Items

To fetch items run:
```bash
scrapy crawl items
```
This will produce a items.json with all items (including weapons) with their name, level, recipe, bonus and requirements information. If the item is a weapon there is an additional information called weapon_stat.
Item information example:
```json
{
    "name": "Petite Epée de Fouraille",
    "level": 13,
    "recipe": [
        {
            "item": "Cuivre",
            "count": 3
        },
        {
            "item": "Bois de Châtaignier",
            "count": 5
        },
        {
            "item": "Fer",
            "count": 5
        }
    ],
    "bonus": [
        {
            "type": "Dommages neutre",
            "values": [
                11,
                15
            ]
        },
        {
            "type": "Vitalité",
            "values": 11
        },
        {
            "type": "Agilité",
            "values": -15
        }
    ],
    "weapon_stats": {
        "AP": 4,
        "scope": 1,
        "critical_hit_bonus": 5,
        "critical_hit_prob": 50,
        "fail_prob": 50
    },
    "requirements": [
        {
            "type": "Force >",
            "value": 26
        }
    ]
},
```

#### Sets

To fetch sets run:
```bash
scrapy crawl sets
```
This will produce a sets.json with all sets (including weapons) with their name, items and bonus by weared items count.
Set information example:
```json
{
    "name": "Panoplie Ougah",
    "items": [
        "Ougalurette",
        "Ougature",
        "Ougamulette",
        "Ougarteau"
    ],
    "bonus": [
        [],
        [
            {
                "type": "Dommages",
                "value": "2"
            },
            {
                "type": "Prospection",
                "value": "10"
            },
            {
                "type": "Sagesse",
                "value": "10"
            }
        ],
        [
            {
                "type": "Dommages",
                "value": "4"
            },
            {
                "type": "Prospection",
                "value": "20"
            },
            {
                "type": "Sagesse",
                "value": "20"
            }
        ],
        [
            {
                "type": "Dommages",
                "value": "6"
            },
            {
                "type": "Prospection",
                "value": "30"
            },
            {
                "type": "Sagesse",
                "value": "30"
            },
            {
                "type": "Portée",
                "value": "1"
            }
        ]
    ]
}
```