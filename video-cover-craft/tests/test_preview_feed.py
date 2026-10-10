"""Behavioral checks for portable previews and non-destructive feedback handoff."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preview_feed", ROOT / "scripts/preview_feed.py")
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.image = self.root / "original.png"
        Image.new("RGB", (320, 180), "green").save(self.image)
        self.digest = hashlib.sha256(self.image.read_bytes()).hexdigest()

    def tearDown(self):
        self.tmp.cleanup()

    def data(self, out):
        page = (out / "feed-preview.html").read_text()
        return json.loads(page.split('<script id="cover-data" type="application/json">')[1].split('</script>')[0])

    def test_portable_preview_keeps_original_bytes_and_resources(self):
        out = self.root / "preview"
        preview.create_preview([self.image], out)
        row = self.data(out)["images"][0]
        self.assertEqual(row["sha256"], self.digest)
        self.assertEqual(hashlib.sha256((out / row["file"]).read_bytes()).hexdigest(), self.digest)
        for name in ("feed-review.js", "feed-review.css"):
            self.assertEqual((out / "preview-assets" / name).read_bytes(), (ROOT / "assets" / name).read_bytes())
        self.assertEqual(hashlib.sha256(self.image.read_bytes()).hexdigest(), self.digest)

    def test_reject_overwrite_without_touching_previous_preview(self):
        out = self.root / "preview"
        preview.create_preview([self.image], out)
        (out / "sentinel").write_text("keep")
        with self.assertRaises(ValueError):
            preview.create_preview([self.image], out)
        self.assertEqual((out / "sentinel").read_text(), "keep")

    def test_title_and_feedback_cannot_break_out_of_json_script(self):
        text = '</script><script>alert("x")</script>&中文'
        feedback = self.root / "feedback.json"
        feedback.write_text(json.dumps({"schema_version": 1, "kind": "covercraft-feedback", "images": [
            {"image_sha256": self.digest, "notes": [], "label": text}]}))
        out = self.root / "preview"
        preview.create_preview([self.image], out, text, [text], feedback)
        data = self.data(out)
        self.assertEqual(data["videoTitle"], text)
        self.assertEqual(data["feedback"]["images"][0]["label"], text)
        self.assertNotIn(text, (out / "feed-preview.html").read_text())

    def test_feedback_invalid_shape_rejected_before_output(self):
        bad = self.root / "bad.json"
        for value in ([], {"schema_version": 99}, {"schema_version": 1, "kind": "covercraft-feedback", "images": [{"image_sha256": "wrong", "notes": []}]}):
            bad.write_text(json.dumps(value))
            with self.assertRaises(ValueError):
                preview.create_preview([self.image], self.root / "preview", feedback=bad)
            self.assertFalse((self.root / "preview").exists())

    def test_image_hash_survives_label_and_directory_change(self):
        preview.create_preview([self.image], self.root / "a", labels=["初稿"])
        preview.create_preview([self.image], self.root / "b", labels=["修改前"])
        self.assertEqual(self.data(self.root / "a")["images"][0]["sha256"], self.data(self.root / "b")["images"][0]["sha256"])

    def test_invalid_image_leaves_no_partial_output(self):
        bad = self.root / "bad.png"
        bad.write_bytes(b"not an image")
        with self.assertRaises((ValueError, OSError)):
            preview.create_preview([self.image, bad], self.root / "preview")
        self.assertFalse((self.root / "preview").exists())

    def test_revision_target_and_previous_are_explicit_not_input_order(self):
        after = self.root / "after.png"
        Image.new("RGB", (320, 180), "blue").save(after)
        preview.create_preview([after, self.image], self.root / "revision",
                               current_image=after, previous_image=self.image)
        data = self.data(self.root / "revision")
        self.assertEqual(data["currentImageSha256"], hashlib.sha256(after.read_bytes()).hexdigest())
        self.assertEqual(data["previousImageSha256"], self.digest)
        self.assertEqual(data["previewMode"], "revision")

    def test_independent_candidates_do_not_get_a_guessed_latest_version(self):
        second = self.root / "other.png"
        Image.new("RGB", (320, 180), "blue").save(second)
        preview.create_preview([self.image, second], self.root / "candidates")
        data = self.data(self.root / "candidates")
        self.assertIsNone(data["currentImageSha256"])
        self.assertEqual(data["previewMode"], "candidates")

    def test_revision_target_must_be_in_input_and_different_from_previous(self):
        outside = self.root / "outside.png"
        Image.new("RGB", (320, 180), "blue").save(outside)
        for options in ({"current_image": outside},
                        {"previous_image": self.image},
                        {"current_image": self.image, "previous_image": self.image}):
            with self.assertRaises(ValueError):
                preview.create_preview([self.image], self.root / "bad-target", **options)
            self.assertFalse((self.root / "bad-target").exists())

    def test_exif_orientation_uses_display_coordinates(self):
        rotated = self.root / "rotated.jpg"
        exif = Image.Exif()
        exif[274] = 6
        Image.new("RGB", (180, 320), "blue").save(rotated, exif=exif)
        preview.create_preview([rotated], self.root / "preview")
        self.assertEqual(self.data(self.root / "preview")["images"][0]["size"], [320, 180])


if __name__ == "__main__":
    unittest.main()
