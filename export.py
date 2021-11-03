import sys
from mistletoe import markdown
from notion.client import NotionClient
from md2notion.upload import convert, uploadBlock
# from notion.block import PageBlock
# from md2notion.upload import upload

if len(sys.argv) < 3:
    sys.exit("Give me an url and a markdown file")

client = NotionClient(token_v2="983c97739c1626bf9769b9e3a4149d82953ec0e70f0a1f94709bf7e4eee378006b375088b3d0d225a6902b01289e64eb6c14ea5017b1c0f8a7c805b0bbaa969a7f7a48873a42c236a59f44808bb9")
block = sys.argv[1]
markdown_file=sys.argv[2]
page = client.get_block(block)

with open(markdown_file, "r", encoding="utf-8") as mdFile:
    rendered = convert(mdFile)
    for blockDescriptor in rendered:
        uploadBlock(blockDescriptor, page, mdFile.name)
    # newPage = page.children.add_new(PageBlock, title="TestMarkdown Upload")
    # upload(mdFile, newPage) #Appends the converted contents of TestMarkdown.md to newPage
