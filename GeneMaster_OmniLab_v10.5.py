
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, simpledialog
import random
from datetime import datetime

class GeneMasterOmniLab:
    def __init__(self, root):
        self.root = root
        self.root.title("GENE-MASTER OMNI-LAB v10.5 | Universal Research")
        self.root.geometry("1450x950")
        self.root.configure(bg="#020617")

        # Sequência padrão inicial (pode ser qualquer uma)
        self.default_dna = "ATGTTTGTTTTTCTTGTTTTATTGCCACTAGT"
        self.database = {
            "SARS-CoV-2": "ATGTTTGTTTTTCTTGTTTTATTGCCACTAGT",
            "Insulina Humana": "AGCCCTCCAGGACAGGCTGCATCAGAAGAGGCC",
            "E. coli (K12)": "ATGAAACAAAGCACTATTGCACTGGCACTCTT",
            "H1N1 Influenza": "ATGAAGGCAATACTAGTAGTTCTGCTATATAC"
        }
        
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#0f172a", height=80)
        header.pack(fill="x")
        tk.Label(header, text="GENE-MASTER OMNI-LAB v10.5", font=("Consolas", 24, "bold"), fg="#22d3ee", bg="#0f172a").pack(side="left", padx=30)
        
        ctrl_panel = tk.Frame(self.root, bg="#020617", padx=20, pady=10)
        ctrl_panel.pack(fill="x")

        self.dna_input = tk.Entry(ctrl_panel, font=("Consolas", 14), bg="#1e293b", fg="#f8fafc", borderwidth=0)
        self.dna_input.insert(0, self.default_dna)
        self.dna_input.pack(fill="x", pady=10)

        toolbar = tk.Frame(ctrl_panel, bg="#020617")
        toolbar.pack(fill="x")

        tools = [
            ("BLAST ID", "#0ea5e9", self.exec_blast),
            ("CRISPR EDIT", "#f43f5e", self.simular_crispr),
            ("AUTO-CRISPR", "#b91c1c", self.auto_crispr),
            ("RODAR IA", "#7c3aed", self.prever_impacto_ia),
            ("TRADUZIR", "#a855f7", self.traduzir_proteina),
            ("COMPARAR", "#ec4899", self.comparar_proteinas),
            ("DENSIDADE", "#6366f1", self.plotar_densidade),
            ("ALINHAMENTO", "#fbbf24", self.alinhar_sequencias),
            ("ELETROFORESE", "#10b981", self.exec_gel),
            ("MUTAR", "#d946ef", self.mutar),
            ("DEFINIR BASE", "#4b5563", self.resetar_pesquisa),
            ("EXPORTAR", "#374151", self.exportar_relatorio)
        ]

        for text, color, cmd in tools:
            tk.Button(toolbar, text=text, bg=color, fg="white" if color != "#fbbf24" else "black", 
                      font=("Arial", 8, "bold"), width=13, command=cmd).pack(side="left", padx=2)

        main_frame = tk.Frame(self.root, bg="#020617")
        main_frame.pack(fill="both", expand=True, padx=20)

        self.canvas = tk.Canvas(main_frame, width=400, bg="#000", highlightthickness=1)
        self.canvas.pack(side="left", fill="y", pady=10)

        self.console = tk.Text(main_frame, bg="#0a0a0a", fg="#10b981", font=("Consolas", 10))
        self.console.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

    # --- LÓGICA DE PESQUISA ---

    def resetar_pesquisa(self):
        self.dna_base = self.dna_input.get().upper().strip()
        self.log(f"[SISTEMA]: Nova referência de pesquisa definida ({len(self.dna_base)} bp).")

    def traduzir_sequencia(self, dna_seq):
        tabela = {
            'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
            'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
            'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
            'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
            'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
            'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
            'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
            'TAC':'Y', 'TAT':'Y', 'TGC':'C', 'TGT':'C', 'TGG':'W', 'TAA':'_', 'TAG':'_', 'TGA':'_'
        }
        prot = ""
        for i in range(0, len(dna_seq) - 2, 3):
            aa = tabela.get(dna_seq[i:i+3], "?")
            if aa == "_": break
            prot += aa
        return prot

    def traduzir_proteina(self):
        dna = self.dna_input.get().upper().strip()
        proteina = self.traduzir_sequencia(dna)
        self.log(f"\n--- TRADUÇÃO DE PROTEÍNA ---\nCADEIA: {proteina}")

    def comparar_proteinas(self):
        dna_atual = self.dna_input.get().upper().strip()
        base = getattr(self, 'dna_base', self.default_dna)
            
        prot_ref = self.traduzir_sequencia(base)
        prot_atual = self.traduzir_sequencia(dna_atual)
        
        self.log("\n--- ANÁLISE DE IMPACTO FUNCIONAL ---")
        self.log(f"Proteína Base: {len(prot_ref)} AA | Proteína Atual: {len(prot_atual)} AA")
        
        diff = len(prot_ref) - len(prot_atual)
        if diff > 0:
            self.log(f"STATUS: ⚠️ Perda de {diff} aminoácidos (Deleção).")
        elif diff < 0:
            self.log(f"STATUS: ➕ Ganho de {abs(diff)} aminoácidos (Inserção).")
        else:
            self.log("STATUS: ✅ Estrutura de comprimento preservada.")

    def prever_impacto_ia(self):
        dna = self.dna_input.get().upper().strip()
        base = getattr(self, 'dna_base', self.default_dna)
        
        diffs = sum(1 for i in range(min(len(dna), len(base))) if dna[i] != base[i])
        diffs += abs(len(dna) - len(base))
        
        score = min(100, (diffs * 10)) 
        status = "CRÍTICO" if score > 70 else "MODERADO" if score > 30 else "ESTÁVEL"
        self.log(f"\n[IA PREDICTIVE]: Score de Divergência: {score}/100 | Veredito: {status}")

    def plotar_densidade(self):
        dna = self.dna_input.get().upper()
        self.log("\n--- MAPA DE DENSIDADE MOLECULAR ---")
        for i in range(0, len(dna), 5):
            seg = dna[i:i+5]
            gc = seg.count('G') + seg.count('C')
            barra = "█" * (gc * 2)
            self.log(f"Pos {i+1:02d}: [{barra:10s}] {'FORTE' if gc>=3 else 'FRACA'} ({seg})")

    def auto_crispr(self):
        dna = self.dna_input.get().upper()
        alvos = ["ATTGCC", "TTTTT", "GCGC"]
        for a in alvos:
            if a in dna:
                self.dna_input.delete(0, tk.END)
                self.dna_input.insert(0, dna.replace(a, ""))
                self.log(f"[AUTO-CRISPR]: Sequência viral {a} removida.")
                return
        self.log("[SISTEMA]: Nenhum alvo de clivagem detectado.")

    def exec_blast(self):
        dna = self.dna_input.get().upper()
        for name, seq in self.database.items():
            if dna in seq or seq in dna:
                self.log(f"[BLAST ID]: Identificado como: {name}")
                return
        self.log("[BLAST ID]: Sequência não catalogada (Nova Descoberta).")

    def simular_crispr(self):
        alvo = simpledialog.askstring("CRISPR", "Insira a sequência alvo para corte:")
        dna = self.dna_input.get().upper()
        if alvo and alvo.upper() in dna:
            self.dna_input.delete(0, tk.END)
            self.dna_input.insert(0, dna.replace(alvo.upper(), ""))
            self.log(f"[CRISPR]: Sítio {alvo} removido com sucesso.")

    def alinhar_sequencias(self):
        self.canvas.delete("all")
        dna = self.dna_input.get().upper()
        base = getattr(self, 'dna_base', self.default_dna)
        for i in range(min(len(dna), 12)):
            x = 30 + (i * 30)
            if i < len(base):
                cor = "#10b981" if dna[i] == base[i] else "#ef4444"
            else:
                cor = "#6366f1"
            self.canvas.create_rectangle(x, 50, x+25, 80, fill=cor)
            self.canvas.create_text(x+12, 65, text=dna[i], fill="white")

    def exec_gel(self):
        self.canvas.delete("all")
        size = len(self.dna_input.get())
        y = min(380, max(50, 400 - (size * 5)))
        self.canvas.create_rectangle(100, y, 250, y+5, fill="#a3e635")
        self.log(f"[ELETROFORESE]: Fragmento de {size}bp detectado no gel.")

    def mutar(self):
        dna = list(self.dna_input.get().upper())
        if dna:
            dna[random.randint(0, len(dna)-1)] = random.choice("ATCG")
            self.dna_input.delete(0, tk.END)
            self.dna_input.insert(0, "".join(dna))
            self.log("[MUTADOR]: Mutação randômica induzida.")

    def log(self, msg):
        self.console.insert(tk.END, f"{msg}\n")
        self.console.see(tk.END)

    def exportar_relatorio(self):
        conteudo = self.console.get("1.0", tk.END)
        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"RELATORIO_GENETICO_{data_hora}.txt"
        
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write("=== GENE-MASTER OMNI-LAB v10.5 | RELATÓRIO DE PESQUISA ===\n")
                f.write(f"Data do Experimento: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("-" * 50 + "\n")
                f.write(conteudo)
            messagebox.showinfo("Sucesso", f"Relatório exportado como:\n{nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneMasterOmniLab(root)
    root.mainloop()