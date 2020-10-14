import boto3
import json

client = boto3.client('rekognition')
s3 = boto3.resource('s3')

def detecta_faces():
        faces_detectadas=client.index_faces( #index_faces() identifica as faces em uma imagem e adiciona o resultado em uma coleção
            CollectionId='faces',
            DetectionAttributes=['DEFAULT'],
            ExternalImageId='TEMPORARIA',
            Image={
                'S3Object': {
                    'Bucket': 'lambda-imagens',
                    'Name': '_analise.png',
                },
            },
        )
        return faces_detectadas

def cria_lista_faceId_detectadas(faces_detectadas):
    faceId_detectadas = []
    for imagens in range(len(faces_detectadas['FaceRecords'])):
        faceId_detectadas.append(faces_detectadas['FaceRecords'][imagens]['Face']['FaceId'])
    return faceId_detectadas

#compara uma imagem com as presentes no banco de dados
def compara_imagens(faceId_detectadas):
    resultado_comparacao = []
    for ids in faceId_detectadas:
        resultado_comparacao.append( #anexar
            client.search_faces( #search_faces() serve para pesquisar IDs em uma coleção
                CollectionId='faces',
                FaceId=ids,
                FaceMatchThreshold=80,
                MaxFaces=10,
            )
        )
    return resultado_comparacao

def gera_dados_json(resultado_comparacao): #para colocar em um site
    dados_json = []
    for face_matches in resultado_comparacao:
        if(len(face_matches.get('FaceMatches'))) >=1:
            perfil = dict(nome = face_matches['FaceMatches'][0]['Face']['ExternalImageId'], #construcao do dicionario
                          faceMatch=round(face_matches['FaceMatches'][0]['Similarity'], 2))
            dados_json.append(perfil)
    return dados_json

def publica_dados(dados_json):
    arquivo = s3.Object('website1-lambda', 'dados.json')
    arquivo.put(Body=json.dumps(dados_json))

def exclui_imagem_colecao(faceId_detectadas):
    client.delete_faces(
        CollectionId='faces',
        FaceIds=faceId_detectadas,
    )

def main(event, context):
    faces_detectadas = detecta_faces()
    faceId_detectadas = cria_lista_faceId_detectadas(faces_detectadas)
    resultado_comparacao = compara_imagens(faceId_detectadas)
    dados_json = gera_dados_json(resultado_comparacao)
    publica_dados(dados_json)
    exclui_imagem_colecao(faceId_detectadas)
    print(json.dumps(dados_json, indent=4))
    #print(faceId_detectadas) -- teste cria lista faceId detectadas
    #print(json.dumps(resultado_comparacao, indent=4)) --teste compara imagens. Com o json.dumps e pedido de indentação, fica mais fácil de identificar as hierarquias
    #print(json.dumps(faces_detectadas, indent=4))  --- teste faces detectadas

