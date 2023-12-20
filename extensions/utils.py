from . import jalali
from django.utils import timezone


def persions_numbers_convertor(subject):
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    for e, p in numbers.items():
        subject = subject.replace(e, p)

    return subject


def jalali_convertor(time):
    month = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    time = timezone.localtime(time)
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(month):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    jtime = "{} {} {} , ساعت {}:{}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute
    )

    return persions_numbers_convertor(jtime)
