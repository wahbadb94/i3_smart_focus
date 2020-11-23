import unittest
import focus_helpers
from i3ipc import Rect

from focus_helpers import is_left_of, is_right_of


# helper for building rects during testing
def rect_builder(x: int, y: int, width: int, height: int) -> Rect:
    return Rect(data={"x": x, "y": y, "width": width, "height": height})


class test_focus_helpers(unittest.TestCase):
    def test_is_left_of(self):
        # arrange

        # | t | r |
        # |   |   |
        ref1 = Rect({"x": 1292, "y": 19, "width": 1249, "height": 1378})
        target1 = Rect({"x": 19, "y": 19, "width": 1249, "height": 1378})

        # | t | r |
        # |   |```|
        ref2 = rect_builder(x=652, y=19, width=616, height=677)
        target2 = rect_builder(x=19, y=19, width=609, height=1378)

        # | t |___|
        # |   | r |
        ref3 = rect_builder(x=652, y=720, width=616, height=677)
        target3 = rect_builder(x=9, y=19, width=609, height=1378)

        # |___| r |
        # | t |```|
        ref4 = rect_builder(x=652, y=19, width=616, height=677)
        target4 = rect_builder(x=19, y=720, width=609, height=677)

        # act
        test1 = is_left_of(ref1, target1)
        test2 = is_left_of(ref2, target2)
        test3 = is_left_of(ref3, target3)
        test4 = is_left_of(ref4, target4)

        opposite1 = is_left_of(target1, ref1)
        opposite2 = is_left_of(target2, ref2)
        opposite3 = is_left_of(target3, ref3)
        opposite4 = is_left_of(target4, ref4)

        # assert
        self.assertTrue(test1, "basic horizonal split, target to the left")
        self.assertTrue(test2, "ref half height top right, target full height left")
        self.assertTrue(test3, "ref half height bottom, target full height left")
        self.assertTrue(
            test4, "ref half height top right, target half height bottom left"
        )
        self.assertFalse(opposite1)
        self.assertFalse(opposite2)
        self.assertFalse(opposite3)
        self.assertFalse(opposite4)

    def test_is_right_of(self):
        # arrange

        # | r | t |
        # |   |   |
        target1 = Rect({"x": 1292, "y": 19, "width": 1249, "height": 1378})
        ref1 = Rect({"x": 19, "y": 19, "width": 1249, "height": 1378})

        # | r | t |
        # |   |```|
        target2 = rect_builder(x=652, y=19, width=616, height=677)
        ref2 = rect_builder(x=19, y=19, width=609, height=1378)

        # | r |___|
        # |   | t |
        target3 = rect_builder(x=652, y=720, width=616, height=677)
        ref3 = rect_builder(x=9, y=19, width=609, height=1378)

        # | r |___|
        # |```| t |
        target5 = rect_builder(x=652, y=720, width=616, height=677)
        ref5 = rect_builder(x=9, y=19, width=609, height=677)

        # |___| t |
        # | r |```|
        target4 = rect_builder(x=652, y=19, width=616, height=677)
        ref4 = rect_builder(x=19, y=720, width=609, height=677)

        # |___r___|
        # |   | t |

        # act
        test1 = is_right_of(ref1, target1)
        test2 = is_right_of(ref2, target2)
        test3 = is_right_of(ref3, target3)
        test4 = is_right_of(ref4, target4)
        test5 = is_right_of(ref5, target5)

        opposite1 = is_right_of(target1, ref1)
        opposite2 = is_right_of(target2, ref2)
        opposite3 = is_right_of(target3, ref3)
        opposite4 = is_right_of(target4, ref4)
        opposite5 = is_right_of(target5, ref5)

        # assert
        self.assertTrue(test1, "basic horizonal split, target to the right")
        self.assertTrue(test2, "ref full height left, target half height top right")
        self.assertTrue(test3, "ref full height left, arget hald height bottom right")
        self.assertTrue(
            test4, "ref half height top left, target half height bottom right"
        )
        self.assertTrue(
            test5, "ref half height bottom left, target half height top right"
        )
        self.assertFalse(opposite1)
        self.assertFalse(opposite2)
        self.assertFalse(opposite3)
        self.assertFalse(opposite4)
        self.assertFalse(opposite5)
