from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import locale
import sys
from typing import Optional, List, Dict
import calendar
from collections import defaultdict

from bs4 import BeautifulSoup, Tag
import chevron
import requests


def generate_calendar_data(events: List["Event"], year: int, month: int) -> Dict:
    """Generate calendar data for a specific month."""
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    
    # Create a mapping of dates to events
    events_by_date = defaultdict(list)
    for event in events:
        for scheduling in event.schedulings:
            date = scheduling.date
            if date.year == year and date.month == month:
                events_by_date[date.day].append({
                    'id': f"event-{event.id}",
                    'time': date.strftime('%H:%M'),
                    'title': event.title
                })

    # Generate calendar weeks
    weeks = []
    for week in cal.monthdays2calendar(year, month):
        days = []
        for day_num, _ in week:
            if day_num == 0:
                days.append({'day': None, 'events': []})
            else:
                days.append({
                    'day': day_num,
                    'events': events_by_date[day_num]
                })
        weeks.append({'days': days})

    return {
        'month_name': calendar.month_name[month],
        'year': year,
        'weeks': weeks
    }


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
                event.schedulings[-1].newline_after = True
                event.schedulings.append(next_event.schedulings[0])
                parsed_events.pop(i + 1)

    # Generate main index page
    with open("index.mustache", "r") as f:
        result = chevron.render(f, {"events": parsed_events})

    with open("docs/index.html", "w") as f:
        f.write(result)

    # Generate calendar pages
    # Get unique months from events
    months = set()
    for event in parsed_events:
        for scheduling in event.schedulings:
            months.add((scheduling.date.year, scheduling.date.month))

    # Generate calendar data for all months
    all_months_data = []
    for year, month in sorted(months):
        calendar_data = generate_calendar_data(parsed_events, year, month)
        all_months_data.append(calendar_data)

    # Generate a single calendar page with all months
    with open("calendar.mustache", "r") as f:
        calendar_html = chevron.render(f, {"months": all_months_data})
    
    with open("docs/calendar.html", "w") as f:
        f.write(calendar_html)


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
    img = get_image(content)
    title = standardize_title(content["summary"]["text"])
    description = standardize(content["description"]["text"])
    tickets_url = content["customButtonLink"] if "customButtonLink" in content else None
    eid = event_data["eid"]
    event_id = f"{eid['uid']}-{eid['seq']}-{eid['tid']}-{eid['rid']}"

    return Event(event_id, [Scheduling(tickets_url, event_start)], title, description, img)


@dataclass(frozen=True)
class Img:
    src: str
    alt: str


def get_image(event_content) -> Img:
    image_set = event_content["imageSets"][0]
    owner_id = image_set["ownerId"]
    image_id = image_set["id"]
    width = image_set["width"]
    if width < 512:
        size = 256
    else:
        size = 512
    src = (
        f"https://d3flpus5evl89n.cloudfront.net/{owner_id}/{image_id}/scaled_{size}.jpg"
    )
    alt = image_set["altText"]
    return Img(src, alt)


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
        .replace("op. 120 </span></div>", "op. 120</span></div>")
    )


# Can't make this frozen, it thrown in __post_init__.
@dataclass
class Scheduling:
    tickets_url: Optional[str]
    date: datetime

    def __post_init__(self):
        self.when = self.date.strftime("%a, %d %b %Y, %H:%M")


@dataclass(frozen=True)
class Event:
    id: str
    schedulings: list[Scheduling]
    title: str
    details: str
    image: Optional[Img] = None


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
