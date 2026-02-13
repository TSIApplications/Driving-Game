import tempfile
import unittest
from pathlib import Path

from scripts.generate_starter_maps import generate
from world_explorer.map_loader import MapLoader


class MapPipelineTests(unittest.TestCase):
    def test_generate_and_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            countries = root / "countries.txt"
            countries.write_text("Aland\nBorduria\n", encoding="utf-8")
            maps_root = root / "maps"

            total = generate(countries, maps_root)
            self.assertEqual(total, 2)

            loader = MapLoader(maps_root)
            loaded = loader.load("Aland")
            self.assertEqual(loaded.country, "Aland")
            self.assertEqual(len(loaded.landmarks), 5)


if __name__ == "__main__":
    unittest.main()
