from dataclasses import dataclass
import pickle


@dataclass
class Vertex:
    x: int
    y: int

    def __add__(self, o):
        return Vertex(x = o.x + self.x, y = o.y + self.y)



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
    words = ocr.get_words()
    print(words)

