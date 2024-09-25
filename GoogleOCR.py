import io
from dataclasses import dataclass
from google.cloud import vision
from pdf2image import convert_from_path
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
    center: Vertex
    bounding_box: BoundingBox


class OCR:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.convert_to_images()
        self.client = vision.ImageAnnotatorClient.from_service_account_json(
            "./key.json"
        )
        self.perform_ocr()

    def convert_to_images(self):
        self.images = convert_from_path(self.pdf_path)

    def perform_ocr(self):
        for page, image in enumerate(self.images):
            byte_stream = io.BytesIO()
            image.save(byte_stream, format="PNG")
            vision_image = vision.Image(content=byte_stream.getvalue())
            response = self.client.text_detection(image=vision_image)
            annotations = response.text_annotations
            self.annotations = annotations

    def cache_annotations(self):
        with open(
            self.pdf_path.replace("test_pdfs", "test_pdfs/cache").replace(
                ".pdf", ".pkl"
            ),
            "wb",
        ) as f:
            output = []
            for annotation in self.annotations:
                text = annotation.description
                vertices = []
                for vertex in annotation.bounding_poly.vertices:
                    vertices.append((vertex.x, vertex.y))
                output.append({"text": text, "vertices": vertices})
            pickle.dump(output, f, pickle.HIGHEST_PROTOCOL)

    def get_words(self):
        words = []
        for annotation in self.annotations:
            text = annotation['text']
            vertices = annotation['vertices']
        
            # Assuming the vertices are ordered [topleft, topright, bottomright, bottomleft]
            topleft = Vertex(x=vertices[0][0], y=vertices[0][1])
            topright = Vertex(x=vertices[1][0], y=vertices[1][1])
            bottomright = Vertex(x=vertices[2][0], y=vertices[2][1])
            bottomleft = Vertex(x=vertices[3][0], y=vertices[3][1])
            
            center = topleft + topright + bottomleft + bottomright
            center.x /= 4
            center.y /= 4
            
            # Create BoundingBox object
            bounding_box = BoundingBox(
                topleft=topleft,
                topright=topright,
                bottomleft=bottomleft,
                bottomright=bottomright,
            )
            
            # Create Word object
            word = Word(text=text, center=center, bounding_box=bounding_box)
            words.append(word)
    
        return words


if __name__ == "__main__":
    ocr = OCR("test_pdfs/assignment.pdf")
    ocr.cache_annotations()

# def detect_text(path):
#     """Detects text in the file."""
#     client = vision.ImageAnnotatorClient()
#
#     with io.open(path, "rb") as image_file:
#         content = image_file.read()
#
#     image = vision.Image(content=content)
#
#     if response.error.message:
#         raise Exception(f"{response.error.message}")
#
#     print("Texts:")
#     for text in texts:
#         print('\n"{}"'.format(text.description))
#
#         vertices = [
#             "({},{})".format(vertex.x, vertex.y)
#             for vertex in text.bounding_poly.vertices
#         ]
#
#         print("bounds: {}".format(",".join(vertices)))


# detect_text("D:\hackbattle\invoice1.png")
