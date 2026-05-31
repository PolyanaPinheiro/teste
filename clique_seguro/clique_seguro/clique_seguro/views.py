from django.shortcuts import render, redirect

# ==========================================
# 1. PÁGINAS PRINCIPAIS E AUTENTICAÇÃO
# ==========================================

def home_view(request):
    """Renderiza a página inicial (Homepage)."""
    context = {
        'is_logged_in': False, # Mude para True para testar o botão de Perfil na Navbar
        'username': 'Poliana'
    }
    return render(request, 'homepage.html', context)

def login_view(request):
    """Processa o Login."""
    if request.method == 'POST':
        # Aqui entra a futura lógica de autenticação do Django
        return redirect('home')
    return render(request, 'login.html')

def register_view(request):
    """Processa o Registo de novos utilizadores."""
    if request.method == 'POST':
        # Aqui entra a futura lógica de criação de utilizador
        return redirect('login')
    return render(request, 'register.html')


# ==========================================
# 2. CATEGORIAS E TUTORIAIS
# ==========================================

def get_categories_db():
    """Simula o banco de dados das 4 categorias principais com as cores do design."""
    return {
        'ferramentas-celular': {
            'id': 'ferramentas-celular',
            'name': 'Ferramentas do Celular',
            'subtitle': 'Escolha um tutorial abaixo para começar a aprender',
            'color': 'bg-gradient-to-br from-blue-500 to-blue-600',
            'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="w-full h-full text-white"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg>'
        },
        'comunicacao': {
            'id': 'comunicacao',
            'name': 'Comunicação',
            'subtitle': 'Escolha um tutorial abaixo para começar a aprender',
            'color': 'bg-gradient-to-br from-green-500 to-green-600',
            'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="w-full h-full text-white"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
        },
        'golpes-seguranca': {
            'id': 'golpes-seguranca',
            'name': 'Golpes e Segurança',
            'subtitle': 'Escolha um tutorial abaixo para começar a aprender',
            'color': 'bg-gradient-to-br from-orange-500 to-orange-600',
            'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="w-full h-full text-white"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>'
        },
        'financas-banco': {
            'id': 'financas-banco',
            'name': 'Finanças e Bancos', 
            'subtitle': 'Escolha um tutorial abaixo para começar a aprender',
            'color': 'bg-gradient-to-br from-purple-500 to-purple-600',
            'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="w-full h-full text-white"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>'
        }
    }

def category_page(request, category_id):
    """Renderiza a página de uma Categoria específica com a sua lista de tutoriais."""
    db = get_categories_db()
    category = db.get(category_id)
    
    if not category:
        return redirect('home')

    # Lista de tutoriais baseada nas fotos que enviou
    tutorials = []

    if category_id == 'ferramentas-celular':
        tutorials = [
            {'id': 'tirar-foto', 'title': 'Como tirar Foto', 'desc': 'Aprenda a usar a câmera do seu celular', 'icon': 'camera'},
            {'id': 'pesquisar-apps', 'title': 'Como pesquisar Aplicativos', 'desc': 'Encontre e instale novos aplicativos', 'icon': 'search'},
            {'id': 'iluminacao-tela', 'title': 'Como mudar a iluminação da tela?', 'desc': 'Ajuste o brilho para ver melhor', 'icon': 'sun'},
            {'id': 'bluetooth', 'title': 'Como conectar com o Bluetooth', 'desc': 'Conecte fones e outros dispositivos', 'icon': 'bluetooth'},
            {'id': 'configuracoes', 'title': 'Como usar o Painel de Configurações', 'desc': 'Ajuste as configurações do celular', 'icon': 'settings'},
            {'id': 'despertador', 'title': 'Como colocar o despertar?', 'desc': 'Configure alarmes e despertador', 'icon': 'alarm-clock'},
            {'id': 'navegacao-basica', 'title': 'Navegação básica do celular', 'desc': 'Como usar os três botões da barra inferior', 'icon': 'smartphone'},
            {'id': 'organizar-icones', 'title': 'Como organizar ícones', 'desc': 'Organize sua tela inicial', 'icon': 'layout-grid'},
            {'id': 'ver-fotos', 'title': 'Como ver fotos', 'desc': 'Acesse e visualize suas fotos', 'icon': 'image'},
        ]
    elif category_id == 'financas-banco':
        tutorials = [
            {'id': 'usar-pix', 'title': 'Como usar o Pix', 'desc': 'Transfira dinheiro rapidamente', 'icon': 'dollar-sign'},
            {'id': 'app-banco', 'title': 'Como usar o aplicativo do banco', 'desc': 'Acesse sua conta pelo celular', 'icon': 'landmark'},
            {'id': 'pagar-boletos', 'title': 'Como pagar boletos', 'desc': 'Pague contas pelo celular', 'icon': 'barcode'},
            {'id': 'verificar-saldo', 'title': 'Como verificar saldo', 'desc': 'Consulte seu dinheiro disponível', 'icon': 'wallet'},
            {'id': 'compras-online', 'title': 'Como fazer compras online', 'desc': 'Compre com segurança pela internet', 'icon': 'shopping-cart'},
        ]
    elif category_id == 'golpes-seguranca':
        tutorials = [
            {'id': 'identificar-golpes', 'title': 'Como identificar golpes', 'desc': 'Reconheça tentativas de fraude', 'icon': 'alert-triangle'},
            {'id': 'senhas-seguras', 'title': 'Como criar senhas seguras', 'desc': 'Proteja suas contas', 'icon': 'lock'},
            {'id': 'links-suspeitos', 'title': 'Cuidado com links suspeitos', 'desc': 'Não clique em qualquer link', 'icon': 'mouse-pointer-click'},
            {'id': 'autenticacao-2-etapas', 'title': 'Autenticação em duas etapas', 'desc': 'Deixe suas contas mais seguras', 'icon': 'key'},
            {'id': 'golpes-whatsapp', 'title': 'Golpes no WhatsApp', 'desc': 'Proteja-se de mensagens falsas', 'icon': 'message-square'},
        ]
    elif category_id == 'comunicacao':
        tutorials = [
            {'id': 'fazer-ligacao', 'title': 'Como fazer uma ligação', 'desc': 'Ligue para seus contatos', 'icon': 'phone'},
            {'id': 'enviar-mensagem', 'title': 'Como enviar uma mensagem', 'desc': 'Envie SMS e mensagens de texto', 'icon': 'mail'},
            {'id': 'usar-whatsapp', 'title': 'Como usar o WhatsApp', 'desc': 'Converse com amigos e família', 'icon': 'message-circle'},
            {'id': 'videochamada', 'title': 'Como fazer videochamada', 'desc': 'Conecte fones e outros dispositivos', 'icon': 'video'},
            {'id': 'enviar-email', 'title': 'Como enviar e-mail', 'desc': 'Use o correio eletrônico', 'icon': 'at-sign'},
            {'id': 'adicionar-contatos', 'title': 'Como adicionar contatos', 'desc': 'Salve números importantes', 'icon': 'user-plus'},
        ]

    context = {
        'category': category,
        'tutorials': tutorials
    }
    return render(request, 'category_page.html', context)

def tutorial_page(request, category_id, tutorial_id):
    """Renderiza os passos de um tutorial específico."""
    db = get_categories_db()
    category = db.get(category_id)
    
    if not category:
        return redirect('home')

    # Simulando os passos do tutorial selecionado
    steps = [
        {
            'id': 1,
            'title': 'Identifique o número desconhecido',
            'description': 'Quando o seu telemóvel tocar, olhe para o ecrã. Se aparecer "Spam suspeito" ou um número muito estranho, tenha cuidado.',
            'tips': 'Nunca atenda ligações de números marcados como spam suspeito pelo telemóvel.',
            'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-full h-full text-orange-600"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/><path d="M14.05 2a9 9 0 0 1 8 7.94"/><path d="M14.05 6A5 5 0 0 1 18 10"/></svg>',
            # AQUI ESTÁ A MUDANÇA: Apontando para a imagem que você enviou
            'interactiveImage': '/static/IMG/spam_suspeito.jpg', 
            'imageHotspots': []
        },
        {
            'id': 2,
            'title': 'Toque no botão vermelho para recusar',
            'description': 'Para não atender a ligação, toque no botão vermelho. Ele costuma ficar no canto inferior esquerdo.',
            'tips': 'Ao recusar, a pessoa não tem qualquer acesso ao seu telemóvel.',
            'icon_svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-full h-full text-red-600"><path d="M10.68 13.31a16 16 0 0 0 3.41 2.6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7 2 2 0 0 1 1.72 2v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.42 19.42 0 0 1-3.33-2.67m-2.67-3.34a19.79 19.79 0 0 1-3.07-8.63A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91"/><line x1="22" y1="2" x2="2" y2="22"/></svg>',
        }
    ]

    context = {
        'category': category,
        'tutorial': {'title': 'Como Identificar Ligações Suspeitas'},
        'steps': steps
    }
    return render(request, 'tutorial_page.html', context)


# ==========================================
# 3. DICIONÁRIO E PROGRESSO
# ==========================================

def dictionary_menu(request):
    """Renderiza o menu principal do dicionário."""
    return render(request, 'dictionary_menu.html')

def dictionary_icons(request):
    """Renderiza o dicionário de ícones."""
    icon_categories = [
        {
            'name': 'Comunicação Básica',
            'icons': [
                {
                    'name': 'Telefone Verde',
                    'meaning': 'Serve para atender uma chamada ou iniciar uma nova ligação.',
                    'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
                }
            ]
        }
    ]
    return render(request, 'dictionary_icons.html', {'icon_categories': icon_categories})

def dictionary_words(request):
    """Renderiza o dicionário de palavras."""
    words_data = [
        {
            'word': 'App (Aplicação)',
            'definition': 'Um programa que instala no telemóvel para fazer algo específico.',
            'example': 'Exemplo: "Vou descarregar a app do banco para ver o saldo."'
        },
        {
            'word': 'Wi-Fi',
            'definition': 'Internet sem fios. Permite que o telemóvel se ligue à internet sem gastar dados móveis.',
            'example': 'Exemplo: "Estou ligado ao Wi-Fi de casa."'
        }
    ]
    return render(request, 'dictionary_words.html', {'words': words_data})

def user_progress_view(request):
    """Processa e renderiza as estatísticas do perfil do utilizador."""
    total_tutorials = 24
    completed_tutorials = 8
    progress_percentage = round((completed_tutorials / total_tutorials) * 100) if total_tutorials > 0 else 0
    
    color_map = {
        'blue': 'bg-blue-500', 'green': 'bg-green-500',
        'orange': 'bg-orange-500', 'purple': 'bg-purple-500',
    }
    
    categories_raw = [
        {'name': 'Ferramentas do Telemóvel', 'completed': 3, 'total': 6, 'color': 'blue'},
        {'name': 'Comunicação', 'completed': 2, 'total': 6, 'color': 'green'},
        {'name': 'Golpes e Segurança', 'completed': 2, 'total': 6, 'color': 'orange'},
        {'name': 'Contas e Bancos', 'completed': 1, 'total': 6, 'color': 'purple'},
    ]
    
    categories = []
    for cat in categories_raw:
        percent = round((cat['completed'] / cat['total']) * 100) if cat['total'] > 0 else 0
        categories.append({
            'name': cat['name'], 'completed': cat['completed'], 'total': cat['total'],
            'percentage': percent, 'color_class': color_map.get(cat['color'], 'bg-gray-500')
        })

    recent_completions = ['Como Fazer uma Ligação', 'Como Tirar uma Foto']

    context = {
        'username': 'Poliana',
        'total_tutorials': total_tutorials,
        'completed_tutorials': completed_tutorials,
        'progress_percentage': progress_percentage,
        'categories': categories,
        'recent_completions': recent_completions
    }
    return render(request, 'user_progress.html', context)

def toggle_contrast(request):
    """Liga e desliga o modo de Alto Contraste na sessão."""
    # Inverte o valor: True vira False, e False vira True
    request.session['high_contrast'] = not request.session.get('high_contrast', False)
    
    # Redireciona o utilizador de volta para a mesma página em que ele clicou
    return redirect(request.META.get('HTTP_REFERER', 'home'))