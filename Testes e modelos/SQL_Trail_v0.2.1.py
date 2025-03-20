from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk, messagebox
import json
import psycopg2
import sqlparse
import random
from psycopg2 import OperationalError

class SQLTrail:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Trail App")
        
        self.conn = None 
        self.image_window = None
        self.img_reference = None
        
        self.setup_db_connection() 
        self.setup_image()
        self.load_questions()
        self.create_widgets()
        self.next_question()
        self.create_results_frame()

    def setup_db_connection(self):
        """Configura a conexão com o banco de dados."""
        db_config = {
            'host': 'localhost',
            'port': '5432',
            'dbname': 'compraiz',
            'user': 'hr',
            'password': 'hr'
        }

        try:
            if self.conn and not self.conn.closed:
                self.conn.close()

            self.conn = psycopg2.connect(**db_config)
            self.conn.autocommit = True

        except OperationalError as e:
            if self.conn:
                self.conn.close()
            messagebox.showerror("Erro", f"Falha na conexão: {str(e)}")
            self.root.destroy()
            raise 

    def setup_image(self):
        """Configura a janela com a imagem de referência."""
        try:
            self.image_window = tk.Toplevel(self.root)
            self.image_window.title("Mapa de Referência")
            
            img = Image.open("modelo.PNG")
            self.img_reference = ImageTk.PhotoImage(img)
            
            label = tk.Label(self.image_window, image=self.img_reference)
            label.pack()
            
            self.center_window(self.image_window, img.width, img.height)
            
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo modelo.PNG não encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")

    def load_questions(self):
        """Carrega as questões do arquivo JSON."""
        try:
            with open('questoes.json', 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
                
                # Verifica se cada questão possui os campos necessários
                for q in self.questions:
                    if not all(k in q for k in ('id', 'enunciado', 'resposta_base')):
                        messagebox.showerror("Erro", f"Questão {q.get('id')} inválida!")
                        self.root.destroy()
                        return
                        
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo 'questoes.json' não encontrado.")
            self.root.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Formato JSON inválido!")
            self.root.destroy()

    def create_widgets(self):
        """Cria os widgets da interface."""
        self.question_label = ttk.Label(self.root, text="", wraplength=500)
        self.question_label.pack(pady=10)
        
        self.answer_entry = tk.Text(self.root, font=('Cascadia Code', 10), height=10, width=50)
        self.answer_entry.pack(pady=10)
        
        self.submit_button = ttk.Button(
            self.root, 
            text="Enviar Resposta", 
            command=self.submit_answer
        )
        self.submit_button.pack(pady=5)
        
        self.feedback_label = ttk.Label(
            self.root, 
            text="", 
            font=('Arial', 12)
        )
        self.feedback_label.pack(pady=10)
        
        self.next_button = ttk.Button(
            self.root, 
            text="Próxima Pergunta →", 
            command=self.next_question, 
            state=tk.DISABLED
        )
        self.next_button.pack(pady=5)

    def next_question(self):
        """Exibe a próxima questão ou finaliza se todas já foram respondidas."""
        if self.questions:
            self.current_question = random.choice(self.questions)
            self.questions.remove(self.current_question)
            self.question_label.config(text=self.current_question['enunciado'])
            self.answer_entry.delete('1.0', tk.END)
            self.feedback_label.config(text="")
            self.next_button.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Parabéns!", "Todas as questões foram respondidas!")
            self.on_close()

    def safe_execute(self, sql):
        """
        Executa a query SQL de forma segura, reabrindo a conexão se necessário.
        Retorna uma tupla (linhas, erro).
        """
        try:
            if self.conn.closed or self.conn.status != psycopg2.extensions.STATUS_READY:
                self.setup_db_connection()
                
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                
                if cursor.description:  # Se a query retorna linhas
                    rows = cursor.fetchall()
                    return (rows, None)
                return (None, None)
                
        except psycopg2.Error as e:
            # Em caso de erro, reabre a conexão
            self.conn.close()
            self.setup_db_connection()
            return (None, str(e))
        
    def is_select_only(self, sql):
        """Verifica se a query contém apenas comandos SELECT."""
        try:
            statements = sqlparse.parse(sql)
            for stmt in statements:
                stmt_type = stmt.get_type().upper()
                if stmt_type != 'SELECT': 
                    return False
            return True
        except Exception:
            return False
            
    def normalize_sql(self, sql):
        """Padroniza formatação da query para comparação básica"""
        formatted = sqlparse.format(
            sql,
            keyword_case='upper',    # Palavras-chave em maiúsculo (SELECT, FROM)
            identifier_case='lower', # Nomes de tabelas/colunas em minúsculo
            strip_comments=True,     # Remove comentários
            reindent=True            # Reindenta o código
        )
        # Remove espaços excessivos e quebras de linha
        return ' '.join(formatted.split()).strip()
    

    def create_results_frame(self):
        """Cria o frame para exibição dos resultados lado a lado"""
        results_frame = ttk.Frame(self.root)
        results_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame do resultado do usuário
        self.user_result_frame = ttk.LabelFrame(results_frame, text="Seu Resultado")
        self.user_result_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        self.user_result_text = tk.Text(
            self.user_result_frame, 
            height=15, 
            state='disabled',
            font=('Cascadia Code', 9)
        )
        self.user_result_text.pack(fill=tk.BOTH, expand=True)

        # Frame do resultado esperado
        self.expected_result_frame = ttk.LabelFrame(results_frame, text="Resultado Esperado")
        self.expected_result_frame.pack(side=tk.RIGHT, padx=5, fill=tk.BOTH, expand=True)

        self.expected_result_text = tk.Text(
            self.expected_result_frame, 
            height=15, 
            state='disabled',
            font=('Cascadia Code', 9)
        )
        self.expected_result_text.pack(fill=tk.BOTH, expand=True)

    def display_result(self, text_widget, result, error=None):
        """Exibe o resultado ou erro no widget de texto"""
        text_widget.config(state='normal')
        text_widget.delete('1.0', tk.END)
        
        if error:
            text_widget.insert(tk.END, f"ERRO:\n{error}")
        else:
            if result:
                # Limita a 20 linhas
                for i, row in enumerate(result[:20]):
                    text_widget.insert(tk.END, f"{row}\n")
                if len(result) > 20:
                    text_widget.insert(tk.END, "\n... (resultado truncado)")
            else:
                text_widget.insert(tk.END, "Consulta executada com sucesso (sem resultados)")
        
        text_widget.config(state='disabled')

    def submit_answer(self):

        self.display_result(self.user_result_text, None)
        self.display_result(self.expected_result_text, None)


        """Processa a resposta do usuário e compara com a resposta base."""
        user_sql = self.answer_entry.get('1.0', tk.END).strip()

        if not user_sql:
            messagebox.showwarning("Aviso", "Digite sua resposta SQL.")
            return

        if not self.is_select_only(user_sql):
            self.show_feedback(False, "Apenas comandos SELECT são permitidos.")
            return

        user_rows, user_err = self.safe_execute(user_sql)
        if user_err:
            self.show_feedback(False, f"Erro na query: {user_err}")
            return

        base_sql = self.current_question['resposta_base']
        base_rows, base_err = self.safe_execute(base_sql)
        if base_err:
            self.show_feedback(False, "Erro na resposta base!")
            return

        
        user_rows, user_err = self.safe_execute(user_sql)
        self.display_result(self.user_result_text, user_rows, user_err)

        # Executa a query base e exibe resultado
        base_sql = self.current_question['resposta_base']
        base_rows, base_err = self.safe_execute(base_sql)
        self.display_result(self.expected_result_text, base_rows, base_err)

        # Verifica se o número de linhas retornadas é o mesmo
        if (user_rows is None and base_rows is not None) or (user_rows is not None and base_rows is None) or (user_rows is not None and base_rows is not None and len(user_rows) != len(base_rows)):
            expected = len(base_rows) if base_rows is not None else "0"
            self.show_feedback(False, f"Linhas incorretas. Esperado: {expected}")
            return

        user_norm = self.normalize_sql(user_sql)
        base_norm = self.normalize_sql(base_sql)
    
        if user_norm == base_norm:
            self.show_feedback(True, "Resposta Correta!")
            return
        
        user_details = self.get_execution_plan_details(user_sql)
        base_details = self.get_execution_plan_details(base_sql)

        if user_details['tables'] != base_details['tables']:
            self.show_feedback(False, f"Tabelas incorretas. Esperado: {base_details['tables']}")
            return
        
        missing_conditions = base_details['conditions'] - user_details['conditions']
        extra_conditions = user_details['conditions'] - base_details['conditions']

        if missing_conditions or extra_conditions:
            feedback = []
            if missing_conditions:
                feedback.append(f"Faltam condições: {', '.join(missing_conditions)}")
            if extra_conditions:
                feedback.append(f"Condições extras: {', '.join(extra_conditions)}")
            self.show_feedback(False, " | ".join(feedback))
            return

        self.show_feedback(True, "Resposta Correta!")

    def get_execution_plan_details(self, sql):
        """Extrai tabelas, condições WHERE e JOIN ON do plano de execução."""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"EXPLAIN (FORMAT JSON) {sql}")
                plan_json = cursor.fetchone()[0]
                plan = plan_json[0]['Plan']
                details = {
                    'tables': set(),
                    'conditions': set()
                }

                def extract(plan_node):
                    if 'Relation Name' in plan_node:
                        details['tables'].add(plan_node['Relation Name'])
                    if 'Filter' in plan_node:
                        details['conditions'].add(normalize_condition(plan_node['Filter']))
                    if 'Hash Cond' in plan_node:
                        details['conditions'].add(normalize_condition(plan_node['Hash Cond']))
                    if 'Join Filter' in plan_node:
                        details['conditions'].add(normalize_condition(plan_node['Join Filter']))

                    for key in ('Plans', 'SubPlan', 'InitPlan'):
                        if key in plan_node:
                            for child in plan_node[key]:
                                extract(child)

                def normalize_condition(cond):
                    """Padroniza a formatação das condições para comparação"""
                    return ' '.join(cond.replace('(', '').replace(')', '').lower().split())

                extract(plan)
                return details
        except psycopg2.Error:
            return {'tables': set(), 'conditions': set()}

    def show_feedback(self, correct, message=""):
        """Exibe o feedback para o usuário."""
        if correct:
            self.feedback_label.config(
                text="✅ Correto! " + message, 
                foreground="green"
            )
            self.next_button.config(state=tk.NORMAL)
        else:
            self.feedback_label.config(
                text="❌ Errado! " + message, 
                foreground="red"
            )

    def on_close(self):
        """Fecha a conexão, as janelas abertas e encerra o aplicativo."""
        if self.conn:
            self.conn.close()
        if self.image_window:
            self.image_window.destroy()
        self.root.destroy()

    def center_window(self, window, width, height):
        """Centraliza uma janela na tela."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLTrail(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
