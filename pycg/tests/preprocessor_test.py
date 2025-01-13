import ast
from unittest import TestCase
from pycg.processing.preprocessor import PreProcessor

class PreProcessorTest(TestCase):
    def setUp(self):
        self.preprocessor = PreProcessor(
            filename="pycg/tests/preprocessor_test.py",
            modname="test",
            modules_analyzed=set(),
            import_manager=None,
            scope_manager=None,
            def_manager=None,
            class_manager=None,
            module_manager=None
        )

    def test_get_fun_defaults_positional(self):
        pos_defaults_function_def = """
        def func(a, b=1, c="test"):
            pass
        """.lstrip()
        node = ast.parse(pos_defaults_function_def).body[0]

        defaults = self.preprocessor._get_fun_defaults(node)

        self.assertEqual(defaults["b"], [1])
        self.assertEqual(defaults["c"], ["test"])

    def test_get_fun_defaults_typed_positional(self):
        typed_defaults_function_def = """
        def func(a, b: str | int = 1):
            pass
        """.lstrip()
        node = ast.parse(typed_defaults_function_def).body[0]

        defaults = self.preprocessor._get_fun_defaults(node)

        self.assertEqual(defaults["b"], [1])

    def test_get_fun_defaults_keyword(self):
        kwonly_function_def = """
        def func(kw1=True, kw2=42):
            pass
        """.lstrip()
        node = ast.parse(kwonly_function_def).body[0]

        defaults = self.preprocessor._get_fun_defaults(node)

        self.assertEqual(defaults["kw1"], [True])
        self.assertEqual(defaults["kw2"], [42])

    def test_get_fun_defaults_positional_and_keyword(self):
        pos_and_kw_arg_function_def = """
        def func(a, b=1, *, kw1="test", kw2=False, kw3: str | None = None):
            pass
        """.lstrip()
        node = ast.parse(pos_and_kw_arg_function_def).body[0]

        defaults = self.preprocessor._get_fun_defaults(node)

        self.assertEqual(defaults["b"], [1])
        self.assertEqual(defaults["kw1"], ["test"])
        self.assertEqual(defaults["kw2"], [False])
        self.assertEqual(defaults["kw3"], [None])

    def test_get_fun_defaults_none(self):
        no_defaults_function_def = """
        def func(a, b):
            pass
        """.lstrip()
        node = ast.parse(no_defaults_function_def).body[0]

        defaults = self.preprocessor._get_fun_defaults(node)

        self.assertEqual(defaults, {})
