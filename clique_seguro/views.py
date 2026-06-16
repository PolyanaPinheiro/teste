from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.models import Categoria, Tutorial, Passo, Progresso
from django.contrib.auth.models import User
from django.http import HttpResponse

# ==========================================
# 1. PÁGINAS PRINCIPAIS E AUTENTICAÇÃO
# ==========================================

def home_view(request):
    """Renderiza a página inicial (Homepage)."""
    context = {
        'is_logged_in': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else ''
    }
    return render(request, 'homepage.html', context)

def login_view(request):
    """Processa o Login usando E-mail."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('password')
        
        if not User.objects.filter(username=email).exists():
            return redirect('register')
        
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'Palavra-passe incorreta. Tente novamente.',
                'old_email': email
            })
            
    return render(request, 'login.html')

def logout_view(request):
    """Faz o logout do utilizador."""
    logout(request)
    return redirect('home')

def register_view(request):
    """Processa o Registo pedindo Nome e E-mail."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        nome = request.POST.get('first_name')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm_password')
        
        if senha != confirmar_senha:
            return render(request, 'register.html', {
                'error': 'As senhas não são iguais. Por favor, digite com calma e tente de novo.',
                'old_name': nome,
                'old_email': email
            })
            
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {
                'error': 'Este e-mail já está registado. Se já tem conta, clique em "Entrar".',
                'old_name': nome
            })
            
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=senha, 
            first_name=nome
        )
        login(request, user)
        return redirect('home')
        
    return render(request, 'register.html')

def criar_admin(request):
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='admin')
    user.set_password('senha123')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return HttpResponse('Admin pronto! Usuario: admin | Senha: senha123')
# ==========================================
# 2. CATEGORIAS E TUTORIAIS
# ==========================================

def how_to_use_view(request):
    """Renderiza a página 'Como Usar a Plataforma' com o ambiente de treino."""
    context = {
        'categories_info': [
            {'name': 'Ferramentas do Celular', 'description': 'Aprenda a usar as funções básicas do seu telemóvel.', 'emoji': '📱', 'bg': 'bg-blue-50 border-2 border-blue-200', 'hc_border': 'border-blue-400', 'example': 'Ex: Como ligar o Wi-Fi ou aumentar o volume.'},
            {'name': 'Comunicação', 'description': 'Fale com amigos e família através da internet.', 'emoji': '💬', 'bg': 'bg-green-50 border-2 border-green-200', 'hc_border': 'border-green-400', 'example': 'Ex: Como mandar uma mensagem de áudio.'},
            {'name': 'Golpes e Segurança', 'description': 'Aprenda a proteger-se de esquemas na internet.', 'emoji': '🛡️', 'bg': 'bg-orange-50 border-2 border-orange-200', 'hc_border': 'border-orange-400', 'example': 'Ex: Como identificar links falsos ou mensagens suspeitas.'},
            {'name': 'Finanças e Bancos', 'description': 'Use a aplicação do seu banco com confiança.', 'emoji': '💳', 'bg': 'bg-purple-50 border-2 border-purple-200', 'hc_border': 'border-purple-400', 'example': 'Ex: Como ver o saldo sem ir ao multibanco.'}
        ],
        'tutorial_steps': [
            {'num': '1', 'title': 'Leia a explicação', 'desc': 'Cada passo tem um texto curto, em letras grandes e fáceis de ler.'},
            {'num': '2', 'title': 'Veja a imagem interativa', 'desc': 'Mostramos exatamente onde tem de clicar no ecrã do telemóvel.'},
            {'num': '3', 'title': 'Marque como concluído', 'desc': 'Clique no botão verde para avançar. O seu progresso fica guardado!'}
        ]
    }
    return render(request, 'como_usar.html', context)

def category_page(request, category_id):
    """Renderiza a página de uma Categoria específica."""
    category = Categoria.objects.filter(id=category_id).first()
    if not category:
        return redirect('home')

    tutorials = category.tutorials.all()
    context = {'category': category, 'tutorials': tutorials}
    return render(request, 'category_page.html', context)

def tutorial_page(request, category_id, tutorial_id):
    """Renderiza os passos de um tutorial específico."""
    category = Categoria.objects.filter(id=category_id).first()
    if not category:
        return redirect('home')
        
    tutorial = Tutorial.objects.filter(id=tutorial_id, categoria=category).first()
    if not tutorial:
        return redirect('category', category_id=category_id)
        
    steps = tutorial.steps.all().order_by('ordem')
    
    # -----------------------------------------------------
    # CORREÇÃO: VERIFICA SE O UTILIZADOR JÁ CONCLUIU ANTES
    # -----------------------------------------------------
    is_completed = False
    if request.user.is_authenticated:
        is_completed = Progresso.objects.filter(usuario=request.user, tutorial=tutorial).exists()

    context = {
        'category': category,
        'tutorial': tutorial,
        'steps': steps,
        'is_completed': is_completed  # Variável enviada para o HTML
    }
    return render(request, 'tutorial_page.html', context)


# ==========================================
# 3. REGISTO DE PROGRESSO E PERFIL
# ==========================================

@login_required
def concluir_tutorial(request, tutorial_id):
    """Regista no banco de dados que o utilizador concluiu um tutorial."""
    if request.method == 'POST':
        tutorial = Tutorial.objects.filter(id=tutorial_id).first()
        if tutorial:
            Progresso.objects.get_or_create(usuario=request.user, tutorial=tutorial)
            return JsonResponse({'success': True, 'message': 'Progresso salvo!'})
    return JsonResponse({'success': False, 'message': 'Erro ao salvar.'}, status=400)

@login_required
def user_progress_view(request):
    """Processa e renderiza as estatísticas do perfil do utilizador."""
    progressos = Progresso.objects.filter(usuario=request.user).order_by('-concluido_em')
    total_completed = progressos.count()
    recent_completions = [p.tutorial.title for p in progressos[:5]]
    total_tutorials = Tutorial.objects.count()
    progress_percentage = round((total_completed / total_tutorials) * 100) if total_tutorials > 0 else 0
    
    categories = []
    for cat in Categoria.objects.all():
        total_na_cat = cat.tutorials.count()
        completados_na_cat = progressos.filter(tutorial__categoria=cat).count()
        percent = round((completados_na_cat / total_na_cat) * 100) if total_na_cat > 0 else 0
        categories.append({
            'name': cat.name, 'completed': completados_na_cat,
            'total': total_na_cat, 'percentage': percent, 'color_class': cat.color
        })

    context = {
        'username': request.user.username, 'total_tutorials': total_tutorials,
        'completed_tutorials': total_completed, 'progress_percentage': progress_percentage,
        'categories': categories, 'recent_completions': recent_completions
    }
    return render(request, 'user_progress.html', context)


# ==========================================
# 4. DICIONÁRIO E ACESSIBILIDADE
# ==========================================

def dictionary_menu(request):
    return render(request, 'dictionary_menu.html')

def dictionary_icons(request):
    icon_categories = [
        {'name': 'Comunicação Básica', 'icons': [{'name': 'Telefone Verde', 'meaning': 'Serve para atender uma chamada ou iniciar uma nova ligação.', 'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'},
        {
        'name': 'Telefone Vermelho',
        'meaning': 'Utilizado para recusar uma chamada recebida ou encerrar uma ligação em andamento.',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><path d="M10.68 13.31a16 16 0 0 0 3.41 2.6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7 2 2 0 0 1 1.72 2v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.42 19.42 0 0 1-3.33-2.67m-2.67-3.34a19.79 19.79 0 0 1-3.07-8.63A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91" /><line x1="23" y1="1" x2="1" y2="23" /></svg>'
      },
      {
        'name': 'Chat de Mensagem',
        'meaning': 'Indica o envio ou recebimento de mensagens de texto e conversas por chat.',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
      }                                         ]},
        {
        'name': 'Ações e Navegação',
        'icons': [
        {
            'name': 'Lupa de Pesquisa',
            'meaning': 'Permite buscar por contatos, ferramentas, históricos ou palavras-chave no sistema.',
            'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
        },
        {
            'name': 'Configurações',
            'meaning': 'Dá acesso às definições do sistema, ajustes de conta, privacidade e preferências.',
            'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
        },
        {
            'name': 'Sinal de Adicionar',
            'meaning': 'Utilizado para criar um novo registro, adicionar um contato ou iniciar um novo processo.',
            'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>'
        }
        ]
    },
    {
    'name': 'Mídia e Áudio',
    'icons': [
      {
        'name': 'Microfone Ativo',
        'meaning': 'Indica que o seu microfone está ligado e capturando áudio na chamada.',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v1a7 7 0 0 1-14 0v-1"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>'
      },
      {
        'name': 'Microfone Mutado',
        'meaning': 'Indica que o seu microfone está desativado e os outros participantes não te escutam.',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><line x1="1" y1="1" x2="23" y2="23"/><path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"/><path d="M17 11a7 7 0 0 1-12 0v-1m14 0a6.9 6.9 0 0 1-.5 2.5"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>'
      },
      {
        'name': 'Câmera de Vídeo',
        'meaning': 'Ativa ou desativa a transmissão da sua webcam durante uma videoconferência.',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>'
      }
    ]
    },
  {
    'name': 'Gerenciamento',
    'icons': [
      {
        'name': 'Contatos / Usuários',
        'meaning': 'Dá acesso à lista de contatos, clientes cadastrados ou perfil de usuários.',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
      },
      {
        'name': 'Histórico / Relógio',
        'meaning': 'Exibe a linha do tempo de interações, histórico de chamadas ou atividades recentes.',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-full h-full"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
      }
    ]
  }
    ]
    return render(request, 'dictionary_icons.html', {'icon_categories': icon_categories})

def dictionary_words(request):
    words_data = [
        {'word': 'App (Aplicação)', 'definition': 'Um programa que instala no telemóvel para fazer algo específico.', 'example': 'Exemplo: "Vou abrir o app do banco para ver o saldo."'},
        {'word': 'Wi-Fi', 'definition': 'Internet sem fios. Permite que o telemóvel se ligue à internet sem gastar dados móveis.', 'example': 'Exemplo: "Estou ligado ao Wi-Fi de casa."'},
        {
            'word': 'Link / Hiperligação',
            'definition': 'Um texto azul ou uma imagem onde se clica para abrir uma nova página da internet ou um vídeo.',
            'example': 'Exemplo: "O meu neto enviou-me um link para ver a receita no YouTube."'
        },
        {
            'word': 'Download (Baixar)',
            'definition': 'O ato de baixar ou puxar uma coisa da internet (como uma foto, jogo ou documento) para dentro da memória do telemóvel.',
            'example': 'Exemplo: "Vou fazer o download da fotografia que me enviaste para guardá-la."'
        },
        {
            'word': 'Upload (Carregar / Enviar)',
            'definition': 'O contrário de descarregar. Significa enviar uma foto ou um ficheiro que está no seu telemóvel para a internet ou para outra pessoa.',
            'example': 'Exemplo: "Vou fazer o upload da foto das férias para o Facebook."'
        },
        {
            'word': 'Áudio / Mensagem de Voz',
            'definition': 'Uma mensagem gravada com a voz em vez de ser escrita. Funciona como um gravador de voz rápido.',
            'example': 'Exemplo: "Não consigo escrever agora, vou mandar-te um áudio."'
        },
        {
            'word': 'Notificação',
            'definition': 'Um aviso ou alerta visual e sonoro que aparece no ecrã do telemóvel para avisar que chegou uma nova mensagem, chamada ou novidade.',
            'example': 'Exemplo: "O meu telemóvel apitou, deve ser uma notificação do WhatsApp."'
        },
        {
            'word': 'Login / Iniciar Sessão',
            'definition': 'O processo de entrar numa aplicação ou site inserindo o seu nome de utilizador (ou e-mail) e a sua palavra-passe.',
            'example': 'Exemplo: "Preciso de fazer login para conseguir ver os meus e-mails."'
        },
        {
            'word': 'Ficheiro / Arquivo',
            'definition': 'Qualquer documento digital guardado no telemóvel, como uma fotografia, uma música, um vídeo ou um texto em PDF.',
            'example': 'Exemplo: "Não encontro o ficheiro com o resultado das minhas análises."'
        },
        {
            'word': 'Spam / Mensagens Incomodativas',
            'definition': 'Mensagens eletrónicas ou de publicidade que recebe sem ter pedido. Muitas vezes são propagandas ou tentativas de burla.',
            'example': 'Exemplo: "A minha caixa de correio está cheia de spam de lojas que nem conheço."'
        },
        {
            'word': 'PDF',
            'definition': 'É um documento digital que não se pode alterar. Funciona como uma folha impressa que vê no celular: serve apenas para ler, ver e guardar, sem o risco de apagar ou desconfigurar as letras sem querer.',
            'example': 'Exemplo: "O médico enviou-me a receita em PDF para eu mostrar na farmácia."'
        }
    ]
    return render(request, 'dictionary_words.html', {'words': words_data})

def toggle_contrast(request):
    request.session['high_contrast'] = not request.session.get('high_contrast', False)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def completed_tutorials_view(request):
    progressos = Progresso.objects.filter(usuario=request.user).select_related('tutorial', 'tutorial__categoria')
    tutoriais_por_categoria = {}
    for progresso in progressos:
        categoria = progresso.tutorial.categoria
        if categoria not in tutoriais_por_categoria:
            tutoriais_por_categoria[categoria] = []
        tutoriais_por_categoria[categoria].append(progresso.tutorial)
        
    context = {'tutoriais_por_categoria': tutoriais_por_categoria, 'total_concluidos': progressos.count()}
    return render(request, 'completed_tutorials.html', context)