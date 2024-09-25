import Parser

Parser.set_pdf("test_pdfs/invoice.pdf")
Parser.query("set quantity_minimum = 2")
Parser.query(
    "select keys from words as word where 180 < word.center.x < 200 and word.center.y > 800"
)
Parser.query(
    "select prices from words as word where 1000 < word.center.x < 1200 and 1100 > word.center.y > 800"
)
Parser.query(
    "select quantities from keys as key where int(key.text) > quantity_minimum"
)
Parser.query("export keys as keys")
Parser.query("export quantities as quantities")
Parser.query("export prices as prices")
Parser.query("end")
