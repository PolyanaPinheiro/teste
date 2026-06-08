from django.db import models
from django.contrib.auth.models import User

# 1. CATEGORIAS (Tem de ser a primeira)
class Categoria(models.Model):
    id = models.CharField(max_length=100, primary_key=True, help_text="Ex: ferramentas-celular")
    name = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    subtitle = models.CharField(max_length=255, verbose_name="Subtítulo")
    color = models.CharField(max_length=100, help_text="Classe CSS do Tailwind. Ex: bg-gradient-to-br from-blue-500 to-blue-600")
    icon_svg = models.TextField(help_text="Código SVG completo do ícone principal")

    def __str__(self):
        return self.name

# 2. TUTORIAIS (Liga-se às Categorias)
class Tutorial(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='tutorials', verbose_name="Categoria")
    id = models.CharField(max_length=100, primary_key=True, help_text="Ex: tirar-foto")
    title = models.CharField(max_length=150, verbose_name="Título do Tutorial")
    desc = models.TextField(verbose_name="Descrição Curta")
    icon = models.CharField(max_length=50, help_text="Nome do ícone no Lucide. Ex: camera, lock, phone")

    def __str__(self):
        return f"[{self.categoria.name}] {self.title}"

# 3. PASSOS (Liga-se aos Tutoriais)
class Passo(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='steps', verbose_name="Tutorial")
    ordem = models.PositiveIntegerField(default=1, verbose_name="Número do Passo")
    title = models.CharField(max_length=150, verbose_name="Título do Passo")
    description = models.TextField(verbose_name="Instruções do Passo")
    tips = models.TextField(blank=True, null=True, verbose_name="Dica Importante (Opcional)")
    icon_svg = models.TextField(blank=True, null=True, help_text="SVG opcional para o ícone interno do passo")
    interactiveImage = models.CharField(max_length=255, blank=True, null=True, help_text="Caminho da imagem estática. Ex: /static/IMG/spam_suspeito.jpg")
    
    # === ESTE É O NOVO CAMPO MÁGICO ===
    html_interativo = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="HTML Interativo", 
        help_text="Código HTML/Tailwind que desenha o ecrã do telemóvel. Pode colocar onclick='handleNextStep()' no botão correto!"
    )

    class Meta:
        ordering = ['ordem']
        verbose_name = "Passo do Tutorial"
        verbose_name_plural = "Passos do Tutorial"

    def __str__(self):
        return f"{self.tutorial.title} - Passo {self.ordem}"

# 4. PROGRESSO (Liga-se ao Tutorial e ao User - Tem de ficar no fim)
class Progresso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progressos')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='progressos')
    concluido_em = models.DateTimeField(auto_now_add=True) # Guarda a data e hora automaticamente

    class Meta:
        # Evita que o banco de dados conte 2 vezes se o utilizador refizer o mesmo tutorial
        unique_together = ('usuario', 'tutorial')
        verbose_name = "Progresso"
        verbose_name_plural = "Progressos"

    def __str__(self):
        # Mostra o nome da pessoa (first_name) em vez do email (username) lá no painel Admin
        nome_pessoa = self.usuario.first_name if self.usuario.first_name else self.usuario.username
        return f"{nome_pessoa} concluiu: {self.tutorial.title}"