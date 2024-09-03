from datetime import datetime
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
    for event in events[:4]:
        event_id = event['eid']
        event_url = get_event_url(event_id)
        event_response = requests.get(event_url).json()
        event_details = event_response['events'][0]
        when = event_details['when']
        event_start_millis = when['start']['millis']
        event_end_millis = when['end']['millis']
        event_start = datetime.fromtimestamp(event_start_millis / 1000)
        event_end = datetime.fromtimestamp(event_end_millis / 1000)
        content = event_details['content']
        summary = content['summary']['text']
        description = content['description']['text'].replace("><p", ">\n\t<p")
        # TODO: parse description and extract event details
        #       (orchestra, conductor, soloists, works).
        print(f"""{summary}\n\t{description}\n\n\t{event_start} - {event_end}\n""")
    print(metadata)

def get_event_url(event_id):
    uid = event_id['uid']
    seq = event_id['seq']
    tid = event_id['tid']
    rid = event_id['rid']
    return f"https://tockify.com/api/ngevent/{uid}-{seq}-{tid}-{rid}?calname=stagiune"

def extract_event_details(summary):
    pass

if __name__ == "__main__":
    main()
