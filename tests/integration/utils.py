from typing import List

import random

BAD_STRING_VALUES = [
    "None",
    "null",
    "True",
    "False",
    "0",
    "-1",
    "Some super long really terrible no good very bad name that is just too long to be a name, but is just for testing purposes. I hope this is long enough to break something hahahahah. Evil laugh. And now it is going to be even longer. You can not hope to stop the ceaseless and cruel length of this string!!!! I will live forever!!! Mwahahahahahahahahahahahahahahahahahahahahahahaha!",
    """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lobortis scelerisque fermentum dui faucibus in ornare quam viverra. Pellentesque sit amet porttitor eget dolor morbi non arcu. Dui vivamus arcu felis bibendum ut tristique. Sit amet nulla facilisi morbi tempus iaculis. Aliquam nulla facilisi cras fermentum odio. Rhoncus mattis rhoncus urna neque viverra justo nec ultrices dui. Ullamcorper malesuada proin libero nunc consequat interdum varius sit. Purus in massa tempor nec feugiat nisl pretium fusce id. Libero justo laoreet sit amet cursus. Ultrices neque ornare aenean euismod elementum. Fermentum dui faucibus in ornare quam viverra orci sagittis eu. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Urna porttitor rhoncus dolor purus non enim. Nisl vel pretium lectus quam. Ante in nibh mauris cursus mattis. Egestas fringilla phasellus faucibus scelerisque eleifend donec pretium vulputate.

Accumsan in nisl nisi scelerisque eu ultrices vitae auctor. Facilisis leo vel fringilla est. Vulputate mi sit amet mauris commodo quis imperdiet. Nec ullamcorper sit amet risus nullam eget felis eget. Nulla porttitor massa id neque aliquam vestibulum. Sed pulvinar proin gravida hendrerit. Posuere sollicitudin aliquam ultrices sagittis orci a. Nibh venenatis cras sed felis eget. Et odio pellentesque diam volutpat commodo sed egestas. Blandit aliquam etiam erat velit scelerisque. Est ante in nibh mauris cursus mattis. Quis hendrerit dolor magna eget est lorem ipsum.

Sit amet consectetur adipiscing elit ut. Maecenas pharetra convallis posuere morbi leo urna. Dignissim convallis aenean et tortor at risus viverra adipiscing at. Non diam phasellus vestibulum lorem sed risus. Et sollicitudin ac orci phasellus egestas tellus. Mi eget mauris pharetra et ultrices neque ornare aenean. Tempor orci eu lobortis elementum. Ipsum nunc aliquet bibendum enim facilisis gravida neque. Vehicula ipsum a arcu cursus vitae congue mauris rhoncus aenean. Aliquam eleifend mi in nulla posuere sollicitudin aliquam. Et molestie ac feugiat sed lectus vestibulum mattis ullamcorper. Libero nunc consequat interdum varius sit amet mattis vulputate. Malesuada bibendum arcu vitae elementum curabitur vitae nunc sed velit. Lectus sit amet est placerat in egestas erat. Ullamcorper dignissim cras tincidunt lobortis feugiat vivamus. Auctor urna nunc id cursus metus aliquam. Tempus egestas sed sed risus pretium quam vulputate dignissim. Feugiat nibh sed pulvinar proin gravida hendrerit lectus a. Amet nisl purus in mollis nunc.

Ut pharetra sit amet aliquam id diam maecenas ultricies mi. Velit aliquet sagittis id consectetur purus. Purus semper eget duis at tellus. Adipiscing elit pellentesque habitant morbi tristique senectus et netus et. Lorem dolor sed viverra ipsum nunc aliquet bibendum enim facilisis. Pellentesque diam volutpat commodo sed egestas. Proin nibh nisl condimentum id. Feugiat scelerisque varius morbi enim nunc faucibus. Ut placerat orci nulla pellentesque dignissim enim sit amet. Rutrum tellus pellentesque eu tincidunt. Adipiscing at in tellus integer. Porttitor rhoncus dolor purus non enim praesent elementum facilisis leo. Eleifend quam adipiscing vitae proin sagittis nisl rhoncus. Purus in mollis nunc sed id semper risus. Amet venenatis urna cursus eget. Mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor. Nulla aliquet porttitor lacus luctus accumsan tortor. Nisl purus in mollis nunc sed id semper risus in. Arcu ac tortor dignissim convallis aenean et tortor. Accumsan in nisl nisi scelerisque.

Scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique senectus. Enim ut tellus elementum sagittis vitae. Senectus et netus et malesuada fames ac. Odio pellentesque diam volutpat commodo sed egestas. Sapien nec sagittis aliquam malesuada bibendum arcu vitae elementum curabitur. Pellentesque dignissim enim sit amet venenatis urna cursus eget. Quam pellentesque nec nam aliquam sem. In massa tempor nec feugiat. Malesuada fames ac turpis egestas. Condimentum id venenatis a condimentum vitae. Sed libero enim sed faucibus turpis in. Blandit cursus risus at ultrices mi tempus imperdiet nulla. Tortor id aliquet lectus proin nibh nisl condimentum id. In aliquam sem fringilla ut morbi tincidunt augue. Arcu felis bibendum ut tristique et egestas quis. Vel pharetra vel turpis nunc eget. Sapien et ligula ullamcorper malesuada proin libero.""",
    "123045",
    "\n",
    "\t",
    " ",
    "",
    "01240.1",
    "true",
    "false",
    "\\",
    ",./;'[]\\-=",
    "Ω≈ç√∫˜µ≤≥÷",
    "",
    "‪‪test‪",
    "‫test‫",
    "test",
    "Z̮̞̠͙͔ͅḀ̗̞͈̻̗Ḷ͙͎̯̹̞͓G̻O̭̗̮",
    "<img src=x onerror=alert(123) />",
    "<svg><script>123<1>alert(123)</script>",
    '"><script>alert(123);</script x="',
    "'><script>alert(123);</script x='",
    '<script>alert(123);</script x=","',
    "$HOME",
    "$ENV{'HOME'}",
]

UUIDS = [
    "216b8abc-c544-11ee-b6c3-fa594adb4f7a",
    "1d9d6035-6af0-4168-8c30-b64b73ccda97",
    "1e3d1632d04f4a72",
    "213416656460545719371413119541142710892",
    "1eec544216e7f42",
    "2779827f2e7247d2b4ec2405bdc25c63",
    "ORGANIZATION-15a0x0g93k25j25",
    "org-1e3d1632d04f4a72",
    "9073926b-929f-31c2-abc9-fad77ae3e8eb",
    "cfbff0d1-9375-5685-968c-48ce8b15ae17",
    "11001110000111100011111001000001",
    "1662411373616235",
    "ade26975",
    "0c0c504e5367",
    "1534723675",
    "316416162295410",
    "34899de1-1eec5446a269a8a",
    "CID-d95d-6546",
    "org::32-f0-39-ad-4f-4a-72",
    "instructor-1e3d1632d04f4a72",
    "INSTRUCT::10421::1e3d1632d04f4a72",
]


def generate_random_timestamp(bottom_bound: int = 0) -> int:
    return random.randint(bottom_bound, 10000000000)


def generate_random_uuid() -> str:
    # Select from BAD_STRING_VALUES 10% of the time
    if random.random() < 0.1:
        return random.choice(BAD_STRING_VALUES)
    return random.choice(UUIDS)


def select_from_string_list(string_list: List[str]) -> str:
    # Select from BAD_STRING_VALUES 10% of the time
    if random.random() < 0.1:
        return random.choice(BAD_STRING_VALUES)
    return random.choice(string_list)
