import time
import datetime

d = datetime.date(2015, 1, 5)

unixtime = time.mktime(d.timetuple())


def main():
    today = datetime.datetime.today()
    today = today - datetime.timedelta(days=7)
    next_monday = today + datetime.timedelta(days=1)
    while next_monday.weekday() != 0:
        next_monday = next_monday + datetime.timedelta(days=1)
    next_monday = datetime.datetime(
        next_monday.year,
        next_monday.month,
        next_monday.day,
        21,
        30,
        0,
        0,
        datetime.timezone(datetime.timedelta(hours=9, minutes=0)),
    )
    close_time = next_monday - datetime.timedelta(days=1)
    close_time = next_monday + datetime.timedelta(days=7)

    # raid_times = [next_monday]
    days = ["Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    raid_time_str = f"<t:{int(next_monday.timestamp())}:F>"
    current_date = next_monday
    for i in range(6):
        current_date = current_date + datetime.timedelta(days=1)
        raid_time_str += f", <t:{int(current_date.timestamp())}:F>"
        # raid_times.append(current_date)

    print(f"Today: {today}")
    print(f"Next Monday is {next_monday}")
    print("/quickcreate")
    print(
        f"[template: 25] [title: Blue Mage O12S] [description: What days are you available? = {raid_time_str}] [date: {close_time.day}-{close_time.month}-{close_time.year}] [time: {close_time.hour}:{close_time.minute}] [channel: #scheduling] [advanced: < limit_per_user: 7 > < strawpoll_type: reaction >]"
    )
    # print("25")
    # print(raid_time_str)
    # print("#general")
    # print("28-06-2022")
    # print("21:00")
    # print("2")
    # print("< limit_per_user: 7 >")
    # print("Finish")


if __name__ == "__main__":
    main()
