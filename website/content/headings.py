from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HeadingSegment:
    text: str
    emphasis_color: str = ""


@dataclass(frozen=True, slots=True)
class SectionHeading:
    heading_id: str
    level: int
    variant: str
    segments: tuple[HeadingSegment, ...]


HOMEPAGE_HEADINGS = {
    "overview": SectionHeading(
        heading_id="overview-title",
        level=1,
        variant="hero",
        segments=(
            HeadingSegment("Juna is a "),
            HeadingSegment("creative team", "pink"),
            HeadingSegment(" for "),
            HeadingSegment("conscious brands", "blue"),
            HeadingSegment(
                ", crafting visual identity and messaging strategy that "
            ),
            HeadingSegment("moves your audience", "gold"),
            HeadingSegment(" to "),
            HeadingSegment("make a difference.", "green"),
        ),
    ),
    "works": SectionHeading(
        heading_id="works-title",
        level=2,
        variant="section",
        segments=(
            HeadingSegment("Our "),
            HeadingSegment("Works", "gold"),
        ),
    ),
    "about": SectionHeading(
        heading_id="about-title",
        level=2,
        variant="section",
        segments=(
            HeadingSegment("Who", "blue"),
            HeadingSegment(" you will be working with"),
        ),
    ),
    "services": SectionHeading(
        heading_id="services-title",
        level=2,
        variant="natural-wrap",
        segments=(
            HeadingSegment("How we can help "),
            HeadingSegment("raise your impact", "pink"),
        ),
    ),
    "contact": SectionHeading(
        heading_id="contact-title",
        level=2,
        variant="contact",
        segments=(HeadingSegment("Tell us about your project", "green"),),
    ),
}
