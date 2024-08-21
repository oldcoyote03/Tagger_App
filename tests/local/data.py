""" Data for Local Tests """

from uuid import UUID
from datetime import date


class MockData:
    """ Test Data """

    BOOKMARKS_DATA = [
        {
            "id": UUID('e52cfaf0-acec-400a-9a07-82574f62bc07'),
            "url": "https://www.foo.com",
            "created_at": date(2000, 1, 1),
        },
        {
            "id": UUID('abbfddb2-6ace-403f-a2a4-5cf949c28ac4'),
            "url": "https://www.bar.com",
            "created_at": date(2003, 5, 22),
        },
    ]
