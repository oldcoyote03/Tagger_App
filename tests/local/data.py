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
    EXAMPLE_DATA = [
        {
            "id": UUID("e6bcc9df-9a89-4b31-b01f-5c865a095979"),
            "name": "item1",
            "flag": True,
            "quantity": 0,
            "created_at": date(2000, 1, 1),
        },
        {
            "id": UUID("c0f428b0-3661-4990-af3b-ea0c1c7019e0"),
            "name": "item2",
            "flag": True,
            "quantity": 1,
            "created_at": date(1985, 5, 22),
        },
        {
            "id": UUID("bd712cd9-ee33-46d7-8c64-c529c77d8741"),
            "name": "item3",
            "flag": True,
            "quantity": 2,
            "created_at": date(2013, 12, 4),
        },
        {
            "id": UUID("41850dea-95df-40fc-bcd7-754bc17c4f0b"),
            "name": "item4",
            "flag": False,
            "quantity": 0,
            "created_at": date(2022, 6, 26),
        },
        {
            "id": UUID("fda3f50b-f33f-4fe1-b94b-003b059793ec"),
            "name": "item5",
            "flag": False,
            "quantity": 1,
            "created_at": date(1994, 4, 14),
        },
        {
            "id": UUID("ea1bc265-e436-4994-972f-a6888a02a11b"),
            "name": "item6",
            "flag": False,
            "quantity": 2,
            "created_at": date(2003, 5, 22),
        },
    ]
