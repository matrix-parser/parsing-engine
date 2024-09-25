from dataclasses import dataclass
import pickle


@dataclass
class Vertex:
    x: int
    y: int


@dataclass
class BoundingBox:
    topleft: Vertex
    topright: Vertex
    bottomleft: Vertex
    bottomright: Vertex


@dataclass
class Word:
    text: str
    origin: Vertex
    bounding_box: BoundingBox


class OCR:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.perform_ocr()

    def perform_ocr(self):
        with open(
            self.pdf_path.replace("test_pdfs", "test_pdfs/cache").replace(
                ".pdf", ".pkl"
            ),
            "rb",
        ) as f:
            self.annotations = pickle.load(f)

    def get_words(self):

        return


if __name__ == "__main__":
    ocr = OCR("test_pdfs/assignment.pdf")
    print(ocr.annotations)
