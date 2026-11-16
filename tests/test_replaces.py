"""Tests for `replaces` (ADR 0080): the list per package, the check across entries, the retired list, the XML."""
import unittest
import xml.etree.ElementTree as ET

from support import GOOD, S, build, messages, problems, with_

OTHER = {**GOOD, "id": "fs-y", "name": "Y", "repo": "FreeSynergy/fs-y", "asset": "fs-y-{version}-linux-x86_64.tar.gz"}


def catalog_errors(packages, retired=None):
    return " | ".join(str(i) for i in S.check_catalog(packages, retired) if i.error)


class Replaces(unittest.TestCase):
    def test_valid_replaces_is_green(self):
        self.assertEqual(problems(with_(replaces=["fs-old"])), [])
        self.assertEqual(catalog_errors([with_(replaces=["fs-old"]), OTHER]), "")

    def test_no_replaces_is_green(self):
        self.assertEqual(catalog_errors([GOOD, OTHER]), "")

    def test_name_in_replaces_and_as_own_entry_is_red(self):
        both = [with_(replaces=["fs-y"]), OTHER]
        self.assertIn("also an entry of its own", catalog_errors(both))
        self.assertEqual(catalog_errors([with_(replaces=["fs-gone"]), OTHER]), "")  # counter-test: the same without the entry

    def test_own_id_in_replaces_is_red(self):
        self.assertIn("itself", messages(with_(replaces=["fs-x"])))

    def test_form_errors(self):
        self.assertIn("replaces", messages(with_(replaces="fs-old")))
        self.assertIn("replaces", messages(with_(replaces=[])))
        self.assertIn("replaces", messages(with_(replaces=["Fs Old"])))
        self.assertIn("replaces", messages(with_(replaces=[7])))
        self.assertIn("twice", messages(with_(replaces=["fs-old", "fs-old"])))

    def test_needs_schema_2(self):
        self.assertIn("schema = 2", messages(with_(replaces=["fs-old"]), schema=1))

    def test_two_entries_cannot_take_over_the_same_name(self):
        self.assertIn("already replaced", catalog_errors([with_(replaces=["fs-old"]), {**OTHER, "replaces": ["fs-old"]}]))

    def test_duplicate_ids_are_red(self):
        self.assertIn("more than one", catalog_errors([GOOD, GOOD]))

    def test_retired_list(self):
        retired = S.parse_retired("# comment\nfs-old -> fs-x  # renamed\nfs-a -> fs-b\n")
        self.assertEqual(retired, {"fs-old", "fs-a"})
        self.assertEqual(catalog_errors([with_(replaces=["fs-old"])], retired), "")
        warned = [str(i) for i in S.check_catalog([with_(replaces=["fs-unlisted"])], retired) if not i.error]
        self.assertTrue(any("retired-names" in w for w in warned))  # not on the list: a warning only
        self.assertIn("retired name", catalog_errors([with_(id="fs-old")], retired))  # a retired name is not given out again

    def test_xml_names_the_old_id(self):
        root = ET.fromstring(f"<c>{build(with_(replaces=['fs-old', 'fs-older']))}</c>")
        self.assertEqual([e.text for e in root.findall("./component/replaces/id")], ["fs-old", "fs-older"])
        self.assertEqual(ET.fromstring(f"<c>{build(GOOD)}</c>").findall("./component/replaces"), [])


if __name__ == "__main__":
    unittest.main()
