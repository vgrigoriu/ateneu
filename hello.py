from dataclasses import dataclass
from datetime import datetime
import locale
import sys
from bs4 import BeautifulSoup, Tag
import requests


def main():
    locale.setlocale(locale.LC_ALL, "ro_RO.UTF-8")

    # change startms for the current season
    response = requests.get(
        "https://tockify.com/api/ngevent?calname=stagiune&startms=1725224400000"
    ).json()
    events = response["events"]
    parsed_events = [get_and_parse_event(event["eid"]) for event in events]

    for i, event in enumerate(parsed_events):
        if i + 1 < len(parsed_events):
            next_event = parsed_events[i + 1]
            # assume that if two events have the same title and details, they are one after the other
            # TODO: some Thu/Fri concerts have different details: standardardize them
            if event.title == next_event.title and are_same(
                event.details, next_event.details
            ):
                event.dates.append(next_event.dates[0])
                event.urls.append(next_event.urls[0])
                parsed_events.pop(i + 1)

    print(
        """<html>
        <head>
        <meta charset='utf-8'>
        <title>Stagiunea Filarmonicii George Enescu</title>
        </head>
        <body>"""
    )
    print("<h1>Stagiunea Filarmonicii George Enescu</h1>")
    for event in parsed_events:
        print("<div class='event'>")
        print(f"<h2 style='color: green;'>{event.title}</h2>")
        print("<p>")
        for i in range(len(event.dates)):
            print(
                f"<a href='{event.urls[i]}'>{event.dates[i].strftime("%A, %d %B %Y, %H:%M")}</a>",
                end="",
            )
            if i + 1 < len(event.dates):
                print(", ")
        print("</p>")
        print(f"{event.details}")
        print("</div>")

    print("</body></html>")


def get_and_parse_event(event_id):
    event_url = get_event_url(event_id)
    human_event_url = get_human_event_url(event_id)
    event_response = requests.get(event_url).json()
    event_data = event_response["events"][0]
    when = event_data["when"]
    event_start_millis = when["start"]["millis"]
    event_start = datetime.fromtimestamp(event_start_millis / 1000)
    content = event_data["content"]
    summary = content["summary"]["text"]
    description = standardize(content["description"]["text"])

    return Event([human_event_url], [event_start], summary, description)


def get_event_url(event_id):
    uid = event_id["uid"]
    seq = event_id["seq"]
    tid = event_id["tid"]
    rid = event_id["rid"]
    return f"https://tockify.com/api/ngevent/{uid}-{seq}-{tid}-{rid}?calname=stagiune"


def get_human_event_url(event_id):
    return f"https://tockify.com/stagiune/detail/{event_id["uid"]}/{event_id["tid"]}"


def are_same(details1: str, details2: str) -> bool:
    if details1 == details2:
        return True
    print(f"not same:\n{details1}\n{details2}", file=sys.stderr)


def standardize(details: str) -> str:
    return (
        details.replace(" <br />", "<br />")
        .replace("<span></span>", "")
        .replace("<span> </span>", "")
        .replace("<p><strong></strong></p>", "")
        .replace("<p><strong> </strong></p>", "")
        .replace("<div></div>", "")
        .replace("<p></p>", "")
    )


@dataclass(frozen=True)
class Event:
    urls: list[str]
    dates: list[datetime]
    title: str
    details: str


# unused, kept for historical interest
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
