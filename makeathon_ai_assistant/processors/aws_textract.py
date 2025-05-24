import boto3

def extract_text_textract(file_path):
    client = boto3.client("textract", region_name="us-east-1")

    with open(file_path, "rb") as document:
        image_bytes = document.read()

    response = client.detect_document_text(Document={'Bytes': image_bytes})

    text_lines = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text_lines.append(block['Text'])

    return "\n".join(text_lines)
