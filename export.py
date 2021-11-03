import sys
from notion.client import NotionClient
from md2notion.upload import convert, uploadBlock
# from notion.block import PageBlock
# from md2notion.upload import upload

if len(sys.argv) < 2:
    sys.exit("Give me an url")

client = NotionClient(token_v2="983c97739c1626bf9769b9e3a4149d82953ec0e70f0a1f94709bf7e4eee378006b375088b3d0d225a6902b01289e64eb6c14ea5017b1c0f8a7c805b0bbaa969a7f7a48873a42c236a59f44808bb9")
block = "https://www.notion.so/Influxdb-686f0c30998d46efa7a216e42a0e1f8d"
page = client.get_block(sys.argv[1])

with open("./influxdb.md", "r", encoding="utf-8") as mdFile:
    rendered = convert(mdFile)
    for blockDescriptor in rendered:
        uploadBlock(blockDescriptor, page, mdFile.name)
    # newPage = page.children.add_new(PageBlock, title="TestMarkdown Upload")
    # upload(mdFile, newPage) #Appends the converted contents of TestMarkdown.md to newPage
