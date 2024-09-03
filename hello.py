from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup
import requests

def main():
    # start url is https://tockify.com/api/ngevent?calname=stagiune&startms=1725224400000
    # returns a list of events + metadata
    # each event has an event id:
    # {
    #     "uid": "766",
    #     "seq": 0,
    #     "tid": 1751040000000,
    #     "rid": 0
    # }
    # use the event id to get the event details url:
    # event url is https://tockify.com/api/ngevent/766-0-1751040000000-0?calname=stagiune
    response = requests.get("https://tockify.com/api/ngevent?calname=stagiune&startms=1725224400000").json()
    events = response['events']
    metadata = response['metaData']
    for event in events[:]:
        event_id = event['eid']
        event_url = get_event_url(event_id)
        event_response = requests.get(event_url).json()
        event_data = event_response['events'][0]
        when = event_data['when']
        event_start_millis = when['start']['millis']
        event_end_millis = when['end']['millis']
        event_start = datetime.fromtimestamp(event_start_millis / 1000)
        event_end = datetime.fromtimestamp(event_end_millis / 1000)
        content = event_data['content']
        summary = content['summary']['text']
        description = content['description']['text'].replace("><p", ">\n\t<p")
        event_details = extract_event_details(description)
        # TODO: parse description and extract event details
        #       (orchestra, conductor, soloists, works).
        print(f"""{summary} - {event_url}\n\t{event_details}\n\n\t{event_start} - {event_end}\n""")
    print(metadata)

def get_event_url(event_id):
    uid = event_id['uid']
    seq = event_id['seq']
    tid = event_id['tid']
    rid = event_id['rid']
    return f"https://tockify.com/api/ngevent/{uid}-{seq}-{tid}-{rid}?calname=stagiune"

@dataclass(frozen=True)
class Soloist:
    name: str
    instrument: str|None

@dataclass(frozen=True)
class Work:
    composer: str
    title: str

@dataclass(frozen=True)
class EventDetails:
    subtitle: str | None
    orchestra: str
    conductor: str
    soloists: list[Soloist]
    works: list[Work]

def extract_event_details(description) -> EventDetails:
    parsed_description = BeautifulSoup(description, 'html.parser')
    ps = parsed_description.find_all('p')
    subtitle = extract_subtitle(ps[0])
    orchestra = extract_orchestra(ps) if subtitle is None else extract_orchestra(ps[1:])
    return EventDetails(subtitle, orchestra, "", [], [])

def extract_subtitle(p):
    if p.em is not None:
        return p.em.text
    return None

def extract_orchestra(ps):
    for p in ps:
        if p.strong is not None:
            return p.strong.text
    return "Unknown Orchestra"

if __name__ == "__main__":
    main()
