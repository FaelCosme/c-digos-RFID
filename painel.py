 import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import subprocess
import os

# Define uma cor de fundo (opcional)
Window.clearcolor = (0.15, 0.15, 0.15, 1)

class LoginScreen(Screen):
    """Screen que contém o formulário de login. A estrutura visual
    é definida em 'painel.kv'.
    """

    def verificar_login(self):
        """Chamado pelo botão 'Entrar' no arquivo .kv. Se o login for
        bem-sucedido troca para a tela 'main'."""

        usuario_digitado = self.ids.user_input.text
        senha_digitada = self.ids.pass_input.text

        usuarios_cadastrados = {
            "admin": "senha123",
            "usuario": "abc",
            "kivy_dev": "python",
        }

        feedback_label = self.ids.feedback

        if usuario_digitado in usuarios_cadastrados:
            if usuarios_cadastrados[usuario_digitado] == senha_digitada:
                feedback_label.text = f'Login bem-sucedido! Bem-vindo(a), {usuario_digitado}.'
                feedback_label.color = (0, 1, 0, 1)
                # Troca para a tela principal
                if self.manager:
                    self.manager.current = 'main'
            else:
                feedback_label.text = 'Senha incorreta.'
                feedback_label.color = (1, 0, 0, 1)
        else:
            feedback_label.text = 'Usuário não encontrado.'
            feedback_label.color = (1, 0, 0, 1)

        # Limpa o campo de senha após a tentativa
        self.ids.pass_input.text = ""


# Define o comando padrão para o script de gravação
DEFAULT_COMMAND = os.path.join(os.path.dirname(__file__), 'codigoParaInicar.py')


class MainScreen(Screen):
    """Tela principal que aparece após login bem-sucedido."""

    def start_audio_recording(self):
        """Inicia o script 'codigoParaInicar.py' em background.
        Esta função é chamada diretamente pelo botão 'Gravar Áudio'.
        """
        
        # O comando agora é fixo, não vem mais do input
        cmd_text = f'python "{DEFAULT_COMMAND}"'

        try:
            # Inicia o processo
            subprocess.Popen(cmd_text, shell=True)
            
            # Atualiza o label de feedback
            if 'main_feedback' in self.ids:
                self.ids.main_feedback.text = f'Gravação de áudio iniciada...'
                self.ids.main_feedback.color = (0, 1, 0, 1) # Verde
        except Exception as e:
            if 'main_feedback' in self.ids:
                self.ids.main_feedback.text = f'Erro ao iniciar gravação: {e}'
                self.ids.main_feedback.color = (1, 0, 0, 1) # Vermelho
            else:
                print(f'Erro ao iniciar comando: {e}')

    def do_logout(self):
        """Retorna para a tela de login."""
        if self.manager:
            # Limpa o feedback da tela principal ao sair
            if 'main_feedback' in self.ids:
                self.ids.main_feedback.text = ""
            self.manager.current = 'login'


class PainelApp(App):
    """App principal. Cria um ScreenManager com as telas de login e
    tela principal. O Kivy irá carregar automaticamente o arquivo 'painel.kv'
    """

    def build(self):
        # O ScreenManager agora é gerenciado pelo arquivo .kv
        # Mas manteremos a lógica original para consistência
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

# --- Ponto de entrada do script ---
if __name__ == '__main__':
    PainelApp().run()
