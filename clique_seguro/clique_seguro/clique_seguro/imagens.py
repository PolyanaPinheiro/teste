# imagens.py

# Criamos um dicionário onde a "chave" é o ID do tutorial 
# e o "valor" são os dados da imagem e seus respectivos círculos (hotspots).
# imagens.py

DADOS_TUTORIAIS = {
    'identificar-golpes': {
        # Passo 1: Foto da tela de chamada recebida (Spam)
        1: {
            'arquivo': '/static/IMG/spam_suspeito.jpg',
            'hotspots': [
                {
                    'x': 66.0,
                    'y': 80.2,
                    'pulse': True,
                    'tipo': 'circulo',
                    # 'label': 'Clique aqui para recusar a ligação'
                }
            ]
        },
        # Passo 2: Foto diferente (ex: mostrando o botão de bloquear número)
        2: {
            'arquivo': '/static/IMG/botao_bloquear.jpg',
            'hotspots': [
                {
                    'x': 50.0,
                    'y': 70.0,
                    'pulse': True,
                    'tipo': 'circulo',
                    # 'label': 'Toque em Bloquear para não ligarem mais'
                }
            ]
        }
    },
    
    'tirar-foto': {
        1: {
            'arquivo': '/static/IMG/abrir_camera.jpg',
            'hotspots': [{
                'x': 60.0,
                'y': 70.0, 
                'pulse': True,
                'tipo': 'circulo',
                }]
        },
        2: {
            'arquivo': '/static/IMG/mirar_foto.jpg',
            'hotspots': [{
                'x': 58.0, 
                'y': 60.0,
                'pulse': True,
                'tipo': 'quadrado',
                'largura': 80,  #px
                'altura': 100
                }]
        },
        3: {
            'arquivo': '/static/IMG/mirar_foto.jpg',
            'hotspots': [{
                'x': 50.0, 
                'y': 85.0, 
                'pulse': True, 
                'tipo': 'circulo'
            }]
        }
    }
}