from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk, messagebox
import json
import psycopg2
import sqlparse
import random
from collections import Counter
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
        
        self.feedback_label = ttk.Label(self.root, text="", font=('Arial', 12))
        self.feedback_label.pack(pady=10)
        
        self.next_button = ttk.Button(
            self.root, 
            text="Próxima Pergunta →", 
            command=self.next_question, 
            state=tk.DISABLED
        )
        self.next_button.pack(pady=5)
        
        # Área para exibição dos resultados (lado a lado) em formato tabular
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Resultado da consulta do usuário
        self.user_result_frame = ttk.Frame(self.result_frame)
        self.user_result_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.user_result_label = ttk.Label(self.user_result_frame, text="Resultado da consulta")
        self.user_result_label.pack()
        self.user_result_tree = ttk.Treeview(self.user_result_frame, show="headings")
        self.user_result_tree.pack(fill=tk.BOTH, expand=True)
        user_scroll = ttk.Scrollbar(self.user_result_frame, orient="vertical", command=self.user_result_tree.yview)
        self.user_result_tree.configure(yscrollcommand=user_scroll.set)
        user_scroll.pack(side="right", fill="y")
        
        # Resultado esperado
        self.expected_result_frame = ttk.Frame(self.result_frame)
        self.expected_result_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.expected_result_label = ttk.Label(self.expected_result_frame, text="Resultado esperado")
        self.expected_result_label.pack()
        self.expected_result_tree = ttk.Treeview(self.expected_result_frame, show="headings")
        self.expected_result_tree.pack(fill=tk.BOTH, expand=True)
        expected_scroll = ttk.Scrollbar(self.expected_result_frame, orient="vertical", command=self.expected_result_tree.yview)
        self.expected_result_tree.configure(yscrollcommand=expected_scroll.set)
        expected_scroll.pack(side="right", fill="y")

    def next_question(self):
        """Exibe a próxima questão ou finaliza se todas já foram respondidas."""
        if self.questions:
            self.current_question = random.choice(self.questions)
            self.questions.remove(self.current_question)
            self.question_label.config(text=self.current_question['enunciado'])
            self.answer_entry.delete('1.0', tk.END)
            self.feedback_label.config(text="")
            self.next_button.config(state=tk.DISABLED)
            self.clear_result_widgets()
        else:
            messagebox.showinfo("Parabéns!", "Todas as questões foram respondidas!")
            self.on_close()

    def safe_execute(self, sql):
        """
        Executa a query SQL de forma segura, reabrindo a conexão se necessário.
        Retorna uma tupla (rows, columns, error).
        """
        try:
            if self.conn.closed or self.conn.status != psycopg2.extensions.STATUS_READY:
                self.setup_db_connection()
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                if cursor.description:
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    return (rows, columns, None)
                return (None, None, None)
        except psycopg2.Error as e:
            self.conn.close()
            self.setup_db_connection()
            return (None, None, str(e))
        
    def is_select_only(self, sql):
        """Verifica se a query contém apenas comandos SELECT."""
        try:
            statements = sqlparse.parse(sql)
            for stmt in statements:
                if stmt.get_type().upper() != 'SELECT': 
                    return False
            return True
        except Exception:
            return False

    def get_tables_accessed(self, sql):
        """
        Executa um EXPLAIN (FORMAT JSON) para extrair as tabelas utilizadas na query,
        considerando também subqueries (chaves 'SubPlan' e 'InitPlan').
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"EXPLAIN (FORMAT JSON) {sql}")
                plan_json = cursor.fetchone()[0]
                plan = plan_json[0]['Plan']
                tables = set()
                def extract(plan_node, tables):
                    if 'Relation Name' in plan_node:
                        tables.add(plan_node['Relation Name'])
                    for key in ('Plans', 'SubPlan', 'InitPlan'):
                        if key in plan_node:
                            for child in plan_node[key]:
                                extract(child, tables)
                extract(plan, tables)
                return tables
        except psycopg2.Error:
            return set()
    
    def get_plan_conditions(self, sql):
        """
        Executa um EXPLAIN (FORMAT JSON, VERBOSE) para extrair as condições lógicas da query,
        como condições de junção e filtros.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"EXPLAIN (FORMAT JSON, VERBOSE) {sql}")
                plan_json = cursor.fetchone()[0]
                plan = plan_json[0]['Plan']
                conditions = []
                def extract_conditions(node):
                    for key in ('Hash Cond', 'Merge Cond', 'Join Filter', 'Index Cond'):
                        if key in node:
                            conditions.append(node[key])
                    if 'Filter' in node:
                        conditions.append(node['Filter'])
                    for sub_key in ('Plans', 'SubPlan', 'InitPlan'):
                        if sub_key in node:
                            for child in node[sub_key]:
                                extract_conditions(child)
                extract_conditions(plan)
                return conditions
        except psycopg2.Error:
            return []

    def update_treeview(self, treeview, columns, rows):
        """Atualiza o widget Treeview com os dados fornecidos, limitando a 20 linhas.
           Se 'rows' não for uma lista (ex.: mensagem de erro), trata como string."""
        # Limpa o conteúdo atual
        for item in treeview.get_children():
            treeview.delete(item)
        # Define as colunas
        if columns and isinstance(columns, list) and all(isinstance(x, str) for x in columns):
            treeview["columns"] = columns
            for col in columns:
                treeview.heading(col, text=col)
                treeview.column(col, width=100)
        else:
            treeview["columns"] = ("Resultado",)
            treeview.heading("Resultado", text="Resultado")
            treeview.column("Resultado", width=200)
        # Se rows não for uma lista, trata como string
        if not isinstance(rows, list):
            rows = [(rows,)]
        # Limita a 20 linhas e adiciona "..." se houver mais
        if len(rows) > 20:
            rows_to_insert = rows[:20] + [("...",)]
        else:
            rows_to_insert = rows
        for row in rows_to_insert:
            treeview.insert("", tk.END, values=row)

    def display_query_results(self, user_result, user_columns, expected_result, expected_columns):
        """Exibe os resultados (ou erros) das consultas em formato tabular."""
        self.update_treeview(self.user_result_tree, user_columns, user_result)
        self.update_treeview(self.expected_result_tree, expected_columns, expected_result)

    def clear_result_widgets(self):
        """Limpa os widgets de resultado para a nova questão."""
        for tree in (self.user_result_tree, self.expected_result_tree):
            for item in tree.get_children():
                tree.delete(item)

    def compare_query_logic(self, user_sql, base_sql):
        """Compara a lógica/álgebra relacional da query do usuário com a resposta base."""
        user_rows, user_cols, user_err = self.safe_execute(user_sql)
        base_rows, base_cols, base_err = self.safe_execute(base_sql)
        if user_err or base_err:
            return False, "Erro na execução das queries."
        if Counter(user_rows) != Counter(base_rows):
            return False, "Os dados retornados não correspondem."
        user_tables = self.get_tables_accessed(user_sql)
        base_tables = self.get_tables_accessed(base_sql)
        if user_tables != base_tables:
            return False, f"Tabelas incorretas. Esperado: {base_tables}"
        user_conds = set(self.get_plan_conditions(user_sql))
        base_conds = set(self.get_plan_conditions(base_sql))
        for cond in base_conds:
            if cond not in user_conds:
                return False, "Condições lógicas ausentes na sua query."
        return True, "Lógica da query correta!"

    def submit_answer(self):
        """Processa a resposta do usuário, exibe os resultados e compara com a resposta base."""
        user_sql = self.answer_entry.get('1.0', tk.END).strip()
        if not user_sql:
            messagebox.showwarning("Aviso", "Digite sua resposta SQL.")
            return

        # 1. Verifica se é somente SELECT
        if not self.is_select_only(user_sql):
            self.show_feedback(False, "Apenas comandos SELECT são permitidos.")
            return

        # Executa a query do usuário e a query base
        user_rows, user_cols, user_err = self.safe_execute(user_sql)
        base_sql = self.current_question['resposta_base']
        base_rows, base_cols, base_err = self.safe_execute(base_sql)
        
        # Atualiza os widgets de resultado (exibindo erro, se houver)
        self.display_query_results(
            user_err if user_err else user_rows,
            user_cols,
            base_err if base_err else base_rows,
            base_cols
        )

        if user_err:
            self.show_feedback(False, f"Erro na query: {user_err}")
            return
        if base_err:
            self.show_feedback(False, "Erro na resposta base!")
            return

        # 2. Valida número de linhas
        if (user_rows is None and base_rows is not None) or \
           (user_rows is not None and base_rows is None) or \
           (user_rows is not None and base_rows is not None and len(user_rows) != len(base_rows)):
            expected = len(base_rows) if base_rows is not None else 0
            self.show_feedback(False, f"Linhas incorretas. Esperado: {expected}")
            return

        # 3. Validação da lógica/álgebra relacional (sem considerar as colunas)
        logic_ok, message = self.compare_query_logic(user_sql, base_sql)
        if not logic_ok:
            self.show_feedback(False, message)
            return

        self.show_feedback(True, "Resposta Correta!")

    def show_feedback(self, correct, message=""):
        """Exibe o feedback para o usuário."""
        if correct:
            self.feedback_label.config(text="✅ Correto! " + message, foreground="green")
            self.next_button.config(state=tk.NORMAL)
        else:
            self.feedback_label.config(text="❌ Errado! " + message, foreground="red")

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
