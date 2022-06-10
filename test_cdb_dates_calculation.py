# git@github.com:ProzorroUKR/dateorro.git
from dateorro import calc_normalized_datetime, calc_working_datetime
import datetime
import requests
import typing as t
import json
from tabulate import tabulate


def parse_dt_arg(dt_iso_str) -> datetime.datetime:
    return datetime.datetime.strptime(dt_iso_str, '%Y-%m-%dT%H:%M:%S')


def get_calendar() -> t.Dict[str, bool]:
    resp = requests.get(
        'https://raw.githubusercontent.com/ProzorroUKR/'
        'standards/master/calendars/workdays_off.json'
    )
    resp_json = json.loads(resp.text)

    data = {}
    for d in resp_json:
        data[d] = True

    return data


def calculate_normalized(
    dt_obj: datetime.datetime,
    timedelta_obj: datetime.timedelta
) -> datetime.datetime:
    return calc_normalized_datetime(
        dt_obj,
        ceil=timedelta_obj > datetime.timedelta()
    )


def calculate_expected(
    dt_obj: datetime.datetime,
    timedelta_obj: datetime.timedelta,
    cdb_calendar: t.Dict[str, bool]
) -> datetime.datetime:
    return calc_working_datetime(
        dt_obj,
        timedelta_obj,
        True,
        cdb_calendar
    )


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 5:
        print('not enough arguments\n')
        print(
            f'usage:\t {sys.argv[0]} '
            'XXXX-XX-XXTXX:XX:XX(enquiry start) '
            'XXXX-XX-XXTXX:XX:XX(enquiry end) '
            'XXXX-XX-XXTXX:XX:XX(tendering start) '
            'XXXX-XX-XXTXX:XX:XX(tendering end)'
        )
        print(
            'XXXX-XX-XXTXX:XX:XX - is datetime in iso format, like '
            'YYYY-mm-ddTHH:MM:SS'
        )
        exit(0)

    (
        enq_start,
        enq_end,
        tend_start,
        tend_end,
    ) = [parse_dt_arg(arg) for arg in sys.argv[1:]]

    cdb_calendar = get_calendar()

    cdb_expected_enq_start = calculate_normalized(
        enq_start,
        datetime.timedelta(days=3)
    )
    cdb_expected_enq_end = calculate_expected(
        cdb_expected_enq_start,
        datetime.timedelta(days=3),
        cdb_calendar
    )
    cdb_expected_tend_start = calculate_normalized(
        tend_start,
        datetime.timedelta(days=2)
    )
    cdb_expected_tend_end = calculate_expected(
        cdb_expected_tend_start,
        datetime.timedelta(days=2),
        cdb_calendar
    )

    data = [
        [
            'enquiry period start',
            enq_start.isoformat(),
            cdb_expected_enq_start.isoformat()
        ],
        [
            'enquiry period end',
            enq_end.isoformat(),
            cdb_expected_enq_end.isoformat()
        ],
        [
            'tender period start',
            tend_start.isoformat(),
            cdb_expected_tend_start.isoformat()
        ],
        [
            'tender period end',
            tend_end.isoformat(),
            cdb_expected_tend_end.isoformat()
        ]
    ]
    print(tabulate(data, headers=['name', 'requested', 'calculated by CDB']))
