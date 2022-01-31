GROUP_SETTINGS = dict(
    help_option_names=["-?", "-h", "--help"],
    max_content_width=116  # max PEP8 line-width, -4 to adjust for initial indent
)

DYNAMIC_RANGE_MAP = {
    "SMPTE ST 2086": "HDR10",
    "HDR10": "HDR10",
    "SMPTE ST 2094 App 4": "HDR10+",
    "HDR10+": "HDR10+",
    "Dolby Vision": "DV"
}

AUDIO_CHANNEL_LAYOUT_WEIGHT = {
    "LFE": 0.1
}
