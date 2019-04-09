import datetime
from datetime import timezone

def changingTime(a):
    split1 = a.split(":")
    from_time = datetime.datetime.now()
    from_time = from_time.replace(minute=int(split1[1]), hour=int(split1[0]), second=0, microsecond=0)
    from_time = from_time.replace(tzinfo=timezone.utc).timestamp()
    from_time = datetime.datetime.fromtimestamp(from_time).strftime('%Y-%m-%d %H:%M:%S')
    return(from_time)
