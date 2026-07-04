from dataclasses import dataclass
from itertools import cycle


@dataclass(frozen=True, slots=True)
class WorkItem:
    name: str
    image_path: str
    image_alt: str
    image_width: int
    image_height: int


WORK_ITEMS = (
    WorkItem(
        name="Mobile Health Platform",
        image_path="images/works/email-phone.jpg",
        image_alt=(
            "Mobile health platform displayed on a phone against a red " "background"
        ),
        image_width=5100,
        image_height=3400,
    ),
    WorkItem(
        name="eBay Advertising Signage",
        image_path="images/works/signage.jpg",
        image_alt="eBay Advertising welcome sign surrounded by greenery",
        image_width=4800,
        image_height=3100,
    ),
    WorkItem(
        name="Lai Can Packaging",
        image_path="images/works/lai_project_can.jpg",
        image_alt="Hand holding a white beverage can with navy lettering",
        image_width=4000,
        image_height=6000,
    ),
    WorkItem(
        name="Lai Brand Wordmark",
        image_path="images/works/logo_lai_project.gif",
        image_alt="Animated Lai brand wordmark",
        image_width=1920,
        image_height=1920,
    ),
    WorkItem(
        name="Healthcare Postcard",
        image_path="images/works/postcard_mockup.jpg",
        image_alt="Healthcare brand postcard mockup on a navy background",
        image_width=1350,
        image_height=1080,
    ),
)

WORK_LAYOUT_ROTATION = (
    "landscape-compact",  # Small landscape
    "landscape-wide",  # Wide landscape
    "portrait-feature",  # Tall portrait
    "square",  # Square
    "landscape-card",  # Medium landscape
)

# Each work item is assigned a layout from WORK_LAYOUT_ROTATION in a repeating cycle
WORK_GRID = tuple(zip(WORK_ITEMS, cycle(WORK_LAYOUT_ROTATION)))
