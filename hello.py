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
    for event in events:
        event_id = event['eid']
        event_url = get_event_url(event_id)
        print(event_url)
        # Get event details and extract start time, summary and description. Maybe also image.
    print(metadata)

def get_event_url(event_id):
    uid = event_id['uid']
    seq = event_id['seq']
    tid = event_id['tid']
    rid = event_id['rid']
    return f"https://tockify.com/api/ngevent/{uid}-{seq}-{tid}-{rid}?calname=stagiune"


if __name__ == "__main__":
    main()
