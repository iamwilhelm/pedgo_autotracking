import unittest
from autotrack import tracked, memoize_function

class TestSignals(unittest.TestCase):

    def test_split(self):
        # Example Class using @tracked
        class Example:
            @tracked(1)
            def count_A(self):
                pass

            @tracked(2)
            def count_B(self):
                pass

        # Example Usage
        example = Example()

        # A -> C -\
        # B -> D --> E

        @memoize_function
        def get_A():
            return example.count_A

        @memoize_function
        def get_B():
            return example.count_B

        @memoize_function
        def get_C():
            return 2 * get_A() # 8

        @memoize_function
        def get_D():
            return 3 * get_B() # 6

        @memoize_function
        def get_E():
            return get_C() + get_D()

        # Initial Access
        self.assertEqual(get_E(), 8)
        print("---")
        self.assertEqual(get_E(), 8)
        print("---")

        # Update count
        example.count_A = 2

        # Access after Update
        self.assertEqual(get_E(), 10)

        example.count_A = 4
        self.assertEqual(get_E(), 14)

    def test_auto_track(self):
        # Example Class using @tracked
        class Example:
            @tracked(1)
            def count(self):
                pass

            @tracked(2)
            def count2(self):
                pass

        # Example Usage
        example = Example()

        # E -> F --\
        # A -> B --\
        #  \-> C --> D

        # First memoized function depends on count (A)
        @memoize_function
        def get_A():
            return example.count + 2

        # (E)
        @memoize_function
        def get_E():
            return example.count2 + 4

        # (F)
        @memoize_function
        def get_F():
            return get_E()**2

        # Second memoized function depends on get_count (B)
        @memoize_function
        def get_B():
            return get_A() * 2

        # (C)
        @memoize_function
        def get_C():
            return get_A() * 3

        # (D)
        @memoize_function
        def get_D():
            return get_B() + get_C() + get_F()

        # Initial Access
        self.assertEqual(get_D(), 51)
        print("---")
        self.assertEqual(get_D(), 51)
        print("---")

        # Update count
        example.count = 2

        # Access after Update
        self.assertEqual(get_D(), 56)

        example.count = 4
        self.assertEqual(get_D(), 66)

if __name__ == '__main__':
    unittest.main()
