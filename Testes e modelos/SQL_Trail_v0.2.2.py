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
        # Inicializa a aplicação com a janela principal
        self.root = root
        self.root.title("SQL Trail App")
        
        # Inicializa variáveis para a conexão com o banco e para a imagem de referência
        self.conn = None 
        self.image_window = None
        self.img_reference = None
        
        # Configura a conexão com o banco de dados, a imagem de referência,
        # carrega as questões e cria os widgets da interface, além de exibir a primeira questão.
        self.setup_db_connection() 
        self.setup_image()
        self.load_questions()
        self.create_widgets()
        self.next_question()

    def setup_db_connection(self):
        """Configura a conexão com o banco de dados PostgreSQL usando as configurações definidas."""
        db_config = {
            'host': 'localhost',
            'port': '5432',
            'dbname': 'compraiz',
            'user': 'hr',
            'password': 'hr'
        }
        try:
            # Se já houver uma conexão aberta, fecha-a antes de abrir uma nova
            if self.conn and not self.conn.closed:
                self.conn.close()
            self.conn = psycopg2.connect(**db_config)
            # Ativa o modo autocommit para evitar a necessidade de confirmar transações
            self.conn.autocommit = True
        except OperationalError as e:
            if self.conn:
                self.conn.close()
            messagebox.showerror("Erro", f"Falha na conexão: {str(e)}")
            self.root.destroy()
            raise 

    def setup_image(self):
        """Abre uma janela separada para exibir a imagem de referência (modelo.PNG)."""
        try:
            # Cria uma janela secundária
            self.image_window = tk.Toplevel(self.root)
            self.image_window.title("Mapa de Referência")
            
            # Abre o arquivo de imagem e converte para um formato compatível com Tkinter
            img = Image.open("modelo.PNG")
            self.img_reference = ImageTk.PhotoImage(img)
            
            # Cria um rótulo (Label) para exibir a imagem e o empacota na janela
            label = tk.Label(self.image_window, image=self.img_reference)
            label.pack()
            
            # Centraliza a janela de imagem na tela
            self.center_window(self.image_window, img.width, img.height)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo modelo.PNG não encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")

    def load_questions(self):
        """Carrega as questões do arquivo 'questoes.json' e verifica se cada questão contém os campos necessários."""
        try:
            with open('questoes.json', 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
                # Valida se cada questão possui os campos 'id', 'enunciado' e 'resposta_base'
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
        """Cria e organiza os widgets (elementos de interface) na janela principal."""
        # Rótulo para exibir a questão atual
        self.question_label = ttk.Label(self.root, text="", wraplength=500)
        self.question_label.pack(pady=10)
        
        # Área de texto para que o usuário digite a resposta SQL (apenas SELECTs)
        self.answer_entry = tk.Text(self.root, font=('Cascadia Code', 10), height=10, width=50)
        self.answer_entry.pack(pady=10)
        
        # Botão para enviar a resposta; chama o método submit_answer quando clicado
        self.submit_button = ttk.Button(
            self.root, 
            text="Enviar Resposta", 
            command=self.submit_answer
        )
        self.submit_button.pack(pady=5)
        
        # Rótulo para exibir feedback (acerto ou erro) para a resposta
        self.feedback_label = ttk.Label(self.root, text="", font=('Arial', 12))
        self.feedback_label.pack(pady=10)
        
        # Botão para avançar para a próxima pergunta (inicialmente desabilitado)
        self.next_button = ttk.Button(
            self.root, 
            text="Próxima Pergunta →", 
            command=self.next_question, 
            state=tk.DISABLED
        )
        self.next_button.pack(pady=5)
        
        # Cria um frame para exibir os resultados (do usuário e esperado) lado a lado
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Configura o frame para exibir o resultado da consulta do usuário
        self.user_result_frame = ttk.Frame(self.result_frame)
        self.user_result_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.user_result_label = ttk.Label(self.user_result_frame, text="Resultado da consulta")
        self.user_result_label.pack()
        self.user_result_tree = ttk.Treeview(self.user_result_frame, show="headings")
        self.user_result_tree.pack(fill=tk.BOTH, expand=True)
        user_scroll = ttk.Scrollbar(self.user_result_frame, orient="vertical", command=self.user_result_tree.yview)
        self.user_result_tree.configure(yscrollcommand=user_scroll.set)
        user_scroll.pack(side="right", fill="y")
        
        # Configura o frame para exibir o resultado esperado (query base)
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
        """Exibe a próxima questão; se não houver mais questões, exibe uma mensagem de conclusão e encerra o aplicativo."""
        if self.questions:
            # Seleciona aleatoriamente uma questão e a remove da lista
            self.current_question = random.choice(self.questions)
            self.questions.remove(self.current_question)
            # Atualiza o rótulo da questão, limpa a área de resposta e o feedback
            self.question_label.config(text=self.current_question['enunciado'])
            self.answer_entry.delete('1.0', tk.END)
            self.feedback_label.config(text="")
            # Desabilita o botão de próxima pergunta até que a resposta atual seja validada
            self.next_button.config(state=tk.DISABLED)
            # Limpa os widgets que exibem resultados anteriores
            self.clear_result_widgets()
        else:
            messagebox.showinfo("Parabéns!", "Todas as questões foram respondidas!")
            self.on_close()

    def safe_execute(self, sql):
        """
        Executa a query SQL de forma segura, reabrindo a conexão se necessário.
        Retorna uma tupla (rows, columns, error) contendo os resultados, nomes das colunas e qualquer erro ocorrido.
        """
        try:
            # Verifica se a conexão está fechada ou não pronta; se necessário, reabre a conexão
            if self.conn.closed or self.conn.status != psycopg2.extensions.STATUS_READY:
                self.setup_db_connection()
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                # Se a query retorna resultados (descrição de colunas existe), coleta as linhas e nomes das colunas
                if cursor.description:
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    return (rows, columns, None)
                return (None, None, None)
        except psycopg2.Error as e:
            # Em caso de erro, fecha e reabre a conexão, retornando o erro como string
            self.conn.close()
            self.setup_db_connection()
            return (None, None, str(e))
        
    def is_select_only(self, sql):
        """
        Verifica se a query contém apenas comandos SELECT.
        Utiliza a biblioteca sqlparse para analisar a query e garante que todos os statements são SELECT.
        """
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
        incluindo subqueries (procurando por chaves 'Plans', 'SubPlan' e 'InitPlan').
        Retorna um conjunto (set) com os nomes das tabelas.
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
        como condições de junção, filtros, condições de índice e outros.
        Percorre recursivamente o plano de execução para coletar todas as condições relevantes.
        Retorna uma lista com essas condições.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"EXPLAIN (FORMAT JSON, VERBOSE) {sql}")
                plan_json = cursor.fetchone()[0]
                plan = plan_json[0]['Plan']
                conditions = []
                def extract_conditions(node):
                    # Verifica várias chaves que podem conter condições lógicas
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
        """
        Atualiza o widget Treeview com os dados fornecidos.
        - Limpa o conteúdo atual.
        - Define as colunas (se os nomes forem válidos, usa-os; caso contrário, define uma coluna genérica).
        - Se rows não for uma lista, trata como uma única linha.
        - Limita a exibição a 20 linhas, adicionando "..." se houver mais linhas.
        """
        # Limpa o conteúdo atual do Treeview
        for item in treeview.get_children():
            treeview.delete(item)
        # Configura as colunas do Treeview
        if columns and isinstance(columns, list) and all(isinstance(x, str) for x in columns):
            treeview["columns"] = columns
            for col in columns:
                treeview.heading(col, text=col)
                treeview.column(col, width=100)
        else:
            treeview["columns"] = ("Resultado",)
            treeview.heading("Resultado", text="Resultado")
            treeview.column("Resultado", width=200)
        # Se 'rows' não for uma lista, converte para uma lista contendo uma única tupla
        if not isinstance(rows, list):
            rows = [(rows,)]
        # Limita a 20 linhas; se houver mais, adiciona uma linha com "..."
        if len(rows) > 20:
            rows_to_insert = rows[:20] + [("...",)]
        else:
            rows_to_insert = rows
        for row in rows_to_insert:
            treeview.insert("", tk.END, values=row)

    def display_query_results(self, user_result, user_columns, expected_result, expected_columns):
        """Exibe os resultados (ou mensagens de erro) das queries do usuário e da resposta base nos respectivos Treeviews."""
        self.update_treeview(self.user_result_tree, user_columns, user_result)
        self.update_treeview(self.expected_result_tree, expected_columns, expected_result)

    def clear_result_widgets(self):
        """Limpa os widgets de resultado para que a nova questão seja exibida sem dados residuais."""
        for tree in (self.user_result_tree, self.expected_result_tree):
            for item in tree.get_children():
                tree.delete(item)

    def compare_query_logic(self, user_sql, base_sql):
        """
        Compara a lógica (ou álgebra relacional) da query do usuário com a query base.
        Para isso:
        - Executa ambas as queries e compara os dados retornados (usando Counter para ignorar a ordem).
        - Verifica se as tabelas acessadas em ambas as queries são as mesmas.
        - Extrai as condições lógicas das queries e verifica se a query do usuário contém todas as condições da base.
        Retorna uma tupla (booleano, mensagem) indicando se a lógica está correta e uma mensagem de feedback.
        """
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
        """
        Processa a resposta do usuário, seguindo os passos:
        1. Obtém a consulta digitada e remove espaços extras.
        2. Verifica se o usuário digitou alguma consulta.
        3. Verifica se a consulta contém apenas comandos SELECT (DQL).
        4. Executa a query do usuário e a query base, capturando os resultados ou erros.
        5. Atualiza os widgets de resultado para exibir os dados ou erros.
        6. Compara o número de linhas retornadas.
        7. Compara a lógica da query (tabelas e condições) utilizando compare_query_logic.
        8. Exibe o feedback final (correto ou incorreto).
        """
        # Obtém a query digitada na área de texto e remove espaços em branco no início e no final
        user_sql = self.answer_entry.get('1.0', tk.END).strip()
        # Se o usuário não digitou nada, exibe um aviso e interrompe a execução
        if not user_sql:
            messagebox.showwarning("Aviso", "Digite sua resposta em DQL.")
            return

        # Verifica se a query contém apenas comandos SELECT (DQL). Se não, mostra feedback de erro.
        if not self.is_select_only(user_sql):
            self.show_feedback(False, "Apenas comandos SELECT são permitidos.")
            return

        # Executa a query do usuário e também a query base (resposta esperada) para comparar os resultados
        user_rows, user_cols, user_err = self.safe_execute(user_sql)
        base_sql = self.current_question['resposta_base']
        base_rows, base_cols, base_err = self.safe_execute(base_sql)
        
        # Atualiza os widgets que exibem os resultados das queries (do usuário e esperado)
        self.display_query_results(
            user_err if user_err else user_rows,
            user_cols,
            base_err if base_err else base_rows,
            base_cols
        )

        # Se ocorrer um erro na execução da query do usuário, exibe o feedback e interrompe
        if user_err:
            self.show_feedback(False, f"Erro na query: {user_err}")
            return
        # Se ocorrer um erro na query base, exibe feedback de erro
        if base_err:
            self.show_feedback(False, "Erro na resposta base!")
            return

        # Valida se o número de linhas retornadas pela query do usuário é igual ao da query base
        if (user_rows is None and base_rows is not None) or \
           (user_rows is not None and base_rows is None) or \
           (user_rows is not None and base_rows is not None and len(user_rows) != len(base_rows)):
            expected = len(base_rows) if base_rows is not None else 0
            self.show_feedback(False, f"Linhas incorretas. Esperado: {expected}")
            return

        # Compara a lógica da query do usuário com a query base (tabelas e condições lógicas)
        logic_ok, message = self.compare_query_logic(user_sql, base_sql)
        if not logic_ok:
            self.show_feedback(False, message)
            return

        # Se todas as validações passarem, exibe feedback de resposta correta
        self.show_feedback(True, "Resposta Correta!")

    def show_feedback(self, correct, message=""):
        """
        Exibe o feedback para o usuário.
        Se a resposta estiver correta, mostra uma mensagem em verde e habilita o botão para a próxima pergunta.
        Caso contrário, exibe uma mensagem em vermelho.
        """
        if correct:
            self.feedback_label.config(text="✅ Correto! " + message, foreground="green")
            self.next_button.config(state=tk.NORMAL)
        else:
            self.feedback_label.config(text="❌ Errado! " + message, foreground="red")

    def on_close(self):
        """
        Fecha a conexão com o banco, a janela de imagem (se aberta) e encerra a aplicação.
        Esse método é chamado quando o usuário fecha a janela principal.
        """
        if self.conn:
            self.conn.close()
        if self.image_window:
            self.image_window.destroy()
        self.root.destroy()

    def center_window(self, window, width, height):
        """
        Centraliza a janela 'window' na tela.
        Calcula a posição com base no tamanho da tela e nas dimensões da janela,
        e define a geometria da janela para que ela fique centralizada.
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    # Inicializa a aplicação criando a janela principal
    root = tk.Tk()
    app = SQLTrail(root)
    # Define que, ao fechar a janela principal, o método on_close é chamado para encerrar corretamente a aplicação
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    # Inicia o loop principal da interface Tkinter
    root.mainloop()
