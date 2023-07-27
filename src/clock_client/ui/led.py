import math
import pygame

# Colors for the simulated LED segments.
# Each named color has two color objects -- the first is used for a segment
# that is turned off, the second is used for a segment that is turned on
COLORS = {
    "white": (pygame.color.Color(20, 20, 20), pygame.color.Color(240, 240, 240)),
    "red": (pygame.color.Color(24, 0, 0), pygame.color.Color(240, 0, 0)),
    "green": (pygame.color.Color(0, 24, 0), pygame.color.Color(0, 224, 0)),
    "blue": (pygame.color.Color(0, 0, 24), pygame.color.Color(0, 72, 255)),
    "cyan": (pygame.color.Color(0, 20, 20), pygame.color.Color(0, 196, 196)),
    "amber": (pygame.color.Color(20, 20, 0), pygame.color.Color(196, 196, 0)),
}

# Ratio of segment width to segment length
SEGMENT_RATIO = 0.20   


def _horizontal_segment(width, length):
    """ Produces the polygon for a horizontal segment """
    h = width / 2
    return ((0, h), (h, 0), (length - h, 0), (length, h), (length - h, width), (h, width))
    
def _vertical_segment(width, length):
    """ Produces the polygon for a vertical segment """
    h = width / 2
    return ((0, h), (h, 0), (width, h), (width, length - h), (h, length), (0, length - h))

def _segment_H(width, length):
    """ Produces the polygon for the H segment in a 14-segment display """
    hw = width / 2
    hl = length / 2
    pad = math.ceil(0.2 * width)
    return ((0, 0), (hw, 0), (hl - hw, length - hw), (hl - hw, length - pad), (hl - 2*hw, length - pad), (0, hw))

def _segment_I(width, length):
    """ Produces the polygon for the I segment in a 14-segment display """
    h = width / 2
    pad = math.ceil(0.2 * width)
    return ((0, pad), (width, pad), (width, length - h), (h, length), (0, length - h))

def _segment_J(width, length):
    """ Produces the polygon for the J segment in a 14-segment display """
    hw = width / 2
    hl = length / 2
    pad = math.ceil(0.2 * width)
    return ((hl - hw, 0), (hl - hw, hw), (hw, length - pad), (0, length - pad), (0, length - hw), (hl - 2*hw, 0))

def _segment_K(width, length):
    """ Produces the polygon for the K segment in a 14-segment display """
    hw = width / 2
    hl = length / 2
    pad = math.ceil(0.2 * width)
    return ((1, 0 + pad), (1 + hw, 0 + pad), (hl - hw, length - hw), (hl - hw, length), (hl - 2*hw, length), (1, hw))

def _segment_L(width, length):
    """ Produces the polygon for the L segment in a 14-segment display """
    h = width / 2
    pad = math.ceil(0.2 * width)
    return ((h, 0), (width, h), (width, length - pad), (0, length - pad), (0, h))        

def _segment_M(width, length):
    """ Produces the polygon for the M segment in a 14-segment display """
    hw = width / 2
    hl = length / 2
    pad = math.ceil(0.2 * width)
    return ((hl - hw, 0 + pad), (hl - hw, hw), (hw, length), (0, length), (0, length - hw), (hl - 2*hw, 0 + pad))
    
def _translate_polygon(polygon, xy):
    """ Performs an affine transformation to move the origin of the given polygon's coordinate frame """
    return tuple((pygame.math.Vector2(point) + xy for point in polygon))
    
def segment_length(segment_width):
    """ Computes the segment length given a segment width """
    return int(segment_width / SEGMENT_RATIO)

def char_width(segment_width):
    """ Computes the display character width given a segment width """
    return 2*segment_width + segment_length(segment_width)
    
def char_height(segment_width):
    """ Computes the display character height given a segment width """
    return 3*segment_width + 2*segment_length(segment_width)

def char_space(segment_width):
    """ Computes the space to allow between characters given a segment width """
    width = char_width(segment_width)
    return int(width/0.7 - width)

def word_space(segment_width):
    """ Computes the space to allow between words given a segment width """
    return 3 * char_space(segment_width)


class Display7Segment:
    """ Simulates a common 7-segment LED display """

    # Typical 7-segment displays assign a letter to each segment, starting with A
    # at the top, and continuing clockwise, and assigning G to the middle segment.
    # See https://en.wikipedia.org/wiki/Seven-segment_display for details.
    
    _PATTERNS = (
    # For each digit 0 to 9, we specify which of segments A..G are on
    #    A  B  C  D  E  F  G
        (1, 1, 1, 1, 1, 1, 0),   # digit 0
        (0, 1, 1, 0, 0, 0, 0),   # digit 1
        (1, 1, 0, 1, 1, 0, 1),   # digit 2
        (1, 1, 1, 1, 0, 0, 1),   # digit 3
        (0, 1, 1, 0, 0, 1, 1),   # digit 4
        (1, 0, 1, 1, 0, 1, 1),   # digit 5
        (1, 0, 1, 1, 1, 1, 1),   # digit 6
        (1, 1, 1, 0, 0, 0, 0),   # digit 7
        (1, 1, 1, 1, 1, 1, 1),   # digit 8
        (1, 1, 1, 1, 0, 1, 1),   # digit 9
    )    

    def __init__(self, surface, xy, segment_width, color):
        """ Initializes a 7-segment display instance.

        Args:
            surface: a pygame drawing surface
            xy: pygame coordinate pair (2-tuple or vector) for the top level corner
            segment_width: desired LED segment width
            color: a color name key as defined in COLORS
        """
        assert color in COLORS, "invalid color"
        self._surface = surface
        self._xy = xy
        self._color = color

        segment_len = segment_length(segment_width)
        horizontal_segment = _horizontal_segment(segment_width, segment_len)
        vertical_segment = _vertical_segment(segment_width, segment_len)

        self._segments = (
            _translate_polygon(horizontal_segment, (segment_width, 0)),
            _translate_polygon(vertical_segment, (segment_width + segment_len, segment_width)),
            _translate_polygon(vertical_segment, (segment_width + segment_len, 2*segment_width + segment_len)),
            _translate_polygon(horizontal_segment, (segment_width, 2*segment_width + 2*segment_len)),
            _translate_polygon(vertical_segment, (0, 2*segment_width + segment_len)),
            _translate_polygon(vertical_segment, (0, segment_width)),
            _translate_polygon(horizontal_segment, (segment_width, segment_width + segment_len)),
        )
    
    def draw(self, value: int):
        """ Draws the 7-segment display that corresponds to the given value

        Args:
            value (int): the value (modulo 10) to be displayed; blank display if None
        """
        if value is not None:
            value %= 10
            for i, on in enumerate(self._PATTERNS[value]):
                points = [pygame.math.Vector2(x,y) + self._xy for x, y in self._segments[i]]
                pygame.draw.polygon(self._surface, COLORS[self._color][on], points)
        else:
            for position in self._segments:
                points = [pygame.math.Vector2(x,y) + self._xy for x, y in position]
                pygame.draw.polygon(self._surface, COLORS[self._color][0], points)
            

class Display14Segment:
    """ Simulates a common 14-segment LED display """

    # Typical 14-segment displays assign a letter to each segment, starting with A
    # at the top, and continuing clockwise, and assigning G1 and G2 to the middle segment.
    # The interior segments are then assigned, starting with H at the top left, and
    # continuing clockwise through M.
    # See https://en.wikipedia.org/wiki/Fourteen-segment_display for details.

    _PATTERNS = (
    # For each letter A to Z, we specify which of segments A..M are on
    #    A  B  C  D  E  F  G1 G2 H  I  J  K  L  M
        (1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),    # letter A
        (1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0),    # letter B
        (1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),    # letter C
        (1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0),    # letter D
        (1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),    # letter E
        (1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),    # letter F
        (1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0),    # letter G
        (0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),    # letter H
        (1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0),    # letter I
        (0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),    # letter J
        (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0),    # letter K
        (0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),    # letter L
        (0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0),    # letter M
        (0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0),    # letter N
        (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),    # letter O
        (1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),    # letter P
        (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0),    # letter Q
        (1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0),    # letter R
        (1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0),    # letter S
        (1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0),    # letter T
        (0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),    # letter U
        (0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1),    # letter V
        (0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1),    # letter W
        (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1),    # letter X
        (0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0),    # letter Y
        (1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1),    # letter Z
    )    

    def __init__(self, surface, xy, segment_width, color):
        """ Initializes a 14-segment display instance.

        Args:
            surface: a pygame drawing surface
            xy: pygame coordinate pair (2-tuple or vector) for the top level corner
            segment_width: desired LED segment width
            color: a color name key as defined in COLORS
        """
        assert color in COLORS, "invalid color"
        self._surface = surface
        self._xy = xy
        self._color = color

        segment_len = segment_length(segment_width)
        horizontal_segment = _horizontal_segment(segment_width, segment_len)
        half_segment = _horizontal_segment(segment_width, segment_len / 2)
        vertical_segment = _vertical_segment(segment_width, segment_len)

        self._segments = (
            _translate_polygon(horizontal_segment, (segment_width, 0)),
            _translate_polygon(vertical_segment, (segment_width + segment_len, segment_width)),
            _translate_polygon(vertical_segment, (segment_width + segment_len, 2*segment_width + segment_len)),
            _translate_polygon(horizontal_segment, (segment_width, 2*segment_width + 2*segment_len)),
            _translate_polygon(vertical_segment, (0, 2*segment_width + segment_len)),
            _translate_polygon(vertical_segment, (0, segment_width)),
            _translate_polygon(half_segment, (segment_width, segment_width + segment_len)),
            _translate_polygon(half_segment, (segment_width + segment_len / 2, segment_width + segment_len)),
            _translate_polygon(_segment_H(segment_width, segment_len),
                               (segment_width, segment_width)),
            _translate_polygon(_segment_I(segment_width, segment_len), 
                               (segment_width + segment_len/2 - segment_width/2, segment_width)),
            _translate_polygon(_segment_J(segment_width, segment_len), 
                               (segment_width + segment_len/2 + segment_width/2, segment_width)),
            _translate_polygon(_segment_K(segment_width, segment_len), 
                               (segment_width + segment_len/2 + segment_width/2, 2*segment_width + segment_len)),
            _translate_polygon(_segment_L(segment_width, segment_len),
                               (segment_width + segment_len/2 - segment_width/2, 2*segment_width + segment_len)),
            _translate_polygon(_segment_M(segment_width, segment_len),
                               (segment_width, 2*segment_width + segment_len)),
        )

    def draw(self, value):
        """ Draws the 14-segment display that corresponds to the given value

        Args:
            value (int or str): the value to be displayed; if an int, it is interpreted as 
                an index the into the set of patterns; if a non-empty string, the first 
                character of the string must be a letter A..Z; blank display if None or empty string
        """

        if isinstance(value, str):
            if str:
                value = ord(value[0])
                if value < ord('A') or value > ord('Z'):
                    raise ValueError("requires a letter from A..Z")
                value -= ord('A')
            else:
                value = None
    
        if value is not None:
            value %= 26
            for i, on in enumerate(self._PATTERNS[value]):
                segment = self._segments[i]
                if segment:
                    points = [pygame.math.Vector2(x,y) + self._xy for x, y in segment]
                    pygame.draw.polygon(self._surface, COLORS[self._color][on], points)
        else:
            for segment in self._segments:
                if segment:
                    points = [pygame.math.Vector2(x,y) + self._xy for x, y in segment]
                    pygame.draw.polygon(self._surface, COLORS[self._color][0], points)


class Colon:
    """ Simulates a colon on an LED display """

    def __init__(self, surface, xy, segment_width, on, color):
        """ Initializes a colon display.

        Args:
            surface: pygame drawing surface
            xy: pygame coordinate pair (2-tuple or vector) for the top level corner
            segment_width: desired LED segment width
            on: boolean specifying whether the colon should be displayed in the "on" state
            color: a color name key as defined in COLORS
        """
        assert color in COLORS, "invalid color"
        self.segment_width = segment_width
        self._surface = surface
        dy = char_height(segment_width)//2 - 2*segment_width
        self._xy = (xy[0], xy[1] + dy)
        self._on = on
        self._color = color
        
    def draw(self):
        """ Draws the colon on the configured surface """
        square = pygame.Rect(0, 0, self.segment_width, self.segment_width)
        pygame.draw.rect(self._surface, COLORS[self._color][self._on], square.move(self._xy))
        pygame.draw.rect(self._surface, COLORS[self._color][self._on], 
                         square.move((self._xy[0], self._xy[1] + 3*self.segment_width)))