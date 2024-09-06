from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup, Tag
import requests


def main():
    # change startms for the current season
    response = requests.get(
        "https://tockify.com/api/ngevent?calname=stagiune&startms=1725224400000"
    ).json()
    events = response["events"]
    parsed_events = [get_and_parse_event(get_event_url(event["eid"])) for event in events[::2]]
    parsed_events.sort(key=lambda event: event.start)

    print("<html><head><meta charset='utf-8'><title>Stagiunea Filarmonicii George Enescu</title></head><body>")
    print("<h1>Stagiunea Filarmonicii George Enescu</h1>")
    for event in parsed_events:
        print(f"<h2>{event.title}</h2>")
        # TODO: print start time for humans (including day of week)
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


def get_event_url(event_id):
    uid = event_id["uid"]
    seq = event_id["seq"]
    tid = event_id["tid"]
    rid = event_id["rid"]
    return f"https://tockify.com/api/ngevent/{uid}-{seq}-{tid}-{rid}?calname=stagiune"


@dataclass(frozen=True)
class Event:
    start: datetime
    end: datetime
    title: str
    details: str


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
