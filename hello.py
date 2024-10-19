from dataclasses import dataclass
from datetime import datetime
import locale
import sys
from typing import Optional
from bs4 import BeautifulSoup, Tag
import requests
import json

def main():
    locale.setlocale(locale.LC_ALL, "ro_RO.UTF-8")

    # don't download the data if --no-download is passed
    should_download = "--no-download" not in sys.argv
    if should_download:
        download_events_data()
    else:
        print("Skipping download", file=sys.stderr)

    only_download = "--only-download" in sys.argv
    if only_download:
        return

    with open("docs/raw_events.json") as f:
        events_details = json.load(f)["events_details"]
    parsed_events = [parse_event(event) for event in events_details]

    for i, event in enumerate(parsed_events):
        if i + 1 < len(parsed_events):
            next_event = parsed_events[i + 1]
            # assume that if two events have the same title and details,
            # they are the same show scheduled twice
            if event.title == next_event.title and are_same(
                event.details, next_event.details
            ):
                event.schedulings.append(next_event.schedulings[0])
                parsed_events.pop(i + 1)

    print(
        """<!DOCTYPE html>
        <html>
        <head>
        <meta charset='utf-8'>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Stagiunea Filarmonicii George Enescu</title>
        <link rel="stylesheet" href="style.css">
        </head>
        <body>"""
    )
    print("<header><h1>Stagiunea Filarmonicii <em>„George&nbsp;Enescu”</em></h1></header>")
    print("<main>")
    for event in parsed_events:
        print("<section>")
        print(f"<h2>{event.title}</h2>")
        print(f"<img src='{event.image_url}'/>")
        print("<p>")
        for i, scheduling in enumerate(event.schedulings):
            if scheduling.tickets_url is not None:
                print(f"<a href='{scheduling.tickets_url}' class='button'>", end="")
            print(
                f"{scheduling.date.strftime("%a, %d %b %Y, %H:%M")}",
                end="",
            )
            if scheduling.tickets_url is not None:
                print("</a>", end="")
            if i + 1 < len(event.schedulings):
                print("<br/>")
        print("</p>")
        print(f"{event.details}")
        print("</section>")

    print("</main>")
    print("""<footer><a href="/raw_events.json">Raw data</a></footer>""")
    print("</body></html>")


def download_events_data():
    # change start_date for the current season
    start_date = datetime(2024, 9, 1)
    events_ids = get_events_ids(start_date)
    events_details = get_events_details(events_ids)
    # save the details on disk as JSON
    with open("docs/raw_events.json", "w") as f:
        json.dump({"events_details": events_details}, f, indent=2)


def get_events_ids(start_date: datetime):
    start_ms = start_date.timestamp() * 1000
    response = requests.get(
        f"https://tockify.com/api/ngevent?calname=stagiune&startms={start_ms}"
    ).json()
    return [event["eid"] for event in response["events"]]


def get_events_details(events_ids):
    print(f"Downloading {len(events_ids)} events", file=sys.stderr, end="")
    events_details = [get_event_details(event_id) for event_id in events_ids]
    return events_details


def get_event_details(event_id):
    event_url = get_event_url(event_id)
    print(".", file=sys.stderr, end="", flush=True)
    event_response = requests.get(event_url).json()
    return event_response["events"][0]


def parse_event(event_data):
    when = event_data["when"]
    event_start_millis = when["start"]["millis"]
    event_start = datetime.fromtimestamp(event_start_millis / 1000)
    content = event_data["content"]
    image_url = get_image_url(content)
    title = standardize_title(content["summary"]["text"])
    description = standardize(content["description"]["text"])
    tickets_url = content["customButtonLink"] if "customButtonLink" in content else None
    print(f"{title} {event_start} {tickets_url}", file=sys.stderr)

    return Event(
        [Scheduling(tickets_url, event_start)], title, description, image_url
    )


def get_image_url(event_content):
    image_set = event_content["imageSets"][0]
    owner_id = image_set["ownerId"]
    image_id = image_set["id"]
    return f"https://d3flpus5evl89n.cloudfront.net/{owner_id}/{image_id}/scaled_512.jpg"


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
    print(f"not same:\n{details1}\n{details2}\n", file=sys.stderr)
    return False


def standardize_title(title: str) -> str:
    return title.replace("ÎNCHIDERERA", "ÎNCHIDEREA")


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
class Scheduling:
    tickets_url: Optional[str]
    date: datetime


@dataclass(frozen=True)
class Event:
    schedulings: list[Scheduling]
    title: str
    details: str
    image_url: Optional[str] = None


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
