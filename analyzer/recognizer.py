from typing import Optional, List

from presidio_analyzer import Pattern, PatternRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts

import regex as re


class CoordinatesRecognizer(PatternRecognizer):
    """
    Recognize date using regex.
    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
          Pattern(
                "decimal degrees",
                r"[-+]?([1-8]?\d(\.\d+)|90(\.0+)?),\s*[-+]?(180(\.0+)|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)",
                0.6,
        ),
        Pattern(
                "Latitude 1",
                r"([1-8]?\d(\.\d+)|90(\.0+)?)[N|S]",  
                0.6,
        ),
        Pattern(
                "Latitude 2",
                r"[N|S]([1-8]?\d(\.\d+)|90(\.0+)?)",
                0.6,
        ),
        Pattern(
                "Longitude 2",
                r"[E|W](180(\.0+)|((1[0-7]\d)|([1-9]?\d))(\.\d+))",
                0.6,
        ),
        Pattern(
                "Longitude 1",
                r"(180(\.0+)|((1[0-7]\d)|([1-9]?\d))(\.\d+))[E|W]",
                0.6,
        ),
        Pattern(
                "DMS",
                r"((\d+)\s?\º|((\d+)\s?\˜°|((\d+)\s?\°)|(\d+)\s?\˚))\s?((\d+)\s?\’|(\d+)\s?\')?\s?((\d{1,}\.?\,?\d{0,}?)\")?\s?[N,S,E,W]",
                0.6,
        ),
        Pattern(
                "DMS 2",
                r"[N,S,E,W]((\d+)\s?\º|((\d+)\s?\˜°|((\d+)\s?\°)|(\d+)\s?\˚))\s?((\d+)\s?\’|(\d+)\s?\')?\s?((\d{1,}\.?\,?\d{0,}?)\")?",
                0.6,
        ),
    ]

    CONTEXT = ["coordinates"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "GEO_COORDINATES",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

