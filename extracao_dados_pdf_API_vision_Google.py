#script para tratamento de arquivos pdfs escaneados conexão API com google vision cloud 
import os, io
import json
import re
from google.cloud import vision
from google.cloud import storage
from bs4 import BeautifulSoup

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\Andreia.siqueira\Desktop\CXP\CXP\LUMERA OCR WKS\fleet-garage-382714-ee832074e3e0.json"

# Instânciando o cliente 
client = vision.ImageAnnotatorClient( )

batch_size=2

mime_type = 'application/pdf'
feature = vision.Feature(
    type=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

# The name of the image file to annotate
file_name = os.path.abspath(r"C:\Users\Andreia.siqueira\Desktop\Captalys\__Contracts\Novos Contratos Sociais\ContrSoc98\ddb60fc2-1ff9-4c60-b3be-19bab5265543 ContratoSocial1.pdf")

# # Loads the image into memory
with io.open(r"C:\Users\Andreia.siqueira\Desktop\Captalys\__Contracts\Novos Contratos Sociais\ContrSoc306\Ata_Estatuto_COnstituicao_LUFT.pdf",'rb') as image_file:
     content = image_file.read()

input_config = vision.InputConfig(content=content, mime_type=mime_type)

gcs_source = vision.GcsSource(uri='gs://matriculas_lumera/ddb60fc2-1ff9-4c60-b3be-19bab5265543 ContratoSocial1.pdf')
input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

gcs_destination = vision.GcsDestination(uri='gs://matriculas_lumera/pdf')
output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=50)


async_request = vision.AsyncAnnotateFileRequest(
    features=[feature], input_config=input_config, output_config=output_config)

operation = client.async_batch_annotate_files(
    requests=[async_request])


print('Waiting for the operation to finish.')
operation.result(timeout=420)

async_request = vision.AsyncAnnotateFileRequest(
    features=[feature], input_config=input_config, output_config=output_config)

operation = client.async_batch_annotate_files(
        requests=[async_request])

print('Waiting for the operation to finish.')
operation.result(timeout=420)

# Once the request has completed and the output has been
# written to GCS, we can list all the output files.
storage_client = storage.Client()

bucket = storage_client.get_bucket('matriculas_lumera')
# List objects with the given prefix, filtering out folders.
blob_list = [blob for blob in list(bucket.list_blobs(
        prefix='pdfoutput')) if not blob.name.endswith('/')]
print('Output files:')
for blob in blob_list:
    print(blob.name)
       
# Process the first output file from GCS.
# Since we specified batch_size=2, the first response contains
# the first two pages of the input file.
output = blob_list[0]
json_string = output.download_as_string()
response = json.loads(json_string)

# The actual response for the first page of the input file.
first_page_response = response['responses'][0]
annotation = first_page_response['fullTextAnnotation']

# Here we print the full text from the first page.
# The response contains more information:
# annotation/pages/blocks/paragraphs/words/symbols
# including confidence scores and bounding boxes
print('Full text:\n')
print(annotation['text'])
#print(soup.encode("utf-8"))   
with open(r"C:\Users\Andreia.siqueira\Desktop\Captalys\__Contracts\Novos Contratos Sociais\ContrSoc98\contrato_social98\teste.txt", 'w', encoding="utf-8") as text_file:
        for page in response['responses']:
                text_file.write(page['fullTextAnnotation']['text'])
                text_file.write('\n')

