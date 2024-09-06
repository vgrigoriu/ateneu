from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup, Tag
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
    response = requests.get(
        "https://tockify.com/api/ngevent?calname=stagiune&startms=1725224400000"
    ).json()
    events = response["events"]
    parsed_events = [get_and_parse_event(get_event_url(event["eid"])) for event in events[::2]]
    parsed_events.sort(key=lambda event: event.start)

    print("<html><head><meta charset='utf-8'></head><body>")
    print("<h1>Stagiunea Filarmonicii George Enescu</h1>")
    for event in parsed_events:
        print(f"<h2>{event.title}</h2>")
        print(f"<p>{event.start} - {event.end}</p>")
        print(f"{event.details}")

    print("</body></html>")

def get_and_parse_event(event_url):
    event_response = requests.get(event_url).json()
    event_data = event_response["events"][0]
    when = event_data["when"]
    event_start_millis = when["start"]["millis"]
    event_end_millis = when["end"]["millis"]
    event_start = datetime.fromtimestamp(event_start_millis / 1000)
    event_end = datetime.fromtimestamp(event_end_millis / 1000)
    content = event_data["content"]
    summary = content["summary"]["text"]
    description = content["description"]["text"]

    return Event(event_start, event_end, summary, description)

def print_event(event):
    print(f"Title: {event.title}")
    print(f"Start: {event.start}")
    print(f"End: {event.end}")
    print(f"Details: {event.details}")
    print()


def get_event_url(event_id):
    uid = event_id["uid"]
    seq = event_id["seq"]
    tid = event_id["tid"]
    rid = event_id["rid"]
    return f"https://tockify.com/api/ngevent/{uid}-{seq}-{tid}-{rid}?calname=stagiune"


@dataclass(frozen=True)
class Soloist:
    name: str
    instrument: str | None


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


@dataclass(frozen=True)
class Event:
    start: datetime
    end: datetime
    title: str
    details: str


def extract_event_details(description) -> EventDetails:
    tags = normalize(description)

    subtitle = extract_subtitle(tags[0])
    orchestra_index = 0 if subtitle is None else 1
    orchestra = extract_orchestra(tags[orchestra_index])
    conductor_index = orchestra_index + 1
    (conductor, is_soloist) = extract_conductor(tags[conductor_index])
    soloists = [Soloist(conductor, None)] if is_soloist else []
    # TODO: extract rest of soloists and works
    # problems:
    # - some entries use <div> instead of <p>
    # - https://tockify.com/api/ngevent/731-0-1740675600000-0?calname=stagiune
    #   (everything is wrapped in two <div>s)
    # - https://tockify.com/api/ngevent/709-0-1733418000000-0?calname=stagiune
    #   (has no "Program" line)
    # - https://tockify.com/api/ngevent/715-0-1735923600000-0?calname=stagiune
    #   (has "În program, lucrări de"...)
    # - https://tockify.com/api/ngevent/727-0-1739466000000-0?calname=stagiune
    #   (has soloists each on their own line)
    #   (has "Dirijorul corului" at the end)
    # - https://tockify.com/api/ngevent/751-0-1746720000000-0?calname=stagiune
    #   (each work has its own soloists)
    soloist_index = conductor_index + 1
    print("Soloist tag:", tags[soloist_index])
    if soloist_index + 1 < len(tags):
        print("Next tag: ", tags[soloist_index + 1])
    else:
        print("Fewer rows than expected:")
        print(tags)
    print()
    return EventDetails(subtitle, orchestra, conductor, soloists, [])


def extract_subtitle(p):
    if p.em is not None:
        return p.em.text
    return None


def extract_orchestra(p):
    return p.strong.text


def extract_conductor(p):
    print("Conductor tag:", p)
    conductor_name = p.strong.text.strip()
    if p.text.startswith("Dirijor și solist"):
        return (conductor_name, True)
    if p.text.startswith("Dirijor"):
        return (conductor_name, False)
    print(f"Unexpected conductor format: {p}")
    return (conductor_name, False)


def normalize(description):
    return [
        normalized_tag
        for element in BeautifulSoup(description, "html.parser").contents
        if type(element) is Tag and element.text.strip() != ""
        for normalized_tag in normalize_tag(element)
    ]


def normalize_tag(tag):
    # replace all divs with p
    if tag.name == "div":
        tag.name = "p"
    for div in tag.find_all("div"):
        div.name = "p"
    # remove spans
    for span in tag.find_all("span"):
        if span.text.strip() == "":
            span.extract()
        else:
            span.unwrap()
    # unwrap <p><p><p>
    if tag.p is not None:
        tag.p.unwrap()
    # if tag contains multiple p tags, return all of them
    if len(tag.find_all("p")) > 1:
        return tag.contents
    return [tag]


if __name__ == "__main__":
    main()
